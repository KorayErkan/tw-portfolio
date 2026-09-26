# Nordvale Server Configuration File Reference

All configurable parameters of Nordvale Server are set in _system configuration files_ (__*.scf__) in `C:\Program Files\Nordvale\config\`; the seat provisioning settings are in `prov_config.scf` in `C:\Program Files\Nordvale\users\`. These are plain text files with the syntax described below.

> __Note:__ Nordvale and all hostnames in this document are fictitious. This is a portfolio sample.

## Grammar

The grammar uses W3C-style EBNF: `::=` defines a rule, quoted text is literal, `[...]` is a character class (`[^...]` excludes the listed characters), `#x9`, `#xA`, and `#xD` are the tab, line feed, and carriage return characters, and `?`, `*`, and `+` mean _optional_, _zero or more_, and _one or more_. Sequence binds more tightly than alternation (`|`), so `a b | c` means `(a b) | c`.

```text
config-file    ::= (component | comment | blank-line)*
component      ::= ws* "[" identifier ("." identifier)* "]" ws* newline
                   (property | comment | blank-line)*
property       ::= ws* identifier ws* "=" ws* value ws* newline

value          ::= complex-value | simple-value
complex-value  ::= "{" ws* option (ws* ";" ws* option)* ws* "}"
option         ::= option-type ws* ":" ws* simple-value
option-type    ::= "DEFAULT" | "USER" | "ADMIN" | "SYSTEM"

simple-value   ::= boolean | number | host | file-path | constant | string
boolean        ::= "true" | "false" | "yes" | "no" | "on" | "off"
number         ::= integer | float | size-value | time-value
integer        ::= [0-9]+
float          ::= [0-9]+ "." [0-9]+
size-value     ::= integer ("KB" | "MB" | "GB" | "TB")
time-value     ::= integer ("ms" | "s" | "m" | "h" | "d")

host           ::= ip-address | host-name
ip-address     ::= octet "." octet "." octet "." octet
octet          ::= [0-9] [0-9]? [0-9]?
host-name      ::= label ("." label)*
label          ::= [A-Za-z0-9] ([A-Za-z0-9-]* [A-Za-z0-9])?

file-path      ::= bare-path | '"' drive ":\" [^"#xA#xD]* '"'
bare-path      ::= drive ":\" (segment ("\" segment)*)?
drive          ::= [A-Za-z]
segment        ::= [^\/:*?"<>| #x9#xA#xD]+

constant       ::= [A-Za-z_] [A-Za-z0-9_.]*
string         ::= '"' [^"#xA#xD]* '"' | bare-word
bare-word      ::= [A-Za-z0-9_./+-]+

identifier     ::= [A-Za-z_] [A-Za-z0-9_]*
comment        ::= ws* "--" [^#xA#xD]* newline
blank-line     ::= ws* newline
newline        ::= #xA | #xD #xA
ws             ::= " " | #x9
```

