-- 001_init.sql

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Categories
CREATE TABLE categories (
  id   SERIAL PRIMARY KEY,
  name TEXT   NOT NULL
);

-- Menu items
-- Enable pg_trgm extension for trigram indexes (useful for LIKE/ILIKE performance)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Menu items
CREATE TABLE menu_items (
  id            SERIAL        PRIMARY KEY,
  name          TEXT          NOT NULL,
  description   TEXT,
  price         NUMERIC(8,2)  NOT NULL,
  category_id   INTEGER       REFERENCES categories(id) ON DELETE SET NULL,
  is_special    BOOLEAN       DEFAULT FALSE,
  image_url     TEXT,
  is_available  BOOLEAN       DEFAULT TRUE,
  search_vector TSVECTOR
);

-- Create a GIN index on the search_vector for fast full-text search
CREATE INDEX menu_items_search_idx ON menu_items USING GIN (search_vector);

-- Create a function to update the search_vector
CREATE OR REPLACE FUNCTION update_menu_items_search_vector() RETURNS TRIGGER AS $
BEGIN
  NEW.search_vector = to_tsvector('english', NEW.name || ' ' || COALESCE(NEW.description, ''));
  RETURN NEW;
END;
$ LANGUAGE plpgsql;

-- Create a trigger to call the function before insert or update
CREATE TRIGGER menu_items_search_vector_update
BEFORE INSERT OR UPDATE OF name, description ON menu_items
FOR EACH ROW EXECUTE FUNCTION update_menu_items_search_vector();

-- Optionally, update existing rows
UPDATE menu_items SET search_vector = to_tsvector('english', name || ' ' || COALESCE(description, ''));

-- Orders & items
CREATE TABLE orders (
  id           BIGSERIAL  PRIMARY KEY,
  user_id      UUID       REFERENCES auth.users(id),
  scheduled_at TIMESTAMP  NOT NULL,
  status       TEXT       DEFAULT 'pending',
  created_at   TIMESTAMP  DEFAULT NOW()
);
CREATE TABLE order_items (
  order_id     BIGINT    REFERENCES orders(id) ON DELETE CASCADE,
  menu_item_id INTEGER   REFERENCES menu_items(id),
  quantity     INTEGER   DEFAULT 1,
  PRIMARY KEY(order_id, menu_item_id)
);

-- Reviews
CREATE TABLE reviews (
  id           BIGSERIAL  PRIMARY KEY,
  user_id      UUID       REFERENCES auth.users(id),
  menu_item_id INTEGER    REFERENCES menu_items(id),
  rating       INTEGER    CHECK (rating BETWEEN 1 AND 5),
  comment      TEXT,
  created_at   TIMESTAMP  DEFAULT NOW()
);

-- Favorites
CREATE TABLE favorites (
  user_id      UUID       REFERENCES auth.users(id),
  menu_item_id INTEGER    REFERENCES menu_items(id),
  PRIMARY KEY(user_id, menu_item_id)
);

-- Feedback & Complaints
CREATE TABLE feedback (
  id           BIGSERIAL  PRIMARY KEY,
  user_id      UUID       REFERENCES auth.users(id),
  content      TEXT       NOT NULL,
  created_at   TIMESTAMP  DEFAULT NOW()
);

-- Suggestions (new food items or dietary options)
CREATE TABLE suggestions (
  id           BIGSERIAL  PRIMARY KEY,
  user_id      UUID       REFERENCES auth.users(id),
  title        TEXT       NOT NULL,
  description  TEXT,
  created_at   TIMESTAMP  DEFAULT NOW()
);

-- Enable Row-Level Security
ALTER TABLE orders        ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_items   ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews       ENABLE ROW LEVEL SECURITY;
ALTER TABLE favorites     ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback      ENABLE ROW LEVEL SECURITY;
ALTER TABLE suggestions   ENABLE ROW LEVEL SECURITY;

-- Policies for ownership

CREATE POLICY "own_orders"
  ON orders
  FOR ALL
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "own_order_items"
  ON order_items
  FOR ALL
  TO authenticated
  USING (
    EXISTS (
      SELECT 1
        FROM orders o
       WHERE o.id = order_items.order_id
         AND o.user_id = auth.uid()
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1
        FROM orders o
       WHERE o.id = order_items.order_id
         AND o.user_id = auth.uid()
    )
  );

CREATE POLICY "own_reviews"
  ON reviews
  FOR ALL
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "own_favorites"
  ON favorites
  FOR ALL
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "own_feedback"
  ON feedback
  FOR ALL
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "own_suggestions"
  ON suggestions
  FOR ALL
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);
