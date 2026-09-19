# System Configuration Files

All the configurable parameters of the system are set using _system configuration files_ (__*.scf__). These are plain text files, and they use the following syntax&mdash;formulated in EBNF:

<pre id=ebnf-text>
config-file   ::= (component | comment | blank-line)*
component     ::= "[" identifier ("." identifier)* "]" newline property*
property      ::= identifier "=" value newline
value         ::= simple-value | complex-value
simple-value  ::= constant | boolean | number | string | file-path | ip-address
complex-value ::= "{" option (";" option)* "}"
option        ::= option-type ":" definition
option-type   ::= "DEFAULT" | "USER" | "ADMIN" | "SYSTEM"

constant      ::= [A-Za-z_][A-Za-z0-9_]*
boolean       ::= "true" | "false" | "yes" | "no" | "on" | "off"
number        ::= integer | float | size-value | time-value
integer       ::= [0-9]+
float         ::= [0-9]+ "." [0-9]+
size-value    ::= integer ("KB" | "MB" | "GB" | "TB")
time-value    ::= integer ("ms" | "s" | "m" | "h" | "d")
string        ::= "\"" [^"]* "\""
file-path     ::= ("/" | "\\") [^/\\]+ ("/" | "\\" [^/\\]+)*
ip-address    ::= [0-9]{1,3} "." [0-9]{1,3} "." [0-9]{1,3} "." [0-9]{1,3}
identifier    ::= [A-Za-z_][A-Za-z0-9_]*
comment       ::= "--" [^\n]* newline
blank-line    ::= whitespace* newline
newline       ::= "\n" | "\r\n"
whitespace    ::= " " | "\t"
</pre>

## Typical Uses

System components are identified by square brackets, and the settings of the component properties are specified between braces under that section.

The following table provides a few typical examples.

| Type | Examples |
|------|----------|
| **Component Definition** | `[system]`, `[database]`, `[network]`, `[security]` |
| **Nested Components** | `[database.tables]`, `[network.ssl]`, `[security.auth]` |
| **Simple Properties** | `enabled = true`, `port = 8080`, `timeout = 30s` |
| **Complex Properties** | `memory = {DEFAULT: 512MB; USER: 1GB; ADMIN: 2GB}` |
| **File Paths** | `log_file = "/var/log/system.log"` |
| **IP Addresses** | `bind_address = "192.168.1.100"` |

Each component or property has to be on a separate line, and line breaks are assumed to terminate the definition.

The following is an example of a __valid__ layout:

<pre id="config-text">
[database]
table_count = 50
record_size = {DEFAULT: 1024; USER: 4096}
</pre>

The following is an example of an __invalid__ layout: a section id and a property name are on the same line, and the settings of the ğroperties are on the next lines.

<pre id="config-text">
[disks] block_size
= 2048
replicated =
true
</pre>

If a component specified does not exist or the value set for a property is not within a valid range or one of the predefined constants, the definition is ignored.

|Setting|Error|
|-|-|
|`[bicycles]`|The component doesn't exist|
|`frizzles = {DEFAULT: anything; USER: hunky-dory}`|The property doesn't exist, and the settings are not recognized|
|`disk_size = {ADMIN: sys_admin}`|The option does not exist|

## Configuration Reference

The following sections enumerate all system components and their configurable properties, organized by functional area.

### System Core Settings

| Component | Property | Type | Values | Description |
|-----------|----------|------|--------|-------------|
| **[system]** | `id` | string | `[A-Za-z0-9_-]+` | System identifier |
| | `locale` | string | `en-US`, `fr-FR`, `es-ES`, etc. | Localization setting |
| | `timezone` | string | `UTC`, `America/New_York`, etc. | System timezone |
| | `debug_mode` | boolean | `true`, `false` | Enable debug logging |
| | `max_memory` | size-value | `512MB`, `2GB`, `8GB` | Maximum memory allocation |
| | `temp_dir` | file-path | `/tmp`, `C:\temp` | Temporary files directory |

### Database Configuration

| Component | Property | Type | Values | Description |
|-----------|----------|------|--------|-------------|
| **[database]** | `type` | enumerated | `Flat`, `Relational`, `NoSQL` | Database engine type |
| | `host` | ip-address | `127.0.0.1`, `db.internal` | Database server address |
| | `port` | integer | `1433`, `5432`, `3306` | Connection port |
| | `max_connections` | integer | `10`, `50`, `100` | Connection pool size |
| | `timeout` | time-value | `30s`, `5m`, `1h` | Query timeout |
| | `ssl_enabled` | boolean | `true`, `false` | Enable SSL connections |
| **[database.tables]** | `block_size` | size-value | `4KB`, `8KB`, `64KB` | Storage block size |
| | `auto_vacuum` | boolean | `true`, `false` | Automatic maintenance |
| | `compression` | enumerated | `none`, `gzip`, `lz4` | Data compression method |

### Network Configuration

| Component | Property | Type | Values | Description |
|-----------|----------|------|--------|-------------|
| **[network]** | `bind_address` | ip-address | `0.0.0.0`, `192.168.1.100` | Server bind address |
| | `port` | integer | `80`, `443`, `8080` | Service port |
| | `max_request_size` | size-value | `1MB`, `10MB`, `100MB` | Maximum request size |
| | `keep_alive` | boolean | `true`, `false` | Keep connections alive |
| | `timeout` | time-value | `30s`, `2m`, `5m` | Connection timeout |
| **[network.ssl]** | `enabled` | boolean | `true`, `false` | Enable SSL/TLS |
| | `cert_file` | file-path | `/etc/ssl/server.crt` | Certificate file path |
| | `key_file` | file-path | `/etc/ssl/server.key` | Private key file path |
| | `protocol` | enumerated | `TLS1.2`, `TLS1.3` | SSL/TLS protocol version |

### Security Settings

| Component | Property | Type | Values | Description |
|-----------|----------|------|--------|-------------|
| **[security]** | `auth_method` | enumerated | `basic`, `digest`, `oauth`, `jwt` | Authentication method |
| | `session_timeout` | time-value | `15m`, `1h`, `24h` | User session timeout |
| | `password_policy` | enumerated | `weak`, `medium`, `strong` | Password requirements |
| | `max_login_attempts` | integer | `3`, `5`, `10` | Failed login limit |
| **[security.auth]** | `ldap_server` | ip-address | `ldap.company.com` | LDAP server address |
| | `ldap_port` | integer | `389`, `636` | LDAP connection port |
| | `jwt_secret` | string | `base64-encoded-secret` | JWT signing secret |
| | `token_expiry` | time-value | `1h`, `24h`, `7d` | Access token lifetime |

### Performance Tuning

| Component | Property | Type | Values | Description |
|-----------|----------|------|--------|-------------|
| **[performance]** | `cache_size` | size-value | `64MB`, `256MB`, `1GB` | Application cache size |
| | `thread_pool_size` | integer | `4`, `8`, `16` | Worker thread count |
| | `queue_size` | integer | `100`, `1000`, `10000` | Request queue capacity |
| | `gc_threshold` | size-value | `100MB`, `512MB`, `1GB` | Garbage collection trigger |

### Logging & Monitoring

| Component | Property | Type | Values | Description |
|-----------|----------|------|--------|-------------|
| **[logging]** | `level` | enumerated | `DEBUG`, `INFO`, `WARN`, `ERROR` | Log level |
| | `output` | enumerated | `console`, `file`, `syslog` | Log destination |
| | `file_path` | file-path | `/var/log/app.log` | Log file location |
| | `max_file_size` | size-value | `10MB`, `100MB`, `1GB` | Log rotation size |
| | `retention_days` | integer | `7`, `30`, `90` | Log retention period |
| **[monitoring]** | `metrics_enabled` | boolean | `true`, `false` | Enable metrics collection |
| | `health_check_port` | integer | `8081`, `9090` | Health check endpoint |
| | `alert_threshold` | float | `0.8`, `0.9`, `0.95` | Resource alert threshold |
