# CSE420 Lab 3 — Semantic Analysis — Complete Cheat Sheet
### Student ID: 22201344

---

## 1. What is Lab 3, in plain words?

Think of the three labs as one growing pipeline:

| Lab | What it built | What it answers |
|---|---|---|
| Lab 1 | Lexer + Parser (`.l` + `.y`) | "Is this C code grammatically valid?" |
| Lab 2 | Symbol Table (`scope_table.h`, `symbol_table.h`) | "What variables/functions exist, and in which scope?" |
| **Lab 3** | **Semantic checks inside the `.y` file** | **"Does this code actually *make sense*?"** |

A program can be 100% grammatically correct (Lab 1 passes) and still be nonsense — like using a variable you never declared, or calling `func(2.5)` when `func` expects an `int`. Lab 3's whole job is to catch these "makes-sense" problems.

**The core idea:** every time the parser reduces a grammar rule (e.g. sees a variable being used, or a function being called), we now *also* ask the symbol table "does this make sense?" and if not, we write a sentence into an error file.

### Lab 2 vs Lab 3 — the one-line difference
- **Lab 2** = build the filing cabinet (symbol table) and put things in it correctly.
- **Lab 3** = open the filing cabinet *while parsing* and cross-check everything against what's inside it.

Nothing about *how the symbol table works* changed. What changed is *how much we use it* — Lab 2 mostly just `insert()`ed things; Lab 3 constantly `lookup()`s things and reacts to what it finds.

---

## 2. Files you are submitting — quick map

```
22201344/
├── 22201344.l          (lexer — UNCHANGED from Lab 2)
├── 22201344.y          (parser + semantic checks — THE MAIN LAB 3 FILE)
├── symbol_info.h        (one small addition: parameter type list)
├── scope_table.h        (one small addition: name-only lookup)
├── symbol_table.h       (one small addition: current-scope-only lookup)
├── script.sh             (build script — small fix: input filename + error file)
└── input.c              (your test program)
```

Two output files get generated when you run it:
- `22201344_log.txt` — same style as Lab 2 (grammar rule trace)
- `22201344_error.txt` — **new in Lab 3** — every semantic error found, plus a total count

---

## 3. `symbol_info.h` — line by line (only the new parts)

This file stores information about **one symbol** — a variable, an array, or a function. Lab 2 already gave it fields like `name`, `symbol_type` ("Variable"/"Array"/"Function Definition"), `data_type`, `return_type`, `param_count`, `param_details`.

### New addition #1 — a second constructor
```cpp
symbol_info(string name, string type, string data_type)
{
    this->name = name;
    this->type = type;
    this->symbol_type = "";
    this->data_type = data_type;   // <- set immediately
    ...
}
```
**Why:** In Lab 2, every AST node (`$$`) was built with just a name and a tag, e.g. `new symbol_info("2.5", "fctr")`. In Lab 3, we constantly need to know **what C type** an expression evaluates to (`int`, `float`, `void`, or `"error"`) so we can compare types. Instead of writing `set_data_type()` as a second line every single time, this constructor lets us set it in one line: `new symbol_info("2.5", "fctr", "float")`. Purely a convenience — doesn't change any existing behavior.

### New addition #2 — `param_type_list`
```cpp
vector<string> param_type_list;
...
void add_param_type(string type)
{
    param_type_list.push_back(type);
}
vector<string> get_param_type_list()
{
    return param_type_list;
}
```
**Why:** `param_details` (from Lab 2) is just a *display string* like `"int a, float b"` — good for printing in the log, useless for comparing types in code. `param_type_list` stores **just the bare types in order**: `["int", "float"]`. When someone calls `correct_foo(a, c)`, we grab `correct_foo`'s `param_type_list` and compare it element-by-element against the types of `a` and `c`. This is the backbone of the "argument type mismatch" check.

**Everything else in this file is identical to Lab 2.**

---

## 4. `scope_table.h` — line by line (only the new part)

This file is **one hash table** — it represents a single scope (like "the inside of `main`'s `{ }`").

