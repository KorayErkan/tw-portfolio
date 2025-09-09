# __Kozmos__ Language Reference

The following chart provides quick reference for __Kozmos__ syntax, operators, and built-in constructs.

## Language Grammar (EBNF)

<pre id=ebnf-text>
program       ::= (statement | function-def | type-def)*
statement     ::= assignment | control-flow | expression | declaration
assignment    ::= lvalue ":=" expression | lvalue ":<operator>=" expression
lvalue        ::= identifier | array-access | field-access
control-flow  ::= if-stmt | while-stmt | for-stmt | match-stmt | return-stmt
expression    ::= logical-expr | arithmetic-expr | comparison-expr | call-expr
declaration   ::= "var" identifier ":" type ("=" expression)?

if-stmt       ::= "if" expression "then" statement* ("else" statement*)? "end"
while-stmt    ::= "while" expression "do" statement* "end"  
for-stmt      ::= "for" identifier "in" expression "do" statement* "end"
match-stmt    ::= "match" expression ("case" pattern "=>" statement*)+ "end"
return-stmt   ::= "return" expression?

function-def  ::= "fn" identifier "(" parameter-list? ")" (":" type)? statement* "end"
parameter-list::= parameter ("," parameter)*
parameter     ::= identifier ":" type

type-def      ::= "trait" identifier trait-body "end" | "record" identifier record-body "end"
type          ::= primitive-type | generic-type | trait-type
primitive-type::= "Int" | "Float" | "String" | "Bool" | "Nil"
generic-type  ::= identifier "<" type-list ">"
trait-type    ::= identifier (":" trait-constraint)?
</pre>

## Operators

### Arithmetic & Mathematical

| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| Addition | `+` | `a + b` | Numeric addition |
| Subtraction | `-` | `a - b` | Numeric subtraction |  
| Multiplication | `*` | `a * b` | Numeric multiplication |
| Division | `/`, `div` | `a / b`, `a div b` | Float/integer division |
| Modulus | `mod` | `a mod b` | Remainder operation |
| Power | `**` | `a ** b` | Exponentiation |
| Min/Max | `min`, `max` | `min(a, b)`, `max(a, b, c)` | Extrema functions |

### Comparison & Relational

| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| Equal | `=` | `a = b` | Equality test |
| Not Equal | `<>` | `a <> b` | Inequality test |
| Less Than | `<` | `a < b` | Numeric comparison |
| Greater Than | `>` | `a > b` | Numeric comparison |
| Less/Equal | `<=` | `a <= b` | Numeric comparison |
| Greater/Equal | `>=` | `a >= b` | Numeric comparison |

### Logical & Boolean

| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| AND | `and` | `a and b` | Logical conjunction |
| OR | `or` | `a or b` | Logical disjunction |
| NOT | `not` | `not a` | Logical negation |
| XOR | `xor` | `a xor b` | Exclusive or |
| Equivalence | `eqv` | `a eqv b` | Logical equivalence |
| Implication | `imp` | `a imp b` | Logical implication |

### Bitwise Operations

| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| Bitwise AND | `&` | `a & b` | Binary AND |
| Bitwise OR | `\|` | `a \| b` | Binary OR |
| Bitwise XOR | `!` | `a ! b` | Binary XOR |
| Bitwise NOT | `~` | `~a` | Binary complement |
| Left Shift | `<<` | `a << b` | Shift bits left |
| Right Shift | `>>` | `a >> b` | Shift bits right |

## Assignment Operators

| Category | Syntax | Example | Description |
|----------|--------|---------|-------------|
| **Simple** | `:=` | `x := 42` | Basic assignment |
| **Compound** | `:+=`, `:*=`, etc. | `x :+= 5`, `count :*= 2` | Operation + assignment |
| **Array Element** | `[index] :=` | `arr[i] := value` | Array element assignment |
| **List Pattern** | `{head:tail} :=` | `{h:t} := mylist` | Pattern-based assignment |

## Control Flow Statements

| Statement | Syntax | Example |
|-----------|--------|---------|
| **If-Then-Else** | `if cond then ... else ... end` | `if x > 0 then print("positive") end` |
| **While Loop** | `while cond do ... end` | `while i < 10 do i := i + 1 end` |
| **For Loop** | `for var in iterable do ... end` | `for x in [1..10] do print(x) end` |
| **Pattern Match** | `match expr case pattern => ... end` | `match x case 0 => "zero" case _ => "other" end` |
| **Return** | `return expr?` | `return x + y`, `return` |

## Function Definition

| Element | Syntax | Example |
|---------|--------|---------|
| **Basic Function** | `fn name(params) ... end` | `fn add(a: Int, b: Int): Int a + b end` |
| **No Parameters** | `fn name() ... end` | `fn hello() print("Hello!") end` |
| **No Return Type** | `fn name(params) ... end` | `fn process(data: String) print(data) end` |
| **Lambda** | `\|params\| expr` | `map(\|x\| x * 2, numbers)` |

