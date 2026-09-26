# Kozmos Language Reference

The following chart provides a quick reference for __Kozmos__ syntax, operators, and built-in constructs.

> __Note:__ Kozmos is a fictitious language. This is a portfolio sample.

## Language grammar (EBNF)

The grammar uses W3C-style EBNF: `::=` defines a rule, quoted text is literal, `[...]` is a character class, and `?`, `*`, and `+` mean *optional*, *zero or more*, and *one or more*. The grammar describes structure only; operator precedence is not encoded in it.

```text
program         ::= (statement | function-def | type-def)*
statement       ::= declaration | assignment | control-flow | expression
declaration     ::= "var" identifier ":" type (":=" expression)?
assignment      ::= lvalue assign-op expression
assign-op       ::= ":=" | ":" binary-op "="
lvalue          ::= identifier | array-access | field-access | list-pattern

control-flow    ::= if-stmt | while-stmt | for-stmt | match-stmt | return-stmt
                  | try-stmt | throw-stmt
if-stmt         ::= "if" expression "then" statement* ("else" statement*)? "end"
while-stmt      ::= "while" expression "do" statement* "end"
for-stmt        ::= "for" identifier "in" expression "do" statement* "end"
match-stmt      ::= "match" expression ("case" pattern "=>" statement*)+ "end"
return-stmt     ::= "return" expression?
try-stmt        ::= "try" statement* "catch" identifier statement* "end"
throw-stmt      ::= "throw" expression

function-def    ::= "fn" identifier type-params? "(" parameter-list? ")" (":" type)?
                    statement* "end"
function-sig    ::= "fn" identifier type-params? "(" parameter-list? ")" (":" type)?
parameter-list  ::= parameter ("," parameter)*
parameter       ::= identifier ":" type

type-def        ::= "trait" identifier type-params? (":" trait-constraint)? function-sig* "end"
                  | "record" identifier type-params? (":" trait-constraint)?
                    (identifier ":" type)* function-def* "end"
type-params     ::= "<" type-param ("," type-param)* ">"
type-param      ::= identifier (":" trait-constraint)?
trait-constraint::= identifier ("&" identifier)*
type            ::= primitive-type | generic-type | named-type
primitive-type  ::= "Int" | "Float" | "String" | "Bool" | "Nil"
generic-type    ::= identifier "<" type ("," type)* ">"
named-type      ::= identifier

expression      ::= lambda | unary-op expression | expression binary-op expression
                  | postfix-expr
lambda          ::= "|" (identifier ("," identifier)*)? "|" expression
unary-op        ::= "not" | "-" | "~"
binary-op       ::= "+" | "-" | "*" | "/" | "div" | "mod" | "**"
                  | "=" | "<>" | "<" | ">" | "<=" | ">=" | "in"
                  | "and" | "or" | "xor" | "eqv" | "imp"
                  | "&" | "|" | "!" | "<<" | ">>" | "++" | "::"
postfix-expr    ::= primary | array-access | slice | field-access | call-expr
array-access    ::= postfix-expr "[" expression "]"
slice           ::= postfix-expr "[" expression ".." expression "]"
field-access    ::= postfix-expr "." identifier
call-expr       ::= postfix-expr "(" (expression ("," expression)*)? ")"
primary         ::= literal | identifier | "(" expression ")"
                  | "[" (expression ("," expression)*)? "]"
                  | "[" expression ".." expression "]"

pattern         ::= literal | identifier | "_" | list-pattern
                  | identifier "(" pattern ("," pattern)* ")"
list-pattern    ::= "{" pattern ":" pattern "}"
literal         ::= integer | float | string | "True" | "False" | "Nil"
                  | "+Inf" | "-Inf" | "NaN"
integer         ::= [0-9]+
float           ::= [0-9]+ "." [0-9]+
string          ::= '"' [^"]* '"'
identifier      ::= [A-Za-z_] [A-Za-z0-9_]*
```

## Operators

### Arithmetic

| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| Addition | `+` | `a + b` | Numeric addition |
| Subtraction | `-` | `a - b` | Numeric subtraction |
| Multiplication | `*` | `a * b` | Numeric multiplication |
| Division | `/`, `div` | `a / b`, `a div b` | Float division, integer division |
| Modulus | `mod` | `a mod b` | Remainder |
| Power | `**` | `a ** b` | Exponentiation |
| Minimum/maximum | `min`, `max` | `min(a, b)`, `max(a, b, c)` | Built-in functions |

### Comparison

| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| Equal | `=` | `a = b` | Equality test |
| Not equal | `<>` | `a <> b` | Inequality test |
| Less than | `<` | `a < b` | Ordering comparison |
| Greater than | `>` | `a > b` | Ordering comparison |
| Less than or equal | `<=` | `a <= b` | Ordering comparison |
| Greater than or equal | `>=` | `a >= b` | Ordering comparison |

### Logical

| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| AND | `and` | `a and b` | Logical conjunction |
| OR | `or` | `a or b` | Logical disjunction |
| NOT | `not` | `not a` | Logical negation |
| XOR | `xor` | `a xor b` | Exclusive or |
| Equivalence | `eqv` | `a eqv b` | Logical equivalence |
| Implication | `imp` | `a imp b` | Logical implication |

### Bitwise

| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| Bitwise AND | `&` | `a & b` | Binary AND |
| Bitwise OR | `\|` | `a \| b` | Binary OR |
| Bitwise XOR | `!` | `a ! b` | Binary XOR |
| Bitwise NOT | `~` | `~a` | Binary complement |
| Left shift | `<<` | `a << b` | Shift bits left |
| Right shift | `>>` | `a >> b` | Shift bits right |

> __Note:__ __Kozmos__ does __not__ support operator *overloading*. Instead, it supports operator *extension*: an operator can be extended for a `record` or a `trait` only if the extended expression reduces to one of the operator's built-in uses.

### Assignment

| Category | Syntax | Example | Description |
|----------|--------|---------|-------------|
| __Declaration__ | `var name: Type := value` | `var x: Int := 42` | Declare a variable, optionally with an initial value |
| __Simple__ | `:=` | `x := 42` | Assign to an existing variable |
| __Compound__ | `:+=`, `:*=`, and so on | `x :+= 5`, `count :*= 2` | Apply a binary operator, then assign |
| __Array element__ | `name[index] :=` | `arr[i] := value` | Assign to an array element |
| __List pattern__ | `{head:tail} :=` | `{h:t} := mylist` | Destructure a list into its head and tail |

## Control flow statements

| Statement | Syntax | Example |
|-----------|--------|---------|
| __If-then-else__ | `if cond then ... else ... end` | `if x > 0 then print("positive") end` |
| __While loop__ | `while cond do ... end` | `while i < 10 do i := i + 1 end` |
| __For loop__ | `for name in iterable do ... end` | `for x in [1..10] do print(x) end` |
| __Pattern match__ | `match expr case pattern => ... end` | `match x case 0 => "zero" case _ => "other" end` |
| __Return__ | `return expr?` | `return x + y`, `return` |

## Function definition

| Element | Syntax | Example |
|---------|--------|---------|
| __Basic function__ | `fn name(params): Type ... end` | `fn add(a: Int, b: Int): Int return a + b end` |
| __No parameters__ | `fn name() ... end` | `fn hello() print("Hello!") end` |
| __No return type__ | `fn name(params) ... end` | `fn process(data: String) print(data) end` |
| __Generic function__ | `fn name<T: Trait>(params) ... end` | `fn largest<T: Ord>(items: Array<T>): T ... end` |
| __Lambda__ | `\|params\| expr` | `map(\|x\| x * 2, numbers)` |

## Built-in constants

| Category | Constant | Type | Description |
|----------|----------|------|-------------|
| __Numeric__ | `+Inf` | Float | Positive infinity |
| | `-Inf` | Float | Negative infinity |
| | `NaN` | Float | Not a number |
| | `PI` | Float | π (3.14159...) |
| | `E` | Float | Euler's number (2.71828...) |
| __Boolean__ | `True` | Bool | Boolean true value |
| | `False` | Bool | Boolean false value |
| __Reference__ | `Nil` | Nil | Empty reference; assignable to any type |
| __String__ | `""` | String | Empty string literal |

