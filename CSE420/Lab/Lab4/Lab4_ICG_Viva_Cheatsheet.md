# CSE420 – Lab 4: Intermediate Code Generation (Three-Address Code)
### Complete Viva Cheat Sheet

---

## PART 1: WHAT IS THIS LAB ABOUT? (Explain in simple words)

### The big picture
In earlier labs you built:
- **Lab 2**: Lexer (Flex) — turns source code into tokens
- **Lab 3**: Parser (Bison) + Symbol Table + Semantic Analysis — checks the code is structurally and semantically correct

**Lab 4** adds the next stage of a compiler pipeline:
1. **Build an AST (Abstract Syntax Tree)** while parsing — a tree that represents the *structure* of the program (e.g., an assignment node has a variable and an expression as children).
2. **Walk (traverse) that AST** and emit **Three-Address Code (TAC)** — a simple, linear, low-level-ish intermediate representation where **each instruction has at most 3 operands** (one operator, at most two operands, one result).

### Why do we need an intermediate representation?
Machine code is too low-level to generate directly from source, and source code is too high-level/nested to translate directly to assembly. TAC is the "middle ground" — simple enough to be close to machine code, but still readable, and it also enables **optimizations** later (constant folding, dead code elimination, etc.) before final code generation.

### Easy example
C source:
```c
int a, b, c;
a = b + c * 2;
```

Three-address code generated (conceptually):
```
t0 = c
t1 = 2
t2 = t0 * t1     // c * 2
t3 = b
t4 = t3 + t2     // b + (c*2)
a = t4
```
Notice:
- Every complex expression is **broken down** into simple binary steps.
- Each step gets a fresh **temporary variable** `t0, t1, t2, ...`.
- Only ONE operation happens per line (this is the "three-address" idea: `result = operand1 op operand2`).

### Control flow example (if-statement)
```c
if (a > b)
    c = 1;
else
    c = 2;
```
Becomes:
```
t0 = a
t1 = b
t2 = t0 > t1
if t2 goto L0
goto L1
L0:
c = 1
goto L2
L1:
c = 2
L2:
```
Idea: a condition is evaluated into a temp, then we **jump (goto)** to the right label depending on true/false, and labels `L0, L1, L2...` mark where each branch begins/ends.

### Loop example (while)
```c
while (a < 10)
    a = a + 1;
```
Becomes:
```
L0:
t0 = a
t1 = 10
t2 = t0 < t1
if t2 goto L1
goto L2
L1:
t3 = a
t4 = 1
t5 = t3 + t4
a = t5
goto L0
L2:
```
Idea: `L0` = re-check condition (loop back target), `L1` = loop body, `L2` = loop exit.

### The three deliverables (from the lab handout)
1. **ast.h** — defines the AST node classes (the tree structure) and each node's `generate_code()` method (how that node emits TAC).
2. **three_addr_code.h** — a small **driver/wrapper class** (`ThreeAddrCodeGenerator`) that kicks off code generation by calling `generate_code()` on the root of the AST and writing header/footer comments into `code.txt`.
3. Modified **parser (.y file)** — builds the AST nodes *during* parsing (not shown in these two files, but this is where nodes like `AssignNode`, `BinaryOpNode` etc. actually get created and linked together as parsing happens, using the grammar actions).

### Key vocabulary the examiner may test
| Term | Meaning |
|---|---|
| **AST** | Abstract Syntax Tree — hierarchical structure representing the program (ignores punctuation, keeps meaning) |
| **Three-Address Code (TAC)** | Linear intermediate code, each instruction ≤ 3 addresses/operands |
| **Temporary variable (t0, t1, ...)** | Compiler-generated variable to hold an intermediate result |
| **Label (L0, L1, ...)** | A named point in the code that `goto`/`if goto` can jump to |
| **Backpatching** | (Not used here) technique to fill in jump targets later — this lab instead computes all labels immediately since it does a full tree traversal, so it doesn't need backpatching |
| **Recursive tree traversal / Visitor-like pattern** | Every node's `generate_code()` calls `generate_code()` on its children — this is how the whole tree gets walked (post-order-ish: children first, then the node's own operation) |
| **Virtual function / pure virtual (`= 0`)** | Enables polymorphism: calling `node->generate_code(...)` runs the correct override depending on the *actual* node type (VarNode, BinaryOpNode, etc.) even though `node` might be declared as a base `ASTNode*` pointer |
| **Symbol-to-temp map** | A `map<string,string>` that remembers "this variable currently lives in this temp", to avoid re-loading it from memory every time it's used |

---

## PART 2: `ast.h` — LINE BY LINE

### Header guards & includes (lines 1–10)
```cpp
1  #ifndef AST_H
2  #define AST_H
3
4  #include <iostream>
5  #include <vector>
6  #include <string>
7  #include <fstream>
8  #include <map>
9
10 using namespace std;
```
- **Lines 1–2**: Include guard — prevents this header from being included twice in the same compilation (would cause "class redefined" errors).
- **Line 4**: `<iostream>` — standard input/output stream types (not heavily used directly here, but pulled in for good measure / `endl` etc.).
- **Line 5**: `<vector>` — used for `vector<StmtNode*>`, `vector<ExprNode*>`, `vector<pair<...>>` (dynamic arrays).
- **Line 6**: `<string>` — used for variable names, operator symbols, type names.
- **Line 7**: `<fstream>` — gives us `ofstream` (output file stream) — the `outcode` parameter is an `ofstream&` referring to `code.txt`.
- **Line 8**: `<map>` — gives us `map<string,string>` used as `symbol_to_temp` (maps a variable name → the temp currently holding its value).
- **Line 10**: Avoids typing `std::` everywhere.

