# runs on port 1344 (ID: 22201344)
from flask import Flask, request, jsonify
import sqlite3, uuid, os
from datetime import datetime, timedelta, date

DB = "unieats_full.db"
CANCEL_LIMIT_MIN = 30  # cannot cancel within 30 min of pickup

app = Flask(__name__)


def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db(); c = conn.cursor()
    # Menu items (+ stock + category)
    c.execute("""
      CREATE TABLE IF NOT EXISTS menu_items(
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL, -- Snacks | Meals | Drinks | etc.
        price REAL NOT NULL,
        description TEXT,
        in_stock INTEGER NOT NULL DEFAULT 1
      )
    """)
    # Daily schedule: which items appear on which date
    c.execute("""
      CREATE TABLE IF NOT EXISTS menu_schedule(
        id TEXT PRIMARY KEY,
        menu_date TEXT NOT NULL,  -- YYYY-MM-DD
        item_id TEXT NOT NULL,
        UNIQUE(menu_date,item_id),
        FOREIGN KEY(item_id) REFERENCES menu_items(id)
      )
    """)
    # Today's specials (2–3 items per day)
    c.execute("""
      CREATE TABLE IF NOT EXISTS specials(
        id TEXT PRIMARY KEY,
        special_date TEXT NOT NULL,
        item_id TEXT NOT NULL,
        UNIQUE(special_date,item_id),
        FOREIGN KEY(item_id) REFERENCES menu_items(id)
      )
    """)
    # Orders (pre-orders)
    c.execute("""
      CREATE TABLE IF NOT EXISTS orders(
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        item_id TEXT NOT NULL,
        qty INTEGER NOT NULL,
        pickup_time TEXT NOT NULL,  -- ISO datetime
        status TEXT NOT NULL,       -- scheduled | cancelled | completed
        created_at TEXT NOT NULL,
        FOREIGN KEY(item_id) REFERENCES menu_items(id)
      )
    """)
    # Favorites
    c.execute("""
      CREATE TABLE IF NOT EXISTS favorites(
        user_id TEXT NOT NULL,
        item_id TEXT NOT NULL,
        created_at TEXT NOT NULL,
        PRIMARY KEY(user_id,item_id),
        FOREIGN KEY(item_id) REFERENCES menu_items(id)
      )
    """)
    # Reviews
    c.execute("""
      CREATE TABLE IF NOT EXISTS reviews(
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        item_id TEXT NOT NULL,
        rating INTEGER NOT NULL,  -- 1..5
        comment TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(item_id) REFERENCES menu_items(id)
      )
    """)
    # Feedback / complaints
    c.execute("""
      CREATE TABLE IF NOT EXISTS feedback(
        id TEXT PRIMARY KEY,
        user_id TEXT,
        kind TEXT NOT NULL,    -- complaint | suggestion | feedback
        message TEXT NOT NULL,
        contact TEXT,
        created_at TEXT NOT NULL
      )
    """)
    conn.commit()

    # Seed once
    c.execute("SELECT COUNT(*) AS n FROM menu_items"); 
    if c.fetchone()["n"] == 0:
        items = [
            ("Chicken Roll","Snacks",120.0,"Crispy wrap"),
            ("Veg Samosa","Snacks",25.0,"Spiced potato"),
            ("Beef Biryani","Meals",220.0,"Rich biryani"),
            ("Chicken Fried Rice","Meals",180.0,"Wok-fried"),
            ("Iced Lemon Tea","Drinks",60.0,"Refreshing"),
            ("Cold Coffee","Drinks",90.0,"Chilled coffee"),
            ("Vegan Wrap","Meals",200.0,"Plant-based wrap"),
        ]
        ids = []
        for (name,cat,price,desc) in items:
            mid = uuid.uuid4().hex; ids.append(mid)
            c.execute("INSERT INTO menu_items(id,name,category,price,description,in_stock) VALUES(?,?,?,?,?,1)",
                      (mid,name,cat,price,desc))
        # Schedule for today and the week
        today = date.today()
        schedule_map = {
            today: ids[:5],
            today+timedelta(days=1): ids[2:],
            today+timedelta(days=2): ids[:3],
            today+timedelta(days=3): ids[3:6],
            today+timedelta(days=4): ids[:2]+ids[4:6],
            today+timedelta(days=5): ids[1:5],
            today+timedelta(days=6): ids[::2],
        }
        for d, lst in schedule_map.items():
            for item_id in lst:
                c.execute("INSERT OR IGNORE INTO menu_schedule(id,menu_date,item_id) VALUES(?,?,?)",
                          (uuid.uuid4().hex, d.isoformat(), item_id))
        # Specials today: pick 3
        for item_id in ids[:3]:
            c.execute("INSERT OR IGNORE INTO specials(id,special_date,item_id) VALUES(?,?,?)",
                      (uuid.uuid4().hex, today.isoformat(), item_id))
        conn.commit()
    conn.close()

