# System Configuration Files

The system configuration files (__*.scf__) use the following basic syntax&mdash;expressed in EBNF:

```CONFIG
parameter ::= "[" identifier "=" (option | "{" property "}" "]")+
option ::= (Default | System | User)
property ::= identifier ":" option+

Default ::= "DEFAULT" ":" definition
System ::= "SYSTEM" ":" definition
User ::= "USER" ":" definition

definition ::= (String | Integer | Boolean)
identifier ::= letter | (number | letter)*

String ::= (letter | number)+
Integer ::= number+
Boolean ::= (true | false)

letter ::= "a" .. "z" | "A" .. "Z"
number ::= 0 .. 9
```

## Reference Chart

Below you can find the details of the typical uses of __*.scf__ entries.

|Item|Purpose|Typical Use|
|-|-|-|
|[_identifier_ = _value_]|Parameter declaration|[block_size = 4096]|
|||[default_user_count = 100|
|{_identifier_ = _value_}|Property declaration|{block_aligned = true}|
|||{cloud_use = DEFAULT: Local; USER: Local}|
|<_identifier_ = _value_>|Option definition|<owner = "Hijack_Inc">|
