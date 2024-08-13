# System Configuration Files

All the configurable parameters of the system are set using _system configuration files_ (__*.scf__). These are plain text files, and they use the following basic syntax&mdash;formulated in EBNF:

```CONFIG
component ::= "[" identifier ("." identifier)* "]"
property ::= identifier "=" (constant | "{" option (";" option)* "}")
option ::= (Default | User)

Default ::= "DEFAULT" ":" definition
User ::= "USER" ":" definition

comment ::= "--" text
```

## Typical Uses

System components are identified by square brackets, and the settings of the component properties are specified between braces under that section.

The following table provides a few typical examples.

|Type|Examples|
|-|-|
|Component definition|```[system]```<br/>```[database]```<br/>```[database.tables]```|
|Property definition|```block_size = {SYSTEM: 4096; USER: 1024}```<br/>```users.count = {USER: 150}```<br/>```aligned = true```<br/>```cloud_use = {DEFAULT: Local}```<br/>```self_certificate = false```|

Each component or property has to be on a separate line, and line breaks are assumed to terminate the definition.

```CONFIG
-- Valid specification
[database]
table_count = 50
record_size = {DEFAULT: 1024; USER: 4096}

-- Invalid specification
[disks] block_size
= 2048
```

If a component specified does not exist or the value set for a property is not within a valid range or one of the predefined constants, the definition is ignored.

```CONFIG
[bicycles] -- The component doesn't exist
frizzles = {DEFAULT: yuppers; USER: honky-dory} -- The property doesn't exist, and invalid settings
```

## Valid Values

The following table enumerates the components that exist in the system and their properties along with the setting data types and allowable values. Each property can get a _default_ value which then can be overridden with a _user_ value, as stated in the above EBNF specification for options.

|Component|Property|Type|Acceptable Values|
|-|-|-|-|
|_system_|_id_|string|Any arbitrary identifier assigned by the user|
||_locale_|string|Valid locale settings are identical to those of all operating systems, e.g. _en-US_, _fr-FR_, _it-IT_, etc.|
||_cloud_use_|enumerated|Specifies whether the system will use cloud as storage. Can be either _Local_ or _Global_|
|_system.databases_|_count_|integer|The number of databases in the system|
||_backup_|boolean|Whether the system databases will be backed up|
||_auto_resize_|boolean|Whether the system databases will be resized automatically. If false, then the resize logic has to be specified with the next property|
||_resize_by_|integer|The resize value. Has to be a multiple of $2^n$ where $n\ge 8$|
|_database_|_id_|string|Any arbitrary identifier assigned by the user. Has to be the name of a specific database|
|||string|Any arbitrary identifier assigned by the user. Has to be the name of a specific database|
||_replicated_|boolean|Specifies whether the databases will be replicated on multiple sites|
||_users_|integer|The number of users that will be using the database|
|_database.tables_|_id_|string|Any arbitrary identifier for a specific table|
||_block_aligned_|boolean|Whether the table will be aligned on the disk for faster access. If _true_ is specificed the next value must also be set|
||_block_size_|integer|The block size to be used to align the records in the table. Must be a multiple of $2^n$ where $n\ge 8$|