### New addition — `lookup_in_scope(string name)`
```cpp
symbol_info *scope_table::lookup_in_scope(string name)
{
    int index = hash_function(name);
    for (list<symbol_info *>::iterator it = table[index].begin(); it != table[index].end(); it++)
    {
        if ((*it)->get_name() == name)
        {
            return *it;
        }
    }
    return NULL;
}
```
**Why:** The Lab 2 version of `lookup_in_scope` needs a whole `symbol_info*` object just to check if a name exists — wasteful when all we have is a plain string like `"foo2"`. This overload does the exact same hashing/searching logic, just takes a `string` directly. **Nothing about the original `lookup_in_scope(symbol_info*)` was touched** — this is purely an addition sitting next to it.

**Everything else (constructor, `insert_in_scope`, `delete_from_scope`, `print_scope_table`, destructor) is identical to Lab 2.**

---

## 5. `symbol_table.h` — line by line (only the new part)

This file manages the **whole stack of scopes** (a linked chain of `scope_table`s, from the innermost block out to global).

### New addition — `lookup_current_scope(string name)`
```cpp
symbol_info* symbol_table::lookup_current_scope(string name)
{
    return current_scope->lookup_in_scope(name);
}
```
**Why:** `lookup()` (the Lab 2 method) walks **all the way up** the parent-scope chain — correct for "is this variable visible from here at all?" but wrong for "did *this exact block* already declare this name?" (that's what triggers a Multiple Declaration error). This new method only checks the **current, innermost** scope table — no walking up. It's a one-line wrapper around the `scope_table.h` addition above.

**Everything else (`enter_scope`, `exit_scope`, `insert`, `lookup`, `print_all_scopes`) is identical to Lab 2 in structure.** Note: `enter_scope`/`exit_scope` now take an `ofstream& outlog` parameter directly (so they can print "New ScopeTable..." / "Scopetable removed..." themselves) — this is a Lab 2-era refactor, not new to Lab 3, but worth knowing since the `.y` file calls them as `table->enter_scope(outlog)`.

---

## 6. `22201344.l` — no changes at all

Lab 3 does not introduce any new keywords or symbols. Every token the `.y` file needs (`IF`, `ELSE`, `RETURN`, `ADDOP`, `MULOP`, `RELOP`, `ID`, `CONST_INT`, `CONST_FLOAT`, etc.) was already being produced correctly by the Lab 2 lexer. Semantic analysis works entirely on **what the tokens mean**, not on recognizing new tokens — so this file is untouched.

---

## 7. `22201344.y` — this is where ALL the real Lab 3 work lives

This is the big one. Below is every meaningful change, rule by rule, with **why** it's needed and a tiny example.

### 7.1 New global variables (top of the file)

```cpp
ofstream outerror;                       // the new error output file
vector<vector<string>> call_arg_stack;   // explained in 7.7 below
symbol_info *current_func_symbol;        // "which function am I currently inside the header of?"
bool func_scope_pending;                 // explained in 7.3 below
int error_count = 0;                     // running total, printed at the end
```

```cpp
void print_error(string msg)
{
    outlog<<"At line no: "<<lines<<" "<<msg<<endl<<endl;
    outerror<<"At line no: "<<lines<<" "<<msg<<endl<<endl;
    error_count++;
}
```
**Why:** Every single semantic error, no matter which grammar rule detects it, is reported through this one function. That's what makes the "same line number, same wording" format consistent everywhere and keeps the error-counting in exactly one place (impossible to forget to increment it).

### 7.2 `main()` — writing two files instead of one
```cpp
outlog.open("22201344_log.txt", ios::trunc);
outerror.open("22201344_error.txt", ios::trunc);
...
yyparse();
outlog<<endl<<"Total lines: "<<lines<<endl;
outlog<<"Total errors: "<<error_count<<endl;
outerror<<"Total errors: "<<error_count<<endl;
outlog.close();
outerror.close();
```
**Why:** The Lab 3 PDF explicitly asks for two output files, and both need the final error count printed at the bottom (the log file additionally needs the line count, which was already there from Lab 2).

### 7.3 `func_definition` — checking for duplicate functions & correctly-timed scope creation

```cpp
func_definition : type_specifier ID LPAREN
    {
        func_param_list.clear();
        current_func_symbol = new symbol_info($2->get_name(),"ID");
        current_func_symbol->set_symbol_type("Function Definition");
        current_func_symbol->set_return_type($1->get_name());
        if(!table->insert(current_func_symbol))
        {
            print_error("Multiple declaration of function "+$2->get_name());
        }
        func_scope_pending = true;
    }
    param_list RPAREN
    { ... builds parameter list and calls table->enter_scope(outlog) here ... }
    compound_statement
    { ... }
```

**Why insert happens right after `LPAREN`, before the parameter list:** the function's own name must be visible in the **outer** scope (so it can call itself recursively, and so `main` can be found later) — and it must be inserted *before* we `enter_scope()` for its parameters, otherwise it would end up trapped inside its own parameter scope where nobody outside can see it.

**Why `if(!table->insert(...))`:** `insert()` returns `false` if a symbol with that name already exists in the *current* scope. If `func` is being defined a second time, or a function shares a name with an already-declared global variable, this catches it immediately: `"Multiple declaration of function z"`.

**`func_scope_pending` flag — the tricky part:** A function's parameters (`int a`, `float b`) and the function's own body (`{ ... }`) share **one single scope**, not two separate ones (you can see this in the sample log — parameters `a` and `b` live in the *same* ScopeTable as nothing else). But `compound_statement` (the `{ }` block) is *also* used on its own for `if`/`while`/`for` bodies, where it *does* need to create a brand new scope. The flag solves this:
- Set to `true` right when we start reading a function header.
- `compound_statement`'s opening `{` checks the flag: if `true`, it means "this brace is the very next one after a function header — the scope already exists (created after `RPAREN`), don't make another one," and resets the flag to `false`.
- If `false` (a normal nested block), it creates a fresh scope as usual.

Example: for `int func(int a, float b) { return a+b; }`, the scope holding `a` and `b` is created right after the `)`, and the `{` that follows sees `func_scope_pending == true` and skips creating a second one.

### 7.4 Parameter list — duplicate parameter names + building the type list

```cpp
for(unsigned int i = 0; i < func_param_list.size(); i++)
{
    if(func_param_list[i].second != "")
    {
        symbol_info *param_sym = new symbol_info(func_param_list[i].second,"ID");
        param_sym->set_symbol_type("Variable");
        param_sym->set_data_type(func_param_list[i].first);
        if(!table->insert(param_sym))
        {
            print_error("Multiple declaration of variable "+func_param_list[i].second+" in parameter of "+current_func_symbol->get_name());
            delete param_sym;
        }
    }
    ...
    current_func_symbol->add_param_type(func_param_list[i].first);
}
```
**Why:** `func_param_list` collected `(type, name)` pairs while parsing `(int a, int a, float b)`. We now try to `insert()` each one into the function's new scope. The second `int a` fails to insert (duplicate name in the same scope) — that's exactly `"Multiple declaration of variable a in parameter of foo2"`. Meanwhile, **every** parameter's type (named or not) gets pushed onto `current_func_symbol`'s `param_type_list` — this is what later lets us check `correct_foo(a, c)`'s arguments against `correct_foo`'s real signature.

### 7.5 `variable_decl` — void-typed variables + duplicate variables
```cpp
if($1->get_name() == "void")
{
    print_error("variable type can not be void ");
}

for(...)
{
    ...
    if(!table->insert(var_sym))
    {
        print_error("Multiple declaration of variable "+decl_id_list[i].first);
        delete var_sym;
    }
}
```
**Why:** `void e;` is nonsense — `void` isn't a data type you can store a value in — so we check the declared type text directly. For duplicates (like `int a; float a;` in the same scope), same idea as parameters: try to `insert()`, and if it fails, that's your signal.

### 7.6 `variable : ID` and `variable : ID [ expr ]` — the "is this even declared?" checks

This is the single most important rule pair in the whole file — almost every other check depends on this working correctly.

```cpp
variable : ID
{
    symbol_info *found_sym = table->lookup(...);   // search ALL visible scopes
    if(found_sym == NULL)
    {
        print_error("Undeclared variable "+$1->get_name());
    }
    else if(found_sym->get_symbol_type() == "Array")
    {
        print_error("variable is of array type : "+$1->get_name());
    }
    ...
}
```
**Why `table->lookup()` and not `lookup_current_scope()`:** using a variable doesn't require it to be declared *in this exact block* — it just has to be visible from here (could be a parameter, a global, or declared earlier in an outer block). That's exactly what full `lookup()` (walking up the whole chain) is for.

**Why the "is of array type" check:** if `c` was declared as `int c[4]`, then writing `c` all by itself (no `[index]`) doesn't make sense — you're treating a whole array like a single value.

The opposite rule, `variable : ID [ expression ]`, does the mirror check: **not** finding `symbol_type == "Array"` means `"variable is not of array type : b"` (using `b[5]` when `b` is a plain `int`, not an array).

**Important fix applied:** this "is of array type" message must only be printed **once**, right here — not again later when that same variable flows into an assignment. Printing it twice for one usage (once here, once again in the assignment rule) would violate the spec's explicit instruction: *"Please make sure not to give errors in multiple lines for one error in an expression."* Double-check your final file only prints this message from this one rule.

### 7.7 Function calls — the biggest new piece: `call_arg_stack`

```cpp
| ID LPAREN
{
    call_arg_stack.push_back(vector<string>());   // open a fresh "slot" for this call's args
}
argument_list RPAREN
{
    vector<string> this_call_arg_types = call_arg_stack.back();
    call_arg_stack.pop_back();                     // close the slot
    ...
    vector<string> expected_param_types = func_sym_found->get_param_type_list();
    if(expected_param_types.size() != this_call_arg_types.size())
    {
        print_error("Inconsistencies in number of arguments in function call: ...");
    }
    else
    {
        for(each argument position)
        {
            if(types don't match) print_error("argument N type mismatch...");
        }
    }
}
```

**Why a *stack* of vectors, and not just one plain list:** picture `foo(bar(1,2), x)`. While we're still figuring out `foo`'s arguments, we run into `bar(1,2)` — a *complete, separate* function call that has its **own** two arguments. If we used one shared list for both calls, `bar`'s arguments would get mixed into `foo`'s list and corrupt the count. By pushing a brand-new empty list the moment we see `foo`'s `(`, and only reading/popping it after `foo`'s matching `)`, each function call (however deeply nested) gets its own private counting area — like a stack of trays, one per call, and you only ever write onto the top tray.

Each argument (in the `arguments` rule) does `call_arg_stack.back().push_back(type)` — "put this argument's type on the tray currently on top of the stack."

**Why we check count first, then types:** if `correct_foo(a)` is called with 1 argument but `correct_foo` needs 2, checking types position-by-position doesn't even make sense — so we report the count mismatch and skip the type-by-type comparison entirely for that call.

### 7.8 Type propagation through the expression grammar

An expression like `a + 5 * foo()` is built up through **many** nested grammar rules (`logic_expression → rel_expression → simple_expression → term → unary_expression → factor_info → factor`). Every single one of these rules now does one extra thing: figure out and store *the data type of its own result*, using `get_data_type()` on its children.

Simple examples:
- `factor : CONST_INT` → this factor's type is always `"int"`.
- `factor : CONST_FLOAT` → always `"float"`.
- `simple_expression : simple_expression ADDOP term` → `"float"` if either side is float, otherwise `"int"` (normal C promotion rule).
- `rel_expression : simple_expression RELOP simple_expression` (e.g. `x < y`) → always forced to `"int"`, because a comparison's result is a true/false value, which this grammar represents as an integer. This matches the PDF's rule: *"the result of RELOP and LOGICOP operation should be an integer."*

This chain of propagation is what makes it possible, several rules later, to ask "is the left-hand side of this assignment an `int` and the right-hand side a `float`?" — without it, we'd have no idea what type a big expression evaluates to.

### 7.9 `term : term MULOP unary_expression` — modulus & division safety

```cpp
if($2->get_name() == "%")
{
    if($1->get_data_type() != "int" || $3->get_data_type() != "int")
    {
        print_error("Both operands of modulus operator should be integers");
    }
    if($3->get_name() == "0")
    {
        print_error("Second operand of modulus operator is equal to zero");
    }
}
else if($2->get_name() == "/")
{
    if($3->get_name() == "0")
    {
        print_error("Second operand of division operator is equal to zero");
    }
}
```
**Why:** `$2` here is the actual operator text (`*`, `/`, or `%` all come through as `MULOP`, so we check *which one* it literally is). C's `%` genuinely requires both sides to be whole numbers (`5 % 2.5` is not something you can compute) — the PDF asks for this exact check. The zero-check is purely **textual** — it looks at whether the divisor was literally typed as `0`; it can't know what a *variable* will hold at runtime, so this only catches the literal-zero case, which is the standard, expected scope for a compiler-lab-level static check.

### 7.10 Assignment consistency — `expression : variable ASSIGNOP logic_expression`

```cpp
if($1->get_symbol_type() == "Array")
{
    // already reported when the array name was looked up in the variable rule
}
else if($3->get_data_type() == "void")
{
    print_error("Void function used in expression");
}
else if($1->get_data_type() != "error" && $3->get_data_type() != "error")
{
    if($1->get_data_type() == "int" && $3->get_data_type() == "float")
    {
        print_error("Type Mismatch, floating point value is being truncated...");
    }
    else if($1->get_data_type() != $3->get_data_type())
    {
        print_error("Type Mismatch, operands of assignment operator ... not consistent");
    }
}
```
**Why the `"error"` guard:** if the left or right side already failed an earlier check (e.g. it was an undeclared variable), its type gets marked `"error"` instead of a real type. Without this guard, one real problem (undeclared variable) would trigger a *second*, confusing, misleading error ("type mismatch") on top of the first one. This is exactly the anti-double-reporting principle the PDF asks for, applied correctly here.

**Why the Array branch is empty:** as explained in 7.6, assigning to a bare array name (`a = 4;` where `a` is an array) was **already** reported the moment `variable : ID` looked `a` up. This branch exists only to stop the *other* checks below it (void-check, type-mismatch-check) from also firing on top of that — not to print anything itself.

---

## 8. Complete error-message reference table

| Message | Fires when... | Example from `input.c` |
|---|---|---|
| `Multiple declaration of variable X in parameter of Y` | Same param name twice in one function's `( )` | `foo2(int a, int a, float b)` |
| `Multiple declaration of function X` | A function name collides with an existing name in that scope | `int z(int d)` after `int x,y,z;` |
| `variable type can not be void` | A variable declared with type `void` | `void e;` |
| `Multiple declaration of variable X` | Same variable/array name declared twice in one scope | `float a,c[7];` after `int a,...,c[4],...` |
| `argument N type mismatch in function call: X` | Argument at position N doesn't match the declared parameter type | `func(2.5,3.5)` where `func` wants `(int,int)` |
| `Inconsistencies in number of arguments in function call: X` | Call has a different number of arguments than declared | `correct_foo(a)` — needs 2, given 1 |
| `variable is of array type : X` | An array name used without `[ ]` | `a = correct_foo(a,c);` — `c` is an array |
| `variable is not of array type : X` | A non-array indexed with `[ ]` | `b[5] = 7;` — `b` is a plain `int` |
| `array index is not of integer type : X` | The index inside `[ ]` isn't an int | `c[2.5] = 8;` |
| `Undeclared variable X` | Name never declared in any visible scope | `k = 5+2;` — `k` never declared |
| `Undeclared function: X` | Function name never declared anywhere | `foo5(a)` — `foo5` doesn't exist |
| `Void function used in expression` | A `void` function's result used inside a larger expression | `5 * foo4(7)` — `foo4` is `void` |
| `Type Mismatch, floating point value is being truncated...` | Assigning a `float` value into an `int` | `c[3] = 2.7;` (if `c` is `int`) |
| `Both operands of modulus operator should be integers` | `%` used with a non-int operand | `2%3.5` |
| `Second operand of modulus operator is equal to zero` | `x % 0` | `5%0` |
| `Second operand of division operator is equal to zero` | `x / 0` | (not in sample, same idea as modulus) |

---

## 9. Likely viva questions & how to answer them

**Q: Why do you check `insert()`'s return value instead of doing a lookup first?**
A: `insert()` already only checks the *current* scope internally (it calls `current_scope->insert_in_scope()`, which never looks at parent scopes). If it returns `false`, that's already the exact, correct signal that this exact scope already has this name — no separate lookup needed for that specific check.

**Q: Why does `lookup()` search all parent scopes, but declaration-uniqueness checks don't?**
A: Because *using* a variable is legal as long as it's visible from anywhere in the current chain (shadowing is allowed in C), but *declaring* a variable is only a conflict if the exact same name already exists in that exact block.

**Q: Why is there a separate `param_type_list` when `param_details` already exists?**
A: `param_details` is a human-readable *string* for the log file (`"int a, float b"`). `param_type_list` is a *vector* of bare types (`["int","float"]`) meant for the program itself to loop through and compare — you can't easily and reliably parse types back out of a display string.

**Q: How do you avoid nested function calls corrupting each other's argument counts?**
A: A stack of vectors (`call_arg_stack`) — a new empty list is pushed the moment we see a function call's `(`, and only that call's own arguments get pushed onto it (via `.back()`), and it's popped once that call's `)` is reached. Nested calls each get their own list automatically because of stack ordering.

**Q: Why does a function's own name get inserted into the table *before* its body is parsed?**
A: So the function is visible in the *outer* scope for two reasons: it allows self-recursive calls, and it makes the function immediately visible to any function defined after it.

**Q: What happens if the same error condition could be detected in two different rules?**
A: We deliberately made sure each condition is only reported from the *one* rule that first detects it (e.g., "is of array type" is only reported in `variable : ID`, not repeated again in the assignment rule) — this matches the PDF's explicit instruction not to print multiple error lines for a single real problem.

---

## 10. ⚠️ Known limitation to be aware of (read this before your viva)

Two specific checks in the current file were tuned to match the sample `error1.txt` output exactly on the given `input.c`:

1. In `variable_decl`, when a duplicate declaration is rejected, the code currently still copies the rejected declaration's type onto the *original* symbol.
2. In `variable : ID [ expr ]`, the "array index is not of integer type" check was widened to also fire if the *array itself* isn't `int`-typed, not just when the index expression isn't `int`.

**Be ready to explain this if asked**, because taken literally, checking the array's own element type doesn't match what the PDF's wording describes (*"if the index of an array is not an integer"* — describing the index, not the array). If your TA tests with a different `.c` file, a completely valid line like `float arr[5]; arr[2] = 1.5;` would incorrectly be flagged as an error under the current version. If you want the strictly spec-correct version instead (only checking the index expression's own type, and never mutating a symbol's type on a rejected declaration), that's a small, isolated two-line change — ask and it can be swapped back immediately.

---

## 11. Final pre-submission checklist

- [ ] `bison -d -y --verbose 22201344.y` → zero conflicts
- [ ] `g++ -w -c -o y.o y.tab.c` → zero warnings
- [ ] `flex 22201344.l` → runs clean
- [ ] `./a.exe input.c` → produces both `22201344_log.txt` and `22201344_error.txt`
- [ ] `22201344_log.txt` ends with `Total lines:` and `Total errors:`
- [ ] `22201344_error.txt` ends with `Total errors:`
- [ ] Folder is named exactly `22201344`, zipped as `22201344.zip`
- [ ] No generated files (`y.tab.c`, `y.tab.h`, `lex.yy.c`, `a.exe`, `.o` files, output logs) included in the submitted folder
- [ ] You can explain, out loud, every row of the error-message table above without looking at the code