## Data types and structures

| Type | Declaration | Example | Description |
|------|-------------|---------|-------------|
| __Primitives__ | `Int`, `Float`, `String`, `Bool` | `var x: Int := 42` | Basic data types |
| __Array__ | `Array<T>` | `var numbers: Array<Int> := [1, 2, 3]` | Fixed-size, indexed collection |
| __List__ | `List<T>` | `var items: List<String> := ["a", "b"]` | Growable linked list |
| __Map__ | `Map<K, V>` | `var lookup: Map<String, Int>` | Key-value hash table |
| __Set__ | `Set<T>` | `var unique: Set<Int>` | Collection of unique values |
| __Queue__ | `Queue<T>` | `var tasks: Queue<String>` | FIFO queue |
| __Heap__ | `Heap<T: Ord>` | `var priority: Heap<Int>` | Min-heap (element type must implement `Ord`) |
| __Range__ | `[start..end]` | `[1..10]`, `[0..n]` | Inclusive integer sequence |

> __Note:__ __Kozmos__ supports *generics*: records, traits, and functions can declare type parameters. A type parameter can be unconstrained (`<T>`), constrained by one trait (`<T: Ord>`), or constrained by several traits, in which case the type must implement *all* of them (an *intersection*, written with `&`), for example `<T: Ord & Sync>`. Constraints can use the built-in root traits, such as `Eq`, `Ord`, and `Sync`, or user-defined traits.

## Data structure operations

### Array operations

Arrays have a fixed size. Operations that combine arrays return a new array.

| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| __Indexing__ | `arr[i]` | `numbers[0]` | Access an element by index |
| __Slicing__ | `arr[i..j]` | `numbers[1..2]` | Return a new subarray |
| __Length__ | `len(arr)` | `len(numbers)` | Number of elements |
| __Concatenation__ | `arr1 ++ arr2` | `[1, 2] ++ [3, 4]` | Return a new, joined array |
| __Contains__ | `item in arr` | `5 in numbers` | Check membership |

### List operations

| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| __Head__ | `{head:_}` | `{h:_} := mylist` | Get the first element |
| __Tail__ | `{_:tail}` | `{_:t} := mylist` | Get the remaining elements |
| __Prepend__ | `item :: list` | `1 :: [2, 3, 4]` | Add to the front |
| __Append__ | `list ++ [item]` | `mylist ++ [3]` | Add to the end |
| __Empty check__ | `isEmpty(list)` | `isEmpty(mylist)` | Test whether the list is empty |

### Map operations

| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| __Get__ | `map[key]` | `users["john"]` | Retrieve a value |
| __Set__ | `map[key] := value` | `users["jane"] := 25` | Store a key-value pair |
| __Has key__ | `key in map` | `"john" in users` | Check whether a key exists |
| __Remove__ | `delete(map, key)` | `delete(users, "john")` | Remove an entry |
| __Keys__ | `keys(map)` | `keys(users)` | Get all keys |
| __Values__ | `values(map)` | `values(users)` | Get all values |

### String operations

| Operation | Syntax | Example | Description |
|-----------|--------|---------|-------------|
| __Length__ | `len(str)` | `len("hello")` | String length |
| __Concatenation__ | `str1 ++ str2` | `"hello" ++ "world"` | Join strings |
| __Substring__ | `str[i..j]` | `"hello"[1..3]` | Extract a substring |
| __Contains__ | `substr in str` | `"ell" in "hello"` | Substring search |
| __Split__ | `split(str, delim)` | `split("a,b,c", ",")` | Split into an array |

## Error handling

| Construct | Syntax | Example |
|-----------|--------|---------|
| __Try-catch__ | `try ... catch err ... end` | `try risky() catch e print(e) end` |
| __Throw__ | `throw error` | `throw "Invalid input"` |
| __Option type__ | `Some(value)`, `None` | `var result: Option<Int> := Some(42)` |
| __Result type__ | `Ok(value)`, `Err(error)` | `var parsed: Result<Int, String> := Ok(7)` |