Several alternatives of `simple-value` can match the same text; for example, `true` is both a `boolean` and a `constant`, and `127.0.0.1` is both an `ip-address` and a `host-name`. The __Type__ column of the [configuration reference](#configuration-reference) determines how the value of each property is read.

Quote a string or file path if it contains spaces, for example `"C:\Program Files\Nordvale\certs\server.crt"`. Unquoted values end at the first space.

## Typical uses

A component header in square brackets starts a component. The properties that follow, one per line, belong to that component until the next header. Braces are used only for _complex values_, which set a different value for each option type (`DEFAULT`, `USER`, `ADMIN`, `SYSTEM`).

| Type | Examples |
|------|----------|
| __Component header__ | `[system]`, `[database]`, `[network]`, `[security]` |
| __Nested component__ | `[database.tables]`, `[network.ssl]`, `[security.auth]` |
| __Simple properties__ | `debug_mode = false`, `port = 8443`, `timeout = 30s` |
| __Complex property__ | `max_memory = {DEFAULT: 512MB; USER: 1GB; ADMIN: 2GB}` |
| __File paths__ | `temp_dir = C:\temp`, `cert_file = "C:\Program Files\Nordvale\certs\server.crt"` |
| __Host addresses__ | `bind_address = 127.0.0.1`, `host = db01.corp.example` |
| __Enumerated constant__ | `protocol = TLS1.3`, `compression = lz4`, or qualified with the enumeration name: `compression = Compression.lz4` |

Each component header and each property must be on a separate line; a line break ends the definition.

The following is an example of a __valid__ layout:

```text
-- Database settings
[database]
max_connections = 50
timeout = {DEFAULT: 30s; ADMIN: 5m}
```

The following is an example of an __invalid__ layout: a component header and a property name are on the same line, and the values of the properties are on the following lines.

```text
[database.tables] block_size
= 8KB
auto_vacuum =
true
```

If a component does not exist, a property does not exist in its component, or a value is not valid for the property's type, the definition is ignored and a warning is written to the system log.

| Setting | Error |
|---------|-------|
| `[bicycles]` | The component does not exist. |
| `frizzles = {DEFAULT: anything; USER: hunky-dory}` | The property does not exist. |
| `cache_size = {OWNER: 1GB}` | The option type `OWNER` does not exist; valid option types are `DEFAULT`, `USER`, `ADMIN`, and `SYSTEM`. |
| `port = 70000` | The value is outside the valid range (1&ndash;65535). |

## Configuration reference

The following sections list all components and their properties, grouped by function. Properties that are not set use the default value shown.

### System core settings

| Component | Property | Type | Valid values | Default | Description |
|-----------|----------|------|--------------|---------|-------------|
| __[system]__ | `id` | string | Letters, digits, `_`, `-` | Server host name | System identifier |
| | `locale` | string | `en-US`, `en-GB`, `fr-FR`, `es-ES`, ... | `en-US` | Localization setting |
| | `timezone` | string | `UTC`, `America/New_York`, ... | `UTC` | System time zone |
| | `debug_mode` | boolean | `true`, `false` | `false` | Enable debug logging |
| | `max_memory` | size-value | `512MB` to `64GB` | `8GB` | Maximum memory allocation |
| | `temp_dir` | file-path | Any local directory | `C:\Windows\Temp` | Temporary files directory |

### Database configuration

| Component | Property | Type | Valid values | Default | Description |
|-----------|----------|------|--------------|---------|-------------|
| __[database]__ | `type` | constant | `postgresql`, `sqlserver` | `postgresql` | Database engine |
| | `host` | host | IP address or host name, for example `db01.corp.example` | `127.0.0.1` | Database server address |
| | `port` | integer | 1&ndash;65535 | `5432` | Connection port (SQL Server uses `1433`) |
| | `max_connections` | integer | 10&ndash;500 | `50` | Connection pool size |
| | `timeout` | time-value | `1s` to `1h` | `30s` | Query timeout |
| | `ssl_enabled` | boolean | `true`, `false` | `true` | Encrypt database connections |
| __[database.tables]__ | `block_size` | size-value | `4KB`, `8KB`, `16KB`, `64KB` | `8KB` | Storage block size |
| | `auto_vacuum` | boolean | `true`, `false` | `true` | Automatic maintenance |
| | `compression` | constant | `none`, `gzip`, `lz4` | `lz4` | Data compression method |

### Network configuration

| Component | Property | Type | Valid values | Default | Description |
|-----------|----------|------|--------------|---------|-------------|
| __[network]__ | `bind_address` | host | IP address | `127.0.0.1` | Address of the web service; keep the loopback address when IIS is the reverse proxy |
| | `port` | integer | 1&ndash;65535 | `8443` | Web service port (published on 443 by IIS) |
| | `comms_port` | integer | 1&ndash;65535 | `6650` | Communications port for build agents and clients |
| | `max_request_size` | size-value | `1MB` to `100MB` | `10MB` | Maximum request size |
| | `keep_alive` | boolean | `true`, `false` | `true` | Keep connections alive |
| | `timeout` | time-value | `5s` to `10m` | `2m` | Connection timeout |
| __[network.ssl]__ | `enabled` | boolean | `true`, `false` | `true` | Enable TLS |
| | `cert_file` | file-path | Path to a `.crt` file | `"C:\Program Files\Nordvale\certs\server.crt"` | Server certificate; must match `key_file` |
| | `key_file` | file-path | Path to a `.key` file | `"C:\Program Files\Nordvale\certs\server.key"` | Private key of `cert_file` |
| | `protocol` | constant | `TLS1.2`, `TLS1.3` | `TLS1.3` | Minimum TLS protocol version |

### Security settings

| Component | Property | Type | Valid values | Default | Description |
|-----------|----------|------|--------------|---------|-------------|
| __[security]__ | `auth_method` | constant | `ldap`, `saml`, `oidc`, `local` | `ldap` | Authentication method |
| | `session_timeout` | time-value | `5m` to `24h` | `1h` | User session timeout |
| | `password_policy` | constant | `medium`, `strong` | `strong` | Password requirements for local accounts |
| | `max_login_attempts` | integer | 3&ndash;10 | `5` | Failed login limit before lockout |
| __[security.auth]__ | `ldap_server` | host | IP address or host name, for example `ldap.corp.example` | _(none)_ | LDAP server; required when `auth_method = ldap` |
| | `ldap_port` | integer | `389`, `636` | `636` | LDAP port (636 for LDAPS) |
| | `jwt_secret` | string | Quoted base64 string, for example `"<base64-encoded-secret>"` | Generated at installation | Signing secret for API tokens |
| | `token_expiry` | time-value | `15m` to `7d` | `24h` | API token lifetime |

### Performance tuning

| Component | Property | Type | Valid values | Default | Description |
|-----------|----------|------|--------------|---------|-------------|
| __[performance]__ | `cache_size` | size-value | `64MB` to `16GB` | `4096MB` | Application cache size |
| | `thread_pool_size` | integer | 2&ndash;64 | `8` | Worker thread count |
| | `queue_size` | integer | 100&ndash;10000 | `1000` | Request queue capacity |
| | `gc_threshold` | size-value | `100MB` to `4GB` | `512MB` | Memory use that triggers garbage collection; must be less than `max_memory` |

### Seat provisioning

| Component | Property | Type | Valid values | Default | Description |
|-----------|----------|------|--------------|---------|-------------|
| __[provisioning]__ | `max_seats` | integer | 10, 25, or 250 | Set from the license | Maximum number of seats (Standard, Professional, Enterprise); read-only, updated when a license is installed |
| | `seat_dir` | file-path | Any local directory | `"C:\Program Files\Nordvale\users"` | Directory for `*.seat` files |

### Logging and monitoring

| Component | Property | Type | Valid values | Default | Description |
|-----------|----------|------|--------------|---------|-------------|
| __[logging]__ | `level` | constant | `DEBUG`, `INFO`, `WARN`, `ERROR` | `INFO` | Log level |
| | `output` | constant | `file`, `eventlog`, `both` | `file` | Log destination (`eventlog` is the Windows Event Log) |
| | `file_path` | file-path | Path to a `.log` file | `C:\ProgramData\Nordvale\logs\system.log` | Log file location; used when `output` is `file` or `both` |
| | `max_file_size` | size-value | `10MB` to `1GB` | `100MB` | Log rotation size |
| | `retention_days` | integer | 1&ndash;365 | `30` | Log retention period |
| __[monitoring]__ | `metrics_enabled` | boolean | `true`, `false` | `true` | Enable metrics collection |
| | `health_check_port` | integer | 1&ndash;65535 | `8081` | Local health check port |
| | `alert_threshold` | float | `0.5` to `0.99` | `0.9` | Resource usage ratio that triggers an alert |
