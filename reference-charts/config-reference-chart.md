# System Configuration Files

System configuration files (__*.scf__) use the following basic syntax&mdash;expressed in EBNF:

```CONFIG
component ::= "[" identifier "]"
property ::= "{" identifier "=" option (";" option)* "}"
option ::= (Default | User | Disabled)

Default ::= "DEFAULT" ":" definition
User ::= "USER" ":" definition
Disabled ::= "DISABLED"

comment ::= ";" text
```

## Typical Uses

System components are identified by square brackets, and the settings of the component properties are specified between braces under that section.

The following table provides a few typical examples.

|Type|Examples|
|-|-|
|Component definition|```[system]```<br/>```[database]```|
|Property definition|```{blocksize = SYSTEM: 4096; USER: 1024}```<br/>```{user_count = DEFAULT: 50; USER: 150}```<br/>```{disks_aligned = true}```<br/>```{cloud_use = DEFAULT: Local}```<br/>```{self_certificate_use = DISABLED}```|