def rowdicts(rows): return [dict(r) for r in rows]

def parse_iso(dt_str):
    try:
        return datetime.fromisoformat(dt_str)
    except Exception:
        return None

# ---------- 1. View Daily/Weekly Menu ----------
@app.get("/api/menu/daily")
def menu_daily():
    qdate = request.args.get("date") or date.today().isoformat()
    conn = db(); c = conn.cursor()
    c.execute("""
      SELECT mi.* FROM menu_schedule ms
      JOIN menu_items mi ON mi.id=ms.item_id
      WHERE ms.menu_date=?
      ORDER BY mi.category, mi.name
    """, (qdate,))
    data = rowdicts(c.fetchall())
    conn.close()
    return jsonify({"ok": True, "date": qdate, "items": data}), 200

@app.get("/api/menu/weekly")
def menu_weekly():
    start = request.args.get("start")  # YYYY-MM-DD
    if start:
        try: start_date = datetime.fromisoformat(start).date()
        except Exception: return jsonify({"ok": False, "error":"start must be YYYY-MM-DD"}), 400
    else:
        start_date = date.today()
    end_date = start_date + timedelta(days=6)
    conn = db(); c = conn.cursor()
    c.execute("""
      SELECT ms.menu_date, mi.* FROM menu_schedule ms
      JOIN menu_items mi ON mi.id=ms.item_id
      WHERE ms.menu_date BETWEEN ? AND ?
      ORDER BY ms.menu_date, mi.category, mi.name
    """, (start_date.isoformat(), end_date.isoformat()))
    rows = c.fetchall(); conn.close()
    by_day = {}
    for r in rows:
        d = r["menu_date"]
        item = {k:r[k] for k in r.keys() if k!="menu_date"}
        by_day.setdefault(d, []).append(item)
    return jsonify({"ok": True, "start": start_date.isoformat(), "end": end_date.isoformat(), "days": by_day}), 200

# ---------- 2. Filter by Category + keyword search ----------
@app.get("/api/menu")
def menu_filter_search():
    category = (request.args.get("category") or "").strip()
    q = (request.args.get("q") or "").strip().lower()
    available_only = request.args.get("available_only") in ("1","true","yes")
    conn = db(); c = conn.cursor()
    sql = "SELECT * FROM menu_items WHERE 1=1"
    params = []
    if category:
        sql += " AND lower(category)=?"
        params.append(category.lower())
    if q:
        sql += " AND (lower(name) LIKE ? OR lower(description) LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    if available_only:
        sql += " AND in_stock=1"
    sql += " ORDER BY category, name"
    c.execute(sql, tuple(params))
    res = rowdicts(c.fetchall()); conn.close()
    return jsonify({"ok": True, "count": len(res), "items": res}), 200