## Built-in Constants

| Category | Constant | Type | Description |
|----------|----------|------|-------------|
| **Numeric** | `+Inf` | Float | Positive infinity |
| | `-Inf` | Float | Negative infinity |
| | `NaN` | Float | Not a number |
| | `PI` | Float | π constant (3.14159...) |
| | `E` | Float | Euler's number (2.71828...) |
| **Boolean** | `True` | Bool | Boolean true value |
| | `False` | Bool | Boolean false value |
| **Reference** | `Nil` | Any | Null/empty reference |
| **String** | `""` | String | Empty string literal |

## Data Types & Structures

| Type | Declaration | Example | Description |
|------|-------------|---------|-------------|
| **Primitives** | `Int`, `Float`, `String`, `Bool` | `x: Int := 42` | Basic data types |
| **Array** | `Array<T>` | `numbers: Array<Int>` | Fixed-size ordered collection |
| **List** | `List<T>` | `items: List<String>` | Linked list structure |
| **Map** | `Map<K -> V>` | `lookup: Map<String -> Int>` | Key-value hash table |
| **Set** | `Set<T>` | `unique: Set<Int>` | Unique value collection |
| **Queue** | `Queue<T>` | `tasks: Queue<String>` | FIFO data structure |
| **Heap** | `Heap<T>` | `priority: Heap<Int>` | Min/max heap structure |
| **Range** | `[start..end]` | `[1..10]`, `[a..z]` | Sequence range |

> <span id="note-byline"></span> __Kozmos__ does not support general-purpose *generics*. Instead, it has *trait compliance* where the type parameter has to be with one of the built-in root traits such as `Eq`, `Ord`, `Sync`, etc., or a user designed trait that implements those root traits.
> In a data structure declaration, the type parameter has to be a known trait, e.g. `<Ord>`; a descendant of a trait, e.g. `<T: Ord>`; or a descendant of multiple traits (i.e. a *union* of them), e.g. `<T: Ord | Sync>`.

## Data Structure Operations

### Array Operations
| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| **Indexing** | `arr[i]` | `numbers[0]` | Access element by index |
| **Slicing** | `arr[i..j]` | `text[1..5]` | Extract subarray |
| **Length** | `len(arr)` | `len(numbers)` | Get array size |
| **Concatenation** | `arr1 ++ arr2` | `[1,2] ++ [3,4]` | Join arrays |
| **Append** | `arr ++ [item]` | `nums ++ [5]` | Add single element |
| **Contains** | `item in arr` | `5 in numbers` | Check membership |

### List Operations  
| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| **Head** | `{head:_}` | `{h:_} := mylist` | Get first element |
| **Tail** | `{_:tail}` | `{_:t} := mylist` | Get remaining elements |
| **Prepend** | `item :: list` | `1 :: [2,3,4]` | Add to front |
| **Append** | `list ++ [item]` | `[1,2] ++ [3]` | Add to end |
| **Empty Check** | `isEmpty(list)` | `isEmpty(mylist)` | Test if empty |

### Map Operations
| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| **Get** | `map[key]` | `users["john"]` | Retrieve value |
| **Set** | `map[key] := value` | `users["jane"] := 25` | Store key-value |
| **Has Key** | `key in map` | `"john" in users` | Check key exists |
| **Remove** | `delete(map, key)` | `delete(users, "john")` | Remove entry |
| **Keys** | `keys(map)` | `keys(users)` | Get all keys |
| **Values** | `values(map)` | `values(users)` | Get all values |

### String Operations
| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| **Length** | `len(str)` | `len("hello")` | String length |
| **Concatenation** | `str1 ++ str2` | `"hello" ++ "world"` | Join strings |
| **Substring** | `str[i..j]` | `"hello"[1..3]` | Extract substring |
| **Contains** | `substr in str` | `"ell" in "hello"` | Substring search |
| **Split** | `split(str, delim)` | `split("a,b,c", ",")` | Split to array |

## Error Handling

| Construct | Syntax | Example |
|-----------|--------|---------|
| **Try-Catch** | `try ... catch err ... end` | `try risky() catch e print(e) end` |
| **Throw** | `throw error` | `throw "Invalid input"` |
| **Option Type** | `Some(value)`, `None` | `result: Option<Int> := Some(42)` |
| **Result Type** | `Ok(value)`, `Err(error)` | `parse: Result<Int, String>` |

> <span id="note-byline"></span> __Kozmos__ does __not__ support operator *overloading*. Instead, it supports operator *extension*: operators can be extended for a certain type (i.e. a `record`, a `trait`, or a `class`) only on the condition that the expression reduces to one of the built-in uses.
