# Configuration File Reference Chart

The system configuration files have the __*.scf__ extension, and they use the following basic syntax:

```CONFIG
<parameter> ::= "["<identifier>"]" "=" <parameter-options>
<property> ::= "{"<identifier>"}" "=" <property-options>

<parameter-options> ::= (<Init> | <Default> | <User> | <System>)
<property-options> ::= (<Default> | <User>)

<Init> ::= "INIT" identifier
<Default> ::= "DEFAULT" identifier
<User> ::= "USER" identifier
<System> ::= "SYSTEM" identifier

<identifier> ::= <letter> | (<numbers> | <letters>)*
<letters> ::= <letter>+
<letter> ::= "a" .. "z" | "A" .. "Z"
<numbers> ::= <number>+
<number> ::= 0 .. 9
```

Below is a quick reference table detailing the syntax of the __*.scf__ files.

|Item|Purpose|Use|
|---|---|---|
|[\<_key_>]=\<_value_>|Parameter declaration and definition|[disk_size]=4096|
|{\<_key_>}=\<_value_>|Property declaration and definition|{block_aligned}=true|