# ---------- 3. Pre-order Food ----------
@app.post("/api/preorders")
def create_preorder():
    body = request.get_json(silent=True) or {}
    user_id = (body.get("user_id") or "").strip() or "user-001"
    item_id = (body.get("item_id") or "").strip()
    qty = int(body.get("qty") or 1)
    pickup_time = parse_iso(body.get("pickup_time") or "")
    if not item_id or not pickup_time:
        return jsonify({"ok": False, "error":"item_id and pickup_time (ISO) are required"}), 400
    conn = db(); c = conn.cursor()
    c.execute("SELECT in_stock FROM menu_items WHERE id=?", (item_id,))
    row = c.fetchone()
    if not row: 
        conn.close(); return jsonify({"ok": False, "error":"Invalid item_id"}), 404
    if row["in_stock"] != 1:
        conn.close(); return jsonify({"ok": False, "error":"Item out of stock"}), 409
    oid = uuid.uuid4().hex
    c.execute("""INSERT INTO orders(id,user_id,item_id,qty,pickup_time,status,created_at)
                 VALUES(?,?,?,?,?,?,?)""",
              (oid, user_id, item_id, qty, pickup_time.isoformat(), "scheduled", datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return jsonify({"ok": True, "order_id": oid, "status":"scheduled"}), 201

# ---------- 4. Cancel Pre-orders (time window) ----------
@app.delete("/api/preorders/<order_id>")
def cancel_preorder(order_id):
    conn = db(); c = conn.cursor()
    c.execute("SELECT id,pickup_time,status FROM orders WHERE id=?", (order_id,))
    row = c.fetchone()
    if not row: 
        conn.close(); return jsonify({"ok": False, "error":"Order not found"}), 404
    if row["status"] != "scheduled":
        conn.close(); return jsonify({"ok": False, "error":"Only scheduled orders can be cancelled"}), 409
    ptime = parse_iso(row["pickup_time"]); now = datetime.utcnow()
    if now > ptime - timedelta(minutes=CANCEL_LIMIT_MIN):
        conn.close(); 
        return jsonify({"ok": False, "error": f"Cancellation closed {CANCEL_LIMIT_MIN} min before pickup"}), 403
    c.execute("UPDATE orders SET status='cancelled' WHERE id=?", (order_id,))
    conn.commit(); conn.close()
    return jsonify({"ok": True, "order_id": order_id, "status":"cancelled"}), 200

# ---------- 5. Rate & Review Food Items ----------
@app.post("/api/reviews")
def create_review():
    b = request.get_json(silent=True) or {}
    user_id = (b.get("user_id") or "user-001").strip()
    item_id = (b.get("item_id") or "").strip()
    rating = int(b.get("rating") or 0)
    comment = (b.get("comment") or "").strip()
    if not item_id or rating < 1 or rating > 5:
        return jsonify({"ok": False, "error":"item_id and rating 1..5 required"}), 400
    conn = db(); c = conn.cursor()
    c.execute("SELECT id FROM menu_items WHERE id=?", (item_id,))
    if not c.fetchone(): conn.close(); return jsonify({"ok": False, "error":"Invalid item_id"}), 404
    rid = uuid.uuid4().hex
    c.execute("""INSERT INTO reviews(id,user_id,item_id,rating,comment,created_at)
                 VALUES(?,?,?,?,?,?)""",
              (rid,user_id,item_id,rating,comment,datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return jsonify({"ok": True, "review_id": rid}), 201

# ---------- 6. Submit Feedback / Complaints ----------
@app.post("/api/feedback")
def create_feedback():
    b = request.get_json(silent=True) or {}
    kind = (b.get("kind") or "").strip().lower()
    if kind not in {"complaint","suggestion","feedback"}:
        return jsonify({"ok": False, "error":"kind must be complaint|suggestion|feedback"}), 400
    fid = uuid.uuid4().hex
    conn = db(); c = conn.cursor()
    c.execute("""INSERT INTO feedback(id,user_id,kind,message,contact,created_at)
                 VALUES(?,?,?,?,?,?)""",
              (fid,b.get("user_id"),kind,(b.get("message") or "").strip(),
               (b.get("contact") or "").strip(), datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return jsonify({"ok": True, "feedback_id": fid}), 201

# ---------- 7. View Order History ----------
@app.get("/api/orders/history")
def order_history():
    user_id = (request.args.get("user_id") or "user-001").strip()
    conn = db(); c = conn.cursor()
    c.execute("""SELECT o.*, mi.name, mi.category FROM orders o
                 JOIN menu_items mi ON mi.id=o.item_id
                 WHERE o.user_id=? ORDER BY o.created_at DESC""", (user_id,))
    data = rowdicts(c.fetchall()); conn.close()
    return jsonify({"ok": True, "count": len(data), "orders": data}), 200

# ---------- 8. Suggest New Food Items or Dietary Options ----------
@app.post("/api/suggestions")
def suggest():
    b = request.get_json(silent=True) or {}
    kind = (b.get("kind") or "").strip().lower()
    name = (b.get("name") or "").strip()
    if kind not in {"food_item","dietary_option"} or not name:
        return jsonify({"ok": False, "error":"kind=food_item|dietary_option and name required"}), 400
    # Save as feedback 'suggestion'
    fid = uuid.uuid4().hex
    conn = db(); c = conn.cursor()
    c.execute("""INSERT INTO feedback(id,user_id,kind,message,contact,created_at)
                 VALUES(?,?,?,?,?,?)""",
              (fid,b.get("user_id"),"suggestion",
               f"[{kind}] {name} :: {(b.get('details') or '').strip()}",
               (b.get("contact") or "").strip(), datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return jsonify({"ok": True, "suggestion_id": fid, "message":"Suggestion submitted"}), 201

# ---------- 9. Favorite Items ----------
@app.post("/api/favorites")
def add_fav():
    b = request.get_json(silent=True) or {}
    user_id = (b.get("user_id") or "user-001").strip()
    item_id = (b.get("item_id") or "").strip()
    if not item_id: return jsonify({"ok": False, "error":"item_id required"}), 400
    conn = db(); c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO favorites(user_id,item_id,created_at) VALUES(?,?,?)",
              (user_id,item_id,datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return jsonify({"ok": True}), 201

@app.delete("/api/favorites")
def remove_fav():
    user_id = (request.args.get("user_id") or "user-001").strip()
    item_id = (request.args.get("item_id") or "").strip()
    if not item_id: return jsonify({"ok": False, "error":"item_id required"}), 400
    conn = db(); c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE user_id=? AND item_id=?", (user_id,item_id))
    conn.commit(); conn.close()
    return jsonify({"ok": True}), 200

@app.get("/api/favorites")
def list_fav():
    user_id = (request.args.get("user_id") or "user-001").strip()
    conn = db(); c = conn.cursor()
    c.execute("""SELECT mi.* FROM favorites f
                 JOIN menu_items mi ON mi.id=f.item_id
                 WHERE f.user_id=? ORDER BY mi.category, mi.name""", (user_id,))
    data = rowdicts(c.fetchall()); conn.close()
    return jsonify({"ok": True, "count": len(data), "items": data}), 200

# ---------- 10. Out-of-Stock Indicator ----------
@app.patch("/api/items/<item_id>/stock")
def update_stock(item_id):
    b = request.get_json(silent=True) or {}
    in_stock = b.get("in_stock")
    if in_stock not in (0,1,True,False):
        return jsonify({"ok": False, "error":"in_stock must be true/false"}), 400
    val = 1 if bool(in_stock) else 0
    conn = db(); c = conn.cursor()
    c.execute("UPDATE menu_items SET in_stock=? WHERE id=?", (val,item_id))
    if c.rowcount == 0:
        conn.close(); return jsonify({"ok": False, "error":"Item not found"}), 404
    conn.commit(); conn.close()
    return jsonify({"ok": True, "item_id": item_id, "in_stock": bool(val)}), 200

# ---------- 11. Today's Specials ----------
@app.get("/api/specials/today")
def specials_today():
    qdate = request.args.get("date") or date.today().isoformat()
    conn = db(); c = conn.cursor()
    c.execute("""SELECT mi.* FROM specials s
                 JOIN menu_items mi ON mi.id=s.item_id
                 WHERE s.special_date=?
                 ORDER BY mi.name
              """, (qdate,))
    data = rowdicts(c.fetchall()); conn.close()
    return jsonify({"ok": True, "date": qdate, "specials": data}), 200

# --------- Root ---------
@app.get("/")
def home():
    return "UniEats API ready. Try: /api/menu/daily, /api/menu?q=veg, /api/preorders, /api/orders/history, /api/specials/today"

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=1344)