### Base class `ASTNode` (lines 12–16)
```cpp
12 class ASTNode {
13 public:
14     virtual ~ASTNode() {}
15     virtual string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp, int& temp_count, int& label_count) const = 0;
16 };
```
- **Line 12**: This is the **root/base class** every AST node type inherits from (as required by the lab: "A base ASTNode class that all other node types will inherit from").
- **Line 14**: `virtual ~ASTNode() {}` — a **virtual destructor**. This is essential in C++ whenever you plan to `delete` an object through a **base class pointer** (e.g., `delete some_ExprNode_ptr;` where the pointer is typed `ExprNode*` but actually points to a `BinaryOpNode`). Without `virtual`, only the base destructor would run, causing a **memory leak** (child object's own destructor, and its own members like `left`/`right` pointers, would never be freed).
- **Line 15**: The core contract — `generate_code(...)` is declared **pure virtual** (`= 0`). This means:
  - `ASTNode` is an **abstract class** — you cannot create a bare `ASTNode` object directly.
  - Every concrete subclass **must** implement (`override`) this function, or it also stays abstract.
  - Parameters:
    - `ofstream& outcode` — reference to the output file (`code.txt`) so each node can write its own generated instructions.
    - `map<string,string>& symbol_to_temp` — reference to the symbol→temp mapping table, shared and updated across the whole tree traversal.
    - `int& temp_count` — reference to a running counter for the next available temp number (`t0`, `t1`, …). Passed by reference so incrementing it in one node is visible to all others (global counter behavior without a global variable).
    - `int& label_count` — same idea but for label numbers (`L0`, `L1`, …).
  - Returns a `string` — normally the **name of the temp variable holding the result** of that expression (for expression nodes), or `""` empty string for statement nodes that don't produce a usable value.

**Viva tip:** If asked "why pass `temp_count` and `label_count` by reference (`int&`)?" — answer: so that the counters are **shared/global across the entire recursive traversal**; if passed by value, each node would reset to the same starting number and you'd get duplicate temp names like `t0` reused everywhere.

### `ExprNode` — base class for all expressions (lines 18–27)
```cpp
20 class ExprNode : public ASTNode {
21 protected:
22     string node_type;
23 public:
24     ExprNode(string type) : node_type(type) {}
25     virtual string get_type() const { return node_type; }
26     virtual ExprNode* clone() const = 0;
27 };
```
- **Line 20**: `ExprNode` inherits publicly from `ASTNode` — so an `ExprNode` **is-an** `ASTNode`, and must still provide `generate_code` (still inherited as pure virtual, so `ExprNode` itself also remains abstract).
- **Line 21–22**: `protected` member `node_type` — stores the **result type** of this expression (e.g., "int", "float"). `protected` (not `private`) so that derived classes (VarNode, BinaryOpNode, etc.) can access it directly.
- **Line 24**: Constructor — takes the type as a string and stores it via a **member initializer list** (`: node_type(type)`), which is the efficient/idiomatic way to initialize members in C++.
- **Line 25**: `get_type()` — simple getter, returns the stored type. Marked `virtual` so subclasses *could* override it if needed (though none here do).
- **Line 26**: `clone() const = 0` — another **pure virtual function**. Every expression node must be able to **make a deep copy of itself**. This is needed because, during parsing, the same sub-expression sometimes needs to be duplicated (e.g., for compound assignment expansion like `a += b` → `a = a + b`, you need two independent copies of `a`). Being `const` means calling `clone()` doesn't modify the original object.

### `VarNode` — variable reference (lines 29–81)
```cpp
31 class VarNode : public ExprNode {
32 private:
33     string name;
34     ExprNode* index;
```
- **Line 31**: `VarNode` represents a reference to a variable, e.g. `a` or `arr[i]`.
- **Line 33**: `name` — the variable's identifier text (e.g., `"a"`).
- **Line 34**: `index` — pointer to an `ExprNode` representing the **array index expression**, if this variable access is an array access like `a[i+1]`. If it's a plain scalar variable, `index` is `nullptr`.

```cpp
37     VarNode(string name, string type, ExprNode* idx = nullptr)
38         : ExprNode(type), name(name), index(idx) {}
```
- **Lines 37–38**: Constructor. Calls the base class `ExprNode(type)` constructor first (member init list), then sets `name` and `index`. `idx` **defaults to `nullptr`** so you can construct a plain variable as `VarNode("a", "int")` without explicitly passing an index.

```cpp
40     ~VarNode() { if(index) delete index; }
```
- **Line 40**: Destructor — if this VarNode owns an index sub-expression, delete it (**ownership**: VarNode is responsible for freeing memory of its `index` child, preventing memory leaks). The `if(index)` check guards against deleting a `nullptr` (though `delete nullptr` is technically safe in C++, this is defensive/clear style).

```cpp
42     bool has_index() const { return index != nullptr; }
```
- **Line 42**: Helper — tells callers (like `AssignNode`) whether this variable is actually an array access (`a[i] = ...`) or a plain variable (`a = ...`). `const` because it doesn't modify the object.

```cpp
44     string generate_index_code(ofstream& outcode, map<string, string>& symbol_to_temp,
45                               int& temp_count, int& label_count) const {
46         return index->generate_code(outcode, symbol_to_temp, temp_count, label_count);
47     }
```
- **Lines 44–47**: A small helper that generates code for just the **index expression** (e.g., for `a[i+1]`, this generates the code that computes `i+1` into a temp) and returns that temp's name. This is reused both when *reading* the array (inside `generate_code` below) and when *writing* to the array (called from `AssignNode`).

```cpp
49     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
50                         int& temp_count, int& label_count) const override {
51         if(index != nullptr)
52         {
53             string idx_temp = generate_index_code(outcode, symbol_to_temp, temp_count, label_count);
54             string temp = "t" + to_string(temp_count++);
55             outcode << temp << " = " << name << "[" << idx_temp << "]" << endl;
56             return temp;
57         }
```
- **Line 49–50**: The actual override of the pure virtual function, marked `override` (compiler checks it really does override a base virtual function — catches typos).
- **Lines 51–57**: **Array-read case.** If there's an index:
  - Line 53: Recursively generate code for the index expression, get the temp holding the index value (e.g. `t0` holding `i+1`'s result).
  - Line 54: Allocate a brand-new temp name using the current `temp_count`, **then increment it** (`temp_count++` is post-increment: use the old value, then bump it by 1) — this is how `t0, t1, t2, ...` are produced without ever repeating.
  - Line 55: Write the instruction `tN = name[idx_temp]` to the output file, e.g. `t1 = arr[t0]`.
  - Line 56: Return the new temp's name so the **caller** (e.g. a `BinaryOpNode` using this array element in an expression) knows where the value now lives.

```cpp
59         if(symbol_to_temp.find("_param_" + name) != symbol_to_temp.end())
60         {
61             return symbol_to_temp[name];
62         }
```
- **Lines 59–62**: **Function-parameter shortcut.** Recall in `FuncDeclNode::generate_code` (explained later), for every parameter the map gets a special marker key `"_param_" + paramName` set to `"1"`. So this check means: "is `name` actually a function parameter?" If yes, we just return its **already-known temp** from `symbol_to_temp[name]` directly, **without emitting a new `tN = name` line** — because the parameter's value was already loaded into a temp once, right when the function started (see `FuncDeclNode`), so there's no need to reload it every time it's referenced.

```cpp
64         string temp = "t" + to_string(temp_count++);
65         if(symbol_to_temp.find(name) != symbol_to_temp.end())
66         {
67             return symbol_to_temp[name];
68         }
69
70         outcode << temp << " = " << name << endl;
71         symbol_to_temp[name] = temp;
72         return temp;
73     }
```
- **Plain-scalar-variable case** (no index, not a parameter):
  - Line 64: Pre-allocate a new temp name (note: this happens *before* checking the map — meaning `temp_count` is incremented here regardless, even if this particular temp ends up unused — a small quirk/inefficiency you should be aware of if asked "does every call increase temp_count?" — **yes, line 64 always increments it**).
  - Lines 65–68: If this variable's current value is **already cached** in `symbol_to_temp` (meaning we loaded/assigned it before), just **reuse that existing temp** and return it — this **avoids redundant reload instructions** like re-emitting `t5 = a` every single time `a` is mentioned.
  - Lines 70–72: Otherwise, this is the **first time** we're loading this variable: emit `tN = name` (e.g. `t0 = a`), record in the map that `a`'s current value lives in `t0`, and return that temp.
- **Line 73**: closing brace of `generate_code`.

```cpp
75     string get_name() const { return name; }
```
- **Line 75**: Simple getter for the variable's name — used by `AssignNode` to know what to assign into (e.g. `outcode << lhs->get_name() << " = " ...`).

```cpp
77     ExprNode* clone() const override {
78         ExprNode* cloned_index = index != nullptr ? index->clone() : nullptr;
79         return new VarNode(name, node_type, cloned_index);
80     }
81 };
```
- **Lines 77–80**: Implements the deep-copy contract from `ExprNode`. If there's an index, recursively clone it too (deep clone, not just copying the pointer — so the original and the copy own **independent** index sub-trees and won't double-delete). Then constructs and returns a brand new `VarNode` with the same name/type and the cloned index.
- **Line 81**: End of class.

### `ConstNode` — literal constants (lines 83–102)
```cpp
85 class ConstNode : public ExprNode {
86 private:
87     string value;
88
89 public:
90     ConstNode(string val, string type) : ExprNode(type), value(val) {}
```
- **Line 87**: Stores the constant's literal text, e.g. `"5"`, `"3.14"`.
- **Line 90**: Constructor stores value and passes type up to `ExprNode`.

```cpp
92     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
93                         int& temp_count, int& label_count) const override {
94         string temp = "t" + to_string(temp_count++);
95         outcode << temp << " = " << value << endl;
96         return temp;
97     }
```
- **Lines 92–97**: For a constant, code generation is simple: always allocate a fresh temp and emit `tN = value` (e.g. `t2 = 5`), then return that temp. (Note: unlike `VarNode`, there's no caching here — every use of the same literal constant produces a new temp/instruction. If asked "why doesn't ConstNode cache like VarNode?" — a reasonable answer: constants don't have a persistent "current value" concept the way variables do, and TAC generation here treats each occurrence independently for simplicity/matching the sample output.)

```cpp
99     ExprNode* clone() const override {
100        return new ConstNode(value, node_type);
101    }
102 };
```
- **Lines 99–101**: Clone is trivial here since there are no child pointers to deep-copy — just make a new object with the same value/type.

### `BinaryOpNode` — binary operations (lines 104–134)
```cpp
106 class BinaryOpNode : public ExprNode {
107 private:
108     string op;
109     ExprNode* left;
110     ExprNode* right;
```
- Represents things like `a + b`, `x * y`, `p < q`, `m && n`.
- **Line 108**: the operator as text, e.g. `"+"`, `"<"`, `"&&"`.
- **Lines 109–110**: pointers to the left and right operand sub-expressions (which are themselves `ExprNode`s — could be `VarNode`, `ConstNode`, or another nested `BinaryOpNode`, etc. — this recursive structure is exactly what an AST is).

```cpp
113     BinaryOpNode(string op, ExprNode* left, ExprNode* right, string result_type)
114         : ExprNode(result_type), op(op), left(left), right(right) {}
```
- **Line 113–114**: Constructor takes ownership of `left` and `right` pointers (they must have been `new`-allocated by the caller/parser).

```cpp
116     ~BinaryOpNode() {
117         delete left;
118         delete right;
119     }
```
- **Lines 116–119**: Destructor frees both children — this is what makes the whole tree's memory get cleaned up recursively: deleting the root eventually deletes every node, because each parent's destructor deletes its children, whose destructors delete *their* children, and so on.

```cpp
121     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
122                         int& temp_count, int& label_count) const override {
123         string left_temp = left->generate_code(outcode, symbol_to_temp, temp_count, label_count);
124         string right_temp = right->generate_code(outcode, symbol_to_temp, temp_count, label_count);
125
126         string temp = "t" + to_string(temp_count++);
127         outcode << temp << " = " << left_temp << " " << op << " " << right_temp << endl;
128         return temp;
129     }
```
- **This is the heart of "three-address code" generation.**
  - Line 123: **Recursively** generate code for the left sub-expression first — this may itself emit several lines if `left` is a nested expression — and get back the temp holding its final result.
  - Line 124: Same for the right sub-expression.
  - Line 126: Allocate one fresh temp for **this** operation's result.
  - Line 127: Emit exactly one instruction combining the two already-computed temps: `tN = left_temp op right_temp` — this is precisely the "three address" format: **1 result + 2 operands (+1 operator)**.
  - Line 128: Return the new temp so a parent node (or the statement using this expression) knows where the final value is.
- **Order matters here**: left is evaluated completely before right starts — this is why, for `a + b*c`, you'd first fully resolve `a` into a temp, then fully resolve `b*c` into another temp, and only then combine them — matching standard left-to-right evaluation order.

```cpp
131     ExprNode* clone() const override {
132         return new BinaryOpNode(op, left->clone(), right->clone(), node_type);
133     }
134 };
```
- **Lines 131–133**: Deep clone — recursively clones both children so the copy is fully independent.

### `UnaryOpNode` — unary operations (lines 136–161)
```cpp
138 class UnaryOpNode : public ExprNode {
139 private:
140     string op;
141     ExprNode* expr;
```
- Represents things like `-x`, `!flag`.
- Single operand (`expr`) instead of two.

```cpp
144     UnaryOpNode(string op, ExprNode* expr, string result_type)
145         : ExprNode(result_type), op(op), expr(expr) {}
146
147     ~UnaryOpNode() { delete expr; }
```
- Straightforward constructor/destructor, same ownership pattern as before but for a single child.

```cpp
149     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
150                         int& temp_count, int& label_count) const override {
151         string expr_temp = expr->generate_code(outcode, symbol_to_temp, temp_count, label_count);
152
153         string temp = "t" + to_string(temp_count++);
154         outcode << temp << " = " << op << expr_temp << endl;
155         return temp;
156     }
```
- Same idea as `BinaryOpNode` but with only one operand: first evaluate the sub-expression into a temp, then emit `tN = op expr_temp` (e.g. `t3 = -t2` or `t3 = !t2`), no space between `op` and `expr_temp` (matches formats like `-t2`).

```cpp
158     ExprNode* clone() const override {
159         return new UnaryOpNode(op, expr->clone(), node_type);
160     }
161 };
```
- Deep clone of the single child.

### `AssignNode` — assignment (lines 163–203)
```cpp
165 class AssignNode : public ExprNode {
166 private:
167     VarNode* lhs;
168     ExprNode* rhs;
```
- Represents `a = expr` or `arr[i] = expr`. Note `lhs` is specifically typed `VarNode*` (not generic `ExprNode*`) because **only a variable (possibly with an index) can appear on the left of `=`** — you can't assign into `5` or `a+b`. This is a good example of using the type system to enforce a language rule at the AST level.
- **Why does AssignNode extend `ExprNode` and not `StmtNode`?** Because in C, assignment is itself an **expression** with a value (e.g. `x = (y = 5);` or `while ((c = getchar()) != EOF)`), so it needs to return a result temp just like other expressions.

```cpp
171     AssignNode(VarNode* lhs, ExprNode* rhs, string result_type)
172         : ExprNode(result_type), lhs(lhs), rhs(rhs) {}
173
174     ~AssignNode() {
175         delete lhs;
176         delete rhs;
177     }
```
- Standard constructor/destructor with ownership of both sides.

```cpp
179     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
180                         int& temp_count, int& label_count) const override {
181         string rhs_temp = rhs->generate_code(outcode, symbol_to_temp, temp_count, label_count);
182
183         if(lhs->has_index())
184         {
185             string idx_temp = lhs->generate_index_code(outcode, symbol_to_temp, temp_count, label_count);
186             outcode << lhs->get_name() << "[" << idx_temp << "] = " << rhs_temp << endl;
187         }
```
- **Line 181**: First, fully evaluate the right-hand side expression (could be arbitrarily complex/nested) into a temp `rhs_temp`. This means the RHS is *always* computed before we deal with where it's stored — matches normal evaluation order (compute the value first, then store it).
- **Lines 183–187**: **Array-write case** (`lhs` is like `arr[i]`):
  - Line 185: Generate code for the index expression (e.g. `i+1`), getting `idx_temp`.
  - Line 186: Emit `name[idx_temp] = rhs_temp`, e.g. `arr[t2] = t5`. Note this does **not** go through the `symbol_to_temp` map — array elements aren't cached as scalars because each index could refer to a different memory slot.

```cpp
188         else
189         {
190             outcode << lhs->get_name() << " = " << rhs_temp << endl;
191             if(symbol_to_temp.find(lhs->get_name()) != symbol_to_temp.end())
192             {
193                 symbol_to_temp[lhs->get_name()] = rhs_temp;
194             }
195         }
196
197         return rhs_temp;
198     }
```
- **Lines 188–195**: **Plain scalar-write case**:
  - Line 190: Emit the direct assignment instruction, e.g. `a = t5`.
  - Lines 191–194: **Cache update** — if `a` was *already* being tracked in `symbol_to_temp` (i.e., it had been read/used before), **update the map** so that from now on, `a`'s current value is known to be in `rhs_temp` — this way, the *next* time `a` is read, `VarNode::generate_code` can reuse `rhs_temp` directly instead of re-emitting `tN = a`.
  - **Important subtlety** (good viva question): if `a` was **never previously in the map** (never read before), this `if` is **false**, so the map is **not updated** here — meaning the *next* read of `a` will go through `VarNode`'s normal path and emit a fresh `tN = a` load, rather than reusing `rhs_temp`. So caching only "kicks in" for variables that have already been touched once as a read.
  - Line 197: Return `rhs_temp` — because in C, an assignment expression's value **is** the assigned value (enables chained assignment `a = b = 5`).

```cpp
200     ExprNode* clone() const override {
201         return new AssignNode((VarNode*)lhs->clone(), rhs->clone(), node_type);
202     }
203 };
```
- **Line 201**: Clones both sides. `lhs->clone()` returns `ExprNode*` (the declared return type of `clone()`), so it must be **cast back to `VarNode*`** with `(VarNode*)` since we know (by construction) that a `VarNode`'s `clone()` always actually returns a `VarNode` object underneath — this is a **downcast**, safe here because of how `clone()` is implemented for `VarNode`.

### `StmtNode` — base class for statements (lines 205–211)
```cpp
207 class StmtNode : public ASTNode {
208 public:
209     virtual string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
210                                 int& temp_count, int& label_count) const = 0;
211 };
```
- Parallel to `ExprNode`, but for statements (if, while, for, blocks, return, declarations...). Statements generally **don't produce a value** (hence they usually `return ""`), they just perform actions / emit code.
- Still pure virtual — `StmtNode` remains abstract.

### `ExprStmtNode` — expression statement (lines 213–237)
```cpp
215 class ExprStmtNode : public StmtNode {
216 private:
217     ExprNode* expr;
218
219 public:
220     ExprStmtNode(ExprNode* e) : expr(e) {}
221     ~ExprStmtNode() { if(expr) delete expr; }
```
- Wraps a bare expression used as a statement, e.g. `a = b + c;` on its own line, or a function call used as a statement `foo();`.

```cpp
223     ExprNode* release_expr() {
224         ExprNode* e = expr;
225         expr = nullptr;
226         return e;
227     }
```
- **Lines 223–227**: "Releases" ownership of the inner expression — sets its own pointer to `nullptr` and returns the raw pointer to the caller. This pattern (like `std::unique_ptr::release()`) is used when the parser needs to **pull the expression back out** to reuse it elsewhere (e.g., extracting the expression from an `ExprStmtNode` wrapper to embed it directly into a `ForNode`'s `init`/`update` slots without double-deleting it). After this call, `ExprStmtNode`'s destructor won't delete `expr` anymore (since it's now `nullptr`), so ownership has cleanly transferred to whoever called `release_expr()`.

```cpp
229     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
230                         int& temp_count, int& label_count) const override {
231         if(expr != nullptr)
232         {
233             expr->generate_code(outcode, symbol_to_temp, temp_count, label_count);
234         }
235         return "";
236     }
237 };
```
- Simply forwards code generation to the wrapped expression (its side-effects/instructions get written), but **discards the returned temp** (the value isn't needed since this is used as a plain statement, not embedded in a larger expression) and returns `""` since a statement itself has no "result temp" to hand back up.

### `PrintNode` — print statement (lines 239–256)
```cpp
241 class PrintNode : public StmtNode {
242 private:
243     ExprNode* expr;
244
245 public:
246     PrintNode(ExprNode* e) : expr(e) {}
247     ~PrintNode() { if(expr) delete expr; }
248
249     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
250                         int& temp_count, int& label_count) const override {
251         string val_temp = expr->generate_code(outcode, symbol_to_temp, temp_count, label_count);
252         outcode << "param " << val_temp << endl;
253         outcode << "call printf, 1" << endl;
254         return "";
255     }
256 };
```
- Handles something like `print(x);` in the source language.
- Line 251: Evaluate the expression to print into a temp.
- Line 252: Emit `param val_temp` — the standard TAC convention for "push an argument before a call".
- Line 253: Emit `call printf, 1` — calls `printf` with `1` argument. This models how function calls with arguments are represented in TAC (parameters listed first via `param`, then a `call` instruction naming the function and the argument count).
- Not covered value returned since printing is a statement (`return ""`).

### `BlockNode` — compound statement `{ ... }` (lines 258–286)
```cpp
260 class BlockNode : public StmtNode {
261 private:
262     vector<StmtNode*> statements;
```
- Represents `{ stmt1; stmt2; stmt3; }` — a sequence of statements. Uses a `vector` because a block can have **any number** of statements.

```cpp
265     ~BlockNode() {
266         for (auto stmt : statements) {
267             delete stmt;
268         }
269     }
```
- Destructor loops through and deletes every statement it owns (`auto stmt` deduces `StmtNode*` for each element).

```cpp
271     void add_statement(StmtNode* stmt) {
272         if (stmt) statements.push_back(stmt);
273     }
```
- Called by the parser while building the tree — appends one more statement to this block, guarding against adding a `nullptr`.

```cpp
275     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
276                         int& temp_count, int& label_count) const override {
277         for(int i = 0; i < statements.size(); i++)
278         {
279             if(statements[i] != nullptr)
280             {
281                 statements[i]->generate_code(outcode, symbol_to_temp, temp_count, label_count);
282             }
283         }
284         return "";
285     }
286 };
```
- Simply generates code for each statement **in order**, top to bottom, which is exactly how a block of statements executes.

### `IfNode` — if / if-else (lines 288–333)
```cpp
290 class IfNode : public StmtNode {
291 private:
292     ExprNode* condition;
293     StmtNode* then_block;
294     StmtNode* else_block;
```
- Line 294: `else_block` can be `nullptr` if there's no `else` part.

```cpp
297     IfNode(ExprNode* cond, StmtNode* then_stmt, StmtNode* else_stmt = nullptr)
298         : condition(cond), then_block(then_stmt), else_block(else_stmt) {}
```
- `else_stmt` defaults to `nullptr`, so a plain `if` without `else` can call `IfNode(cond, thenStmt)`.

```cpp
300     ~IfNode() {
301         delete condition;
302         delete then_block;
303         if (else_block) delete else_block;
304     }
```
- Frees all three children (guarding `else_block` since it may be null).

```cpp
306     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
307                         int& temp_count, int& label_count) const override {
308         string cond_temp = condition->generate_code(outcode, symbol_to_temp, temp_count, label_count);
309
310         int true_label = label_count++;
311         int false_label = label_count++;
312         int end_label = label_count++;
313
314         outcode << "if " << cond_temp << " goto L" << true_label << endl;
315         outcode << "goto L" << false_label << endl;
316         outcode << "L" << true_label << ":" << endl;
317
318         if(then_block != nullptr) {
319             then_block->generate_code(outcode, symbol_to_temp, temp_count, label_count);
320         }
321
322         outcode << "goto L" << end_label << endl;
323         outcode << "L" << false_label << ":" << endl;
324
325         if(else_block != nullptr) {
326             else_block->generate_code(outcode, symbol_to_temp, temp_count, label_count);
327         }
328
329         outcode << "L" << end_label << ":" << endl;
330
331         return "";
332     }
333 };
```
- **Step-by-step trace** (this is the classic viva "explain this function" target):
  1. **Line 308**: Evaluate the `if` condition into a temp.
  2. **Lines 310–312**: Reserve **three fresh label numbers** upfront: one for the "true" branch, one for "false" branch, one for the "end" (join point after the if-else). Note: labels are allocated **before** any code for the branches is generated, because we need to know their numbers to write the `goto`/`if goto` lines *before* the branch bodies are emitted.
  3. **Line 314**: `if cond_temp goto L<true>` — if condition is true (non-zero), jump into the then-branch.
  4. **Line 315**: `goto L<false>` — otherwise (falls through if the `if` above didn't jump), unconditionally jump to the false-branch. (This two-line pattern — `if X goto TRUE` then `goto FALSE` — is the standard TAC idiom for "if-else" branching, since TAC typically only has conditional-jump-if-true, not if-false.)
  5. **Line 316**: Emit the `true_label:` label — marks where the then-branch code begins.
  6. **Lines 318–320**: Generate the then-branch's code (only if it exists, i.e. not null).
  7. **Line 322**: After the then-branch finishes, `goto end_label` — **skip over** the else-branch (very important, otherwise execution would fall through into the else code too).
  8. **Line 323**: Emit `false_label:` — marks where the else-branch begins.
  9. **Lines 325–327**: Generate the else-branch's code, if present (if `else_block` is null, this label will just be empty/immediately followed by the end label).
  10. **Line 329**: Emit `end_label:` — the join point after the whole if-else, where control continues normally.
- Returns `""` since `if` produces no value.

### `WhileNode` — while loop (lines 335–373)
```cpp
337 class WhileNode : public StmtNode {
338 private:
339     ExprNode* condition;
340     StmtNode* body;
```

```cpp
351     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
352                         int& temp_count, int& label_count) const override {
353         int start_label = label_count++;
354         int body_label = label_count++;
355         int end_label = label_count++;
356
357         outcode << "L" << start_label << ":" << endl;
358
359         string cond_temp = condition->generate_code(outcode, symbol_to_temp, temp_count, label_count);
360         outcode << "if " << cond_temp << " goto L" << body_label << endl;
361         outcode << "goto L" << end_label << endl;
362         outcode << "L" << body_label << ":" << endl;
363
364         if(body != nullptr) {
365             body->generate_code(outcode, symbol_to_temp, temp_count, label_count);
366         }
367
368         outcode << "goto L" << start_label << endl;
369         outcode << "L" << end_label << ":" << endl;
370
371         return "";
372     }
373 };
```
- **Trace**:
  1. Reserve 3 labels: `start` (where the condition is (re)checked — the loop-back target), `body` (loop body start), `end` (after the loop).
  2. Emit `start_label:` — this is where every iteration begins by re-testing the condition.
  3. Evaluate the condition **fresh each time** we reach `start_label` (since it's inside the label's scope — note the condition's code is generated *after* the label so it will execute every time control jumps back here).
  4. `if cond_temp goto body_label` — if true, enter the loop body.
  5. `goto end_label` — otherwise, exit the loop.
  6. Emit `body_label:` and generate the loop body's code.
  7. **Line 368**: After the body finishes, `goto start_label` — **loop back** to re-check the condition (this is what makes it a loop!).
  8. Emit `end_label:` — where control lands once the condition becomes false.
- Compare with `IfNode`: the key structural difference is the **extra `goto start_label` at the end** that jumps backward, creating the repeat behavior, and the condition sits behind a label so it's re-evaluated every pass.

### `ForNode` — for loop (lines 375–435)
```cpp
377 class ForNode : public StmtNode {
378 private:
379     ExprNode* init;
380     ExprNode* condition;
381     ExprNode* update;
382     StmtNode* body;
```
- Represents `for(init; condition; update) body`. All four parts are separate (unlike while, which only has condition+body).

```cpp
385     ForNode(ExprNode* init_expr, ExprNode* cond_expr, ExprNode* update_expr, StmtNode* body_stmt)
386         : init(init_expr), condition(cond_expr), update(update_expr), body(body_stmt) {}
387
388     ~ForNode() {
389         if (init) delete init;
390         if (condition) delete condition;
391         if (update) delete update;
392         if (body) delete body;
393     }
```
- All four parts guarded with `if(...)` before deleting since **any of them can legally be omitted** in C (e.g. `for(;;)` — infinite loop with no init/condition/update).

```cpp
395     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
396                         int& temp_count, int& label_count) const override {
397         if(init != nullptr)
398         {
399             init->generate_code(outcode, symbol_to_temp, temp_count, label_count);
400         }
```
- **Lines 397–400**: Generate the **init** expression's code **once**, before the loop starts (e.g. `i = 0`) — matches C semantics: init runs exactly once.

```cpp
402         int start_label = label_count++;
403         int body_label = label_count++;
404         int end_label = label_count++;
405
406         outcode << "L" << start_label << ":" << endl;
407
408         if(condition != nullptr)
409         {
410             string cond_temp = condition->generate_code(outcode, symbol_to_temp, temp_count, label_count);
411             outcode << "if " << cond_temp << " goto L" << body_label << endl;
412             outcode << "goto L" << end_label << endl;
413         }
414         else
415         {
416             outcode << "goto L" << body_label << endl;
417         }
```
- Same 3-label scheme as `while`.
- **Lines 408–413**: If a condition exists, evaluate it every time we reach `start_label`, and branch to body or end accordingly (same idiom as before).
- **Lines 414–417**: If there's **no condition** (e.g. `for(;;)`), that means the loop should run **unconditionally forever** (until a `break`/`return`), so just always `goto body_label` directly — no test needed.

```cpp
419         outcode << "L" << body_label << ":" << endl;
420         if(body != nullptr)
421         {
422             body->generate_code(outcode, symbol_to_temp, temp_count, label_count);
423         }
424
425         if(update != nullptr)
426         {
427             update->generate_code(outcode, symbol_to_temp, temp_count, label_count);
428         }
429
430         outcode << "goto L" << start_label << endl;
431         outcode << "L" << end_label << ":" << endl;
432
433         return "";
434     }
435 };
```
- Emit `body_label:`, generate the body.
- **Lines 425–428**: **Crucially**, generate the **update** expression's code (e.g. `i = i + 1`) **after the body, but still inside the loop**, and **before** looping back — this matches C's `for` semantics exactly: `init; while(cond) { body; update; }`.
- **Line 430**: `goto start_label` — loop back to re-check condition (note it jumps to `start_label`, not directly to body — so the condition is re-tested every iteration, correctly stopping the loop when false).
- **Line 431**: `end_label:` — loop exit point.

**Viva one-liner**: *"A `for` loop is really syntactic sugar for `init; while(cond){ body; update; }`, and that's literally how `ForNode::generate_code` is structured."*

### `ReturnNode` — return statement (lines 437–460)
```cpp
439 class ReturnNode : public StmtNode {
440 private:
441     ExprNode* expr;
```
- `expr` may be `nullptr` for a bare `return;` with no value (e.g., in a `void` function).

```cpp
447     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
448                         int& temp_count, int& label_count) const override {
449         if(expr != nullptr)
450         {
451             string expr_temp = expr->generate_code(outcode, symbol_to_temp, temp_count, label_count);
452             outcode << "return " << expr_temp << endl;
453         }
454         else
455         {
456             outcode << "return" << endl;
457         }
458         return "";
459     }
460 };
```
- If there's a return value, evaluate it into a temp and emit `return tN`; otherwise, just emit bare `return`.

### `DeclNode` — variable declaration (lines 462–494)
```cpp
464 class DeclNode : public StmtNode {
465 private:
466     string type;
467     vector<pair<string, int>> vars;
```
- Represents something like `int a, b, arr[10];`.
- **Line 466**: `type` — the shared declared type (`int`, `float`, ...).
- **Line 467**: `vars` — a list of `(variable_name, array_size)` pairs. For a plain scalar, `array_size` is `0`; for an array, it's the declared size (e.g., `("arr", 10)`).

```cpp
470     DeclNode(string t) : type(t) {}
471
472     void add_var(string name, int array_size = 0) {
473         vars.push_back(make_pair(name, array_size));
474     }
```
- `add_var` defaults `array_size` to `0` so plain variables can be added with just a name: `decl->add_var("a")`.

```cpp
476     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
477                         int& temp_count, int& label_count) const override {
478         for(int i = 0; i < vars.size(); i++)
479         {
480             if(vars[i].second == 0)
481             {
482                 outcode << "// Declaration: " << type << " " << vars[i].first << endl;
483             }
484             else
485             {
486                 outcode << "// Declaration: " << type << " " << vars[i].first << "[" << vars[i].second << "]" << endl;
487             }
488         }
489         return "";
490     }
```
- **Declarations don't produce executable TAC instructions** (they don't compute anything at runtime) — they only emit **comments** into `code.txt` for readability/documentation (matches lab requirement: "include comments to enhance readability"). `vars[i].second` is the array size: `0` → plain variable comment; non-zero → array variable comment with `[size]`.
- `.first`/`.second` access the two members of each `pair<string,int>` (`.first` = name, `.second` = array size).

```cpp
492     string get_type() const { return type; }
493     const vector<pair<string, int>>& get_vars() const { return vars; }
494 };
```
- Getters, presumably used elsewhere (e.g. by the parser/semantic analysis code, or possibly unused by this file but kept for interface completeness). Returning `const vector<...>&` (a reference) avoids copying the whole vector — efficient read-only access.

### `FuncDeclNode` — function declaration (lines 496–546)
```cpp
498 class FuncDeclNode : public ASTNode {
499 private:
500     string return_type;
501     string name;
502     vector<pair<string, string>> params;
503     BlockNode* body;
```
- Note: inherits directly from `ASTNode` (not `StmtNode` or `ExprNode`) — a function declaration is a **top-level program unit**, not an expression or a statement inside a block.
- `params` — list of `(paramType, paramName)` pairs.
- `body` — the function's `{ ... }` block.

```cpp
506     FuncDeclNode(string ret_type, string n) : return_type(ret_type), name(n), body(nullptr) {}
507     ~FuncDeclNode() { if (body) delete body; }
```
- Constructor initializes `body` to `nullptr` (set later via `set_body`).

```cpp
509     void add_param(string type, string name) {
510         params.push_back(make_pair(type, name));
511     }
512
513     void set_body(BlockNode* b) {
514         body = b;
515     }
```
- Two setters used by the parser while building this node incrementally (parameters are added one at a time as they're parsed; body is attached once the whole `{ }` block has been parsed).

```cpp
517     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
518                         int& temp_count, int& label_count) const override {
519         outcode << "// Function: " << return_type << " " << name << "(";
520         for(int i = 0; i < params.size(); i++)
521         {
522             outcode << params[i].first << " " << params[i].second;
523             if(i != params.size() - 1) outcode << ", ";
524         }
525         outcode << ")" << endl;
```
- **Lines 519–525**: Emit a **header comment** documenting the function signature, e.g. `// Function: int add(int a, int b)`. The loop writes each parameter as `type name`, and inserts a comma **between** parameters (checked via `i != params.size()-1` so the *last* parameter doesn't get a trailing comma).

```cpp
527         symbol_to_temp.clear();
```
- **Very important line.** Clears the symbol→temp map at the start of every new function. This is because **temp caching and variable identity are scoped per-function** — a local variable `a` in one function is unrelated to an `a` in a different function, so the map must be reset to avoid a stale/incorrect mapping leaking from a previous function into this one.

```cpp
529         for(int i = 0; i < params.size(); i++)
530         {
531             string temp = "t" + to_string(temp_count++);
532             outcode << temp << " = " << params[i].second << endl;
533             symbol_to_temp[params[i].second] = temp;
534             symbol_to_temp["_param_" + params[i].second] = "1";
535         }
```
- For **every parameter**, immediately (right at function entry) emit a line loading it into a temp, e.g. `t0 = a` for the first parameter named `a`. This models "parameters arrive already available as values" — the code eagerly materializes each parameter into its own temp up front.
- Line 533: Record in the map that parameter `a`'s value currently lives in that temp.
- Line 534: Set the special **marker key** `"_param_a" = "1"` — this is exactly what `VarNode::generate_code` checks at lines 59–62 to recognize `a` as a parameter and reuse its temp directly without re-emitting a load.

```cpp
537         if(body != nullptr)
538         {
539             body->generate_code(outcode, symbol_to_temp, temp_count, label_count);
540         }
541
542         outcode << endl;
543
544         return "";
545     }
546 };
```
- Generate the function body's code (recursively walks the whole block).
- Line 542: blank line after the function for readability/separation between functions in `code.txt`.

### `ArgumentsNode` — helper for call arguments (lines 548–580)
```cpp
550 class ArgumentsNode : public ASTNode {
551 private:
552     vector<ExprNode*> args;
553
554 public:
555     ~ArgumentsNode() {}
```
- A **helper/utility node used during parsing** to accumulate a comma-separated argument list (e.g., while parsing `f(a, b, c)`, the grammar might build an `ArgumentsNode` first, then transfer its expressions into a `FuncCallNode`).
- **Line 555**: Notice the destructor is **empty** — it does **NOT** delete the expressions inside `args`. This is intentional: `ArgumentsNode` is meant to be a **temporary staging container**; ownership of the actual `ExprNode*` pointers is transferred elsewhere (e.g., into a `FuncCallNode` via `add_argument`), so this class must **not** double-delete them.

```cpp
557     void add_argument(ExprNode* arg) {
558         if (arg) args.push_back(arg);
559     }
560
561     ExprNode* get_argument(int index) const {
562         if (index >= 0 && index < args.size()) {
563             return args[index];
564         }
565         return nullptr;
566     }
```
- `get_argument` — safe indexed access with **bounds checking**; returns `nullptr` instead of crashing if `index` is out of range.

```cpp
568     size_t size() const {
569         return args.size();
570     }
571
572     const vector<ExprNode*>& get_arguments() const {
573         return args;
574     }
```
- `size()` — how many arguments were collected.
- `get_arguments()` — returns a reference to the whole vector (e.g., so `FuncCallNode`'s constructor logic in the parser can loop through them all and transfer them).

```cpp
576     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
577                         int& temp_count, int& label_count) const override {
578         return "";
579     }
580 };
```
- Must implement `generate_code` because it's an `ASTNode` (pure virtual requirement), but this class is **never actually meant to generate code on its own** (it's just a temporary staging structure during parsing, never inserted into the "live" tree that gets traversed for code gen) — so it's a harmless no-op stub.

### `FuncCallNode` — function call expression (lines 582–624)
```cpp
584 class FuncCallNode : public ExprNode {
585 private:
586     string func_name;
587     vector<ExprNode*> arguments;
```
- Represents `foo(a, b)` used **as an expression** (it produces a value — the function's return value — so it correctly extends `ExprNode`, not `StmtNode`).

```cpp
590     FuncCallNode(string name, string result_type)
591         : ExprNode(result_type), func_name(name) {}
592
593     ~FuncCallNode() {
594         for (auto arg : arguments) {
595             delete arg;
596         }
597     }
598
599     void add_argument(ExprNode* arg) {
600         if (arg) arguments.push_back(arg);
601     }
```
- Unlike `ArgumentsNode`, this class **does** own its arguments and deletes them in its destructor — since `FuncCallNode` is the node that actually stays permanently in the AST and participates in code generation.

```cpp
603     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
604                         int& temp_count, int& label_count) const override {
605         for(int i = 0; i < arguments.size(); i++)
606         {
607             string arg_temp = arguments[i]->generate_code(outcode, symbol_to_temp, temp_count, label_count);
608             outcode << "param " << arg_temp << endl;
609         }
610
611         string temp = "t" + to_string(temp_count++);
612         outcode << temp << " = call " << func_name << ", " << arguments.size() << endl;
613         return temp;
614     }
```
- **Lines 605–609**: For each argument, first fully evaluate it into a temp, then emit a `param arg_temp` instruction — this pushes/declares it as one of the call's arguments (same convention seen in `PrintNode`). Arguments are emitted **in order** (left to right).
- **Lines 611–612**: After all `param` lines, emit a single `tN = call func_name, argCount` line — capturing the return value into a new temp, naming the function, and recording how many arguments were passed (needed by the callee to know how many `param`s to expect / for stack cleanup in a real compiler backend).
- **Line 613**: Return that temp so the call's result can be used in a larger expression (e.g. `x = foo(a,b) + 1`).

```cpp
616     ExprNode* clone() const override {
617         FuncCallNode* cloned = new FuncCallNode(func_name, node_type);
618         for(int i = 0; i < arguments.size(); i++)
619         {
620             cloned->add_argument(arguments[i]->clone());
621         }
622         return cloned;
623     }
624 };
```
- Deep-clones every argument individually and adds them to a fresh `FuncCallNode`.

### `ProgramNode` — root of the AST (lines 626–654)
```cpp
628 class ProgramNode : public ASTNode {
629 private:
630     vector<ASTNode*> units;
```
- The **top-level container** for the whole program — a list of top-level "units" (which in practice would be `FuncDeclNode`s, and possibly global `DeclNode`s).
- Declared as `vector<ASTNode*>` (base type) rather than a more specific type, so it can hold **any** kind of top-level construct uniformly.

```cpp
633     ~ProgramNode() {
634         for (auto unit : units) {
635             delete unit;
636         }
637     }
638
639     void add_unit(ASTNode* unit) {
640         if (unit) units.push_back(unit);
641     }
```
- Deleting `ProgramNode` cascades to delete every top-level unit, which cascades further down the tree — this is the **root of the ownership chain**: deleting the `ProgramNode` frees the *entire* AST.

```cpp
643     string generate_code(ofstream& outcode, map<string, string>& symbol_to_temp,
644                         int& temp_count, int& label_count) const override {
645         for(int i = 0; i < units.size(); i++)
646         {
647             if(units[i] != nullptr)
648             {
649                 units[i]->generate_code(outcode, symbol_to_temp, temp_count, label_count);
650             }
651         }
652         return "";
653     }
654 };
```
- Generates code for every top-level unit **in order** — this is the call that **kicks off the entire recursive traversal** of the whole AST (called from `ThreeAddrCodeGenerator::generate()` in `three_addr_code.h`).

```cpp
656 #endif // AST_H
```
- Closes the include guard opened at the top of the file.

---

## PART 3: `three_addr_code.h` — LINE BY LINE

```cpp
1  #ifndef THREE_ADDR_CODE_H
2  #define THREE_ADDR_CODE_H
3
4  #include "ast.h"
5  #include <fstream>
6  #include <string>
7  #include <map>
8
9  using namespace std;
```
- **Lines 1–2**: Include guard (same purpose as in `ast.h`).
- **Line 4**: Includes `ast.h` because this file needs `ProgramNode` and the whole AST hierarchy.
- **Lines 5–7**: `fstream`, `string`, `map` — needed for `ofstream&`, `string`, and `map<string,string>` used in this class (technically already pulled in transitively via `ast.h`, but included explicitly here too for clarity/self-containment — good practice).

```cpp
12 class ThreeAddrCodeGenerator {
13 private:
14     ProgramNode* ast_root;
15     ofstream& outcode;
16     map<string, string> symbol_to_temp;
17     int temp_count;
18     int label_count;
```
- This class is the **"driver"**: it doesn't generate code itself node-by-node — it just **owns the overall state** and kicks off traversal.
- **Line 14**: `ast_root` — pointer to the root `ProgramNode` of the whole tree (built earlier by the parser).
- **Line 15**: `ofstream& outcode` — a **reference** to the output file stream (`code.txt`, opened somewhere in the main program / driver code, e.g. `main.cpp`). It's a reference (not a copy) because file streams shouldn't/can't be copied, and we want this class to write to the *same* file the rest of the program is using.
- **Line 16**: `symbol_to_temp` — the map that gets threaded through the entire AST traversal (this is where it "lives"/is owned; individual node `generate_code` calls just receive it by reference and mutate it).
- **Lines 17–18**: `temp_count`, `label_count` — the running counters for temp/label numbering, starting at 0, owned centrally here and passed by reference into every `generate_code` call so the whole tree shares one continuous numbering sequence.

```cpp
20     ThreeAddrCodeGenerator(ProgramNode* root, ofstream& out)
21         : ast_root(root), outcode(out), temp_count(0), label_count(0) {}
```
- Constructor: takes the AST root and the output stream, stores the root pointer, **binds** the reference `outcode` to `out` (references must be initialized at construction — can't be reassigned later, which is why it's set here via the initializer list), and initializes both counters to `0` (so the first temp generated anywhere is always `t0`, first label is always `L0`).
- Note: this constructor does **not** take ownership of `ast_root` for deletion purposes — there's no destructor here that deletes `ast_root`, so whoever created the `ProgramNode` (likely `main`) is responsible for deleting it. `ThreeAddrCodeGenerator` merely **uses** it.

```cpp
23     void generate() {
24         outcode << "//========== THREE ADDRESS CODE ==========" << endl;
25         outcode << endl;
26         outcode << "// This code was generated by a two-pass compiler" << endl;
27         outcode << "// Format: " << endl;
28         outcode << "// - t0, t1, etc. are temporary variables" << endl;
29         outcode << "// - L0, L1, etc. are labels for jumps" << endl;
30         outcode << "// - Operations follow the three-address code format" << endl;
31         outcode << endl;
32         outcode << "// Three Address Code" << endl;
33         outcode << endl;
```
- **`generate()`** is the single **public entry point** called from `main` (or wherever the driver code lives) to produce the entire `code.txt` output.
- **Lines 24–33**: Write a **header block of comments** at the top of `code.txt` — a title banner, an explanatory note about the format (temps, labels, three-address format) — purely for **human readability** of the output file (matches the lab requirement that the output should be "well-formatted and include comments to enhance readability").

```cpp
35         if(ast_root != nullptr)
36         {
37             ast_root->generate_code(outcode, symbol_to_temp, temp_count, label_count);
38         }
```
- **The single most important line in this file.** This is where the **entire recursive AST traversal begins**:
  - Calls `generate_code` on the **root** `ProgramNode`.
  - Passes in `outcode` (so all nodes write into the same file), the (currently empty) `symbol_to_temp` map, and both counters starting at `0`.
  - Because all four of these are passed **by reference**, every single node anywhere in the deeply nested tree shares and mutates the **exact same** map and counters — this is what gives you a single continuous, correct `t0, t1, t2, ...` / `L0, L1, ...` numbering sequence across the whole program instead of each node "starting over."
  - Guarded by `if(ast_root != nullptr)` in case parsing failed or produced an empty tree (defensive check — avoids a null-pointer crash / segfault).

```cpp
40         outcode << endl;
41         outcode << "//========== END OF CODE ==========" << endl;
42     }
```
- After the whole tree has been traversed (i.e., **all** the code has already been written by the time we get back here, since the call on line 37 doesn't return until the whole recursive traversal is done), write a trailing **footer comment** to visually mark the end of the generated code.

```cpp
44     // You may add helper methods here
45 };
46
47 #endif // THREE_ADDR_CODE_H
```
- Line 44: A comment left by the lab skeleton, inviting you to add any extra utility functions to this class if needed (e.g., you might have added something here if your implementation needed extra bookkeeping — mention this if the examiner asks "did you add anything extra here?").
- Closing brace of the class, and closing the include guard.

---

## PART 4: HOW IT ALL FITS TOGETHER (the full call chain)

```
main() / driver code
   │
   │  1. Lexer + Parser run, building the AST bottom-up as grammar rules fire
   │     (e.g., "expression : variable ASSIGNOP logic_expression" creates an
   │      AssignNode combining the VarNode and the ExprNode already built)
   │
   │  2. Root ProgramNode is fully constructed (units = list of FuncDeclNodes)
   │
   ▼
ThreeAddrCodeGenerator gen(ast_root, code_txt_stream);
gen.generate();
   │
   │  writes header comments
   │  calls ast_root->generate_code(outcode, symbol_to_temp, temp_count, label_count)
   ▼
ProgramNode::generate_code()
   │  loops over units, for each FuncDeclNode calls generate_code()
   ▼
FuncDeclNode::generate_code()
   │  writes "// Function: ..." comment
   │  clears symbol_to_temp (fresh scope!)
   │  loads each parameter into a temp
   │  calls body->generate_code()  (body is a BlockNode)
   ▼
BlockNode::generate_code()
   │  loops over each statement, calling its generate_code()
   ▼
(IfNode / WhileNode / ForNode / DeclNode / ReturnNode / ExprStmtNode / PrintNode ...)
   │  each emits its own control-flow / declaration / etc. code,
   │  and recursively calls generate_code() on any expressions/sub-statements it holds
   ▼
(BinaryOpNode / UnaryOpNode / AssignNode / VarNode / ConstNode / FuncCallNode ...)
   │  each computes its sub-expressions first (recursively), then emits ONE
   │  instruction combining them into a new temp, and returns that temp's name
   │  up to its caller.
```

**Core recurring pattern across almost every node** (say this if the examiner asks "what's the general design pattern here?"):
> "Each node's `generate_code` first recursively generates code for its children (which emits their instructions and returns the temp holding their result), and then the node itself emits exactly one instruction that combines those children's results, allocates a new temp/label if needed, and returns its own result temp (or `""` for statements). This bottom-up, recursive tree walk is what naturally produces correctly-ordered three-address code from a nested AST."

---

## PART 5: LIKELY VIVA QUESTIONS & QUICK ANSWERS

| Question | Quick Answer |
|---|---|
| Why is `generate_code` pure virtual in `ASTNode`? | Forces every concrete node type to implement it; enables polymorphism so calling `node->generate_code()` runs the right version automatically based on the node's real type. |
| Why is the destructor `virtual` in `ASTNode`? | So `delete`ing an object through a base class pointer correctly calls the derived class's destructor too, avoiding memory leaks. |
| Why pass `temp_count`/`label_count`/`symbol_to_temp` by reference? | So all nodes across the recursive tree traversal share one continuous, mutually-consistent numbering/state instead of each node resetting to its own local copy. |
| Why is `symbol_to_temp` cleared in `FuncDeclNode`? | Because temp caching is scoped per function — a variable named `a` in one function is unrelated to `a` in another; stale mappings from a previous function must not leak in. |
| Why does `VarNode` sometimes NOT emit a new load instruction? | If the variable's value is already cached in `symbol_to_temp` (already loaded/assigned before) or it's a function parameter (loaded once at function entry), it just reuses the existing temp instead of reloading. |
| Why is `lhs` in `AssignNode` a `VarNode*` and not `ExprNode*`? | Because only a variable (plain or array-indexed) can legally appear on the left of `=` in C; using the specific type enforces this at compile time. |
| Why does `AssignNode` return `rhs_temp`? | Because assignment is an expression in C and evaluates to the assigned value (supports chained assignment like `a = b = 5`). |
| Why does `if`/`while`/`for` use `if X goto L` followed by `goto L2` (two lines) instead of one "if-false" jump? | TAC here only supports conditional jump on TRUE; expressing "else" requires an explicit fallback unconditional jump to the false branch. |
| Why does `WhileNode` put the condition check *inside* the loop (after `start_label`), unlike a simple linear sequence? | So the condition is **re-evaluated every iteration** — jumping back to `start_label` (not straight to the body) re-triggers the condition test each time. |
| How does `ForNode` differ from `WhileNode` in generated code? | `ForNode` additionally emits the `init` code once before the loop, and the `update` code once per iteration right after the body (before looping back) — modeling `for` as `init; while(cond){body; update;}`. |
| Why does `clone()` exist? | To create independent deep copies of expression sub-trees, needed when the same expression must be duplicated in two places in the tree (each owning its own copy, so no double-deletion). |
| Why does `ArgumentsNode`'s destructor NOT delete its arguments, but `FuncCallNode`'s does? | `ArgumentsNode` is a temporary staging structure during parsing — ownership of the expressions is transferred out (e.g. into a `FuncCallNode`) before the `ArgumentsNode` is discarded, so it must not double-free them. `FuncCallNode` is a permanent AST node that truly owns its arguments long-term. |
| What does `param` / `call func, N` mean in the output? | Standard TAC convention for function calls: each argument is pushed via a `param` instruction (in order), then a single `call` instruction names the function and how many arguments were passed; the result (if any) is captured into a new temp. |
| Why do `DeclNode`/comments not produce real instructions? | Declarations don't compute anything at runtime — they're just documentation of what variables exist, so only comments are emitted, matching the lab's readability requirement. |
| What happens if `temp_count`/`label_count` were passed by value instead of by reference? | Every node would see its own independent copy starting from whatever value was passed in; increments inside one node wouldn't be visible to sibling/parent nodes, causing **duplicate temp/label names** across the program — incorrect output. |
| Where does the actual AST get built? | In the modified Bison/Yacc parser (`.y` file) — grammar rule actions construct node objects (`new BinaryOpNode(...)`, `new AssignNode(...)`, etc.) and link them together as parsing proceeds, then attach them via `set_ast_node()`/`get_ast_node()` (mentioned in the lab handout example) up to the final root `ProgramNode`. |
| Why is code generation done in a *separate* class (`ThreeAddrCodeGenerator`) instead of directly in `main`? | Encapsulation/clean design — it bundles together the state needed for one full "compile a program" run (the map, counters, output stream, root pointer) as a single reusable object rather than loose global variables in `main`. |

---

*Tip for the viva: if the examiner points at any single line and asks "what's happening here", first identify (1) which class/node it's in, (2) whether it's an expression node (returns a temp) or statement node (returns `""`), and (3) whether the line is allocating a new temp/label, emitting an instruction, recursing into a child, or managing memory (constructor/destructor/clone). Walking through that checklist out loud covers almost every possible question on this file.*
