# Nordvale Server 8.5.0 System Configuration Guide

All information contained herein is provided "*AS IS*" based on the state of Nordvale Server as of its release date. Nordvale reserves the right to make changes to this document without prior notice.

---

## Disclaimer

NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, IS MADE IN RELATION TO THE CONTENTS OF THIS DOCUMENT, INCLUDING BUT NOT LIMITED TO AVAILABILITY, ACCURACY, RELIABILITY, NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PURPOSE. IN NO EVENT SHALL NORDVALE BE LIABLE FOR ANY DAMAGES, INCLUDING BUT NOT LIMITED TO DIRECT, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR DUE TO BUSINESS INTERRUPTION, OR ANY LOSS OF PROFIT, REVENUE, BUSINESS OPPORTUNITY, OR DATA THAT MAY ARISE FROM THE USE OF THE INFORMATION IN THIS DOCUMENT.

---

## Copyright

__Nordvale__ is a registered trademark of Nordvale Corporation. Other products mentioned in this document may be trademarks of their respective owners.

&copy; Nordvale Corporation 2026.

> __Note:__ Nordvale, its products, and all hostnames in this document are fictitious. This is a portfolio sample.

---

## Table of contents

* [About this guide](#about-this-guide)
* [Preliminary tasks](#preliminary-tasks)
  * [Server requirements](#server-requirements)
  * [Networking](#networking)
  * [Licenses and certificates](#licenses-and-certificates)
* [Configuration](#configuration)
* [System initialization](#system-initialization)
* [System administration](#system-administration)
  * [Availability and provisioning](#availability-and-provisioning)
  * [Troubleshooting](#troubleshooting)
  * [Decommissioning](#decommissioning)
* [Nordvale hotline](#nordvale-hotline)

---

## About this guide

This guide helps administrators configure, administer, and troubleshoot Nordvale Server 8.5.0 on Windows Server 2022 or Windows Server 2019. It assumes that Nordvale Server has already been installed in the default directory, `C:\Program Files\Nordvale`, on hardware and network infrastructure that meet the requirements below. For the installation procedure, see the *Nordvale Server Installation Guide*.

The examples in this guide use a *Professional* edition system (25 seats) whose web interface is published as `nordvale.corp.example`.

All command-line procedures run in an elevated PowerShell session (__Run as administrator__). Code blocks labeled *PowerShell* contain only commands that you can copy and paste; the output you should expect appears in a separate block.

## Preliminary tasks

For the configuration procedure to complete without errors or interruptions, the server where Nordvale Server is installed, the network devices used to reach it, and the required licenses and certificates must be ready and in place. To meet these prerequisites, follow the instructions below.

### Server requirements

Size the server according to your license edition, which determines the maximum number of users (seats).

| Component | Standard (up to 10 users) | Professional (11&ndash;25 users) | Enterprise (26&ndash;250 users) |
|-----------|---------------------------|----------------------------------|---------------------------------|
| __CPU__ | 4 cores, 2.5 GHz or faster | 8 cores, 2.5 GHz or faster | 16 cores, 2.5 GHz or faster |
| __Memory__ | 16 GB | 32 GB | 64 GB ECC |
| __Primary storage__ | 250 GB SSD | 500 GB NVMe SSD | 1 TB NVMe SSD, RAID 1 |
| __Backup storage__ | 1 TB HDD | 2 TB HDD, RAID 1 | 8 TB HDD, RAID 6 |
| __Network__ | 1 Gigabit Ethernet | Dual 1 Gigabit Ethernet with failover | Dual 10 Gigabit Ethernet with link aggregation |
| __Power__ | 550 W PSU with UPS | Redundant 750 W PSUs with UPS | Redundant 1,600 W PSUs with N+1 UPS |

#### Environmental specifications

* Operating temperature: 10&nbsp;°C to 35&nbsp;°C (50&nbsp;°F to 95&nbsp;°F)
* Humidity: 20% to 80%, non-condensing
* Cooling: plan for about 3,412 BTU/hr per kilowatt of power drawn. A fully loaded Enterprise server drawing 1,600 W needs about 5,460 BTU/hr of cooling capacity.

> __Note:__ Deploy the server behind a perimeter firewall. For Enterprise deployments, place the server in a DMZ that is monitored by an intrusion detection system.

### Networking

Nordvale Server uses a single, fixed network model:

* IIS on the Nordvale server acts as the reverse proxy. It terminates TLS on port 443 and publishes both the web interface and the REST API (`/api/v1`).
* IIS forwards requests to the Nordvale Web Service, which listens only on the loopback address at `https://127.0.0.1:8443`. Port 8443 is never opened in the firewall.
* Build agents and desktop clients connect directly to the communications port, 6650.

#### Network infrastructure requirements

| Component | Specification | Purpose |
|-----------|---------------|---------|
| __Core switch__ | Managed Layer 3 switch with VLAN support | Network backbone |
| __Perimeter firewall__ | Enterprise firewall with IDS/IPS (1 Gbps throughput or higher) | Security perimeter |
| __Reverse proxy__ | IIS 10 with URL Rewrite and Application Request Routing, on the Nordvale server | TLS termination on port 443 |
| __DNS server__ | Primary and secondary DNS, integrated with Active Directory | Name resolution |
| __Network monitoring__ | SNMP-capable monitoring with 24/7 alerting | Infrastructure health |

#### Required network ports

| Port | Protocol | Direction | Service | Access |
|------|----------|-----------|---------|--------|
| 443 | HTTPS | Inbound | Web interface and REST API (IIS) | Corporate network |
| 6650 | TCP (TLS) | Inbound | Communications port for build agents and clients | Internal networks only |
| 8443 | HTTPS | Local only | Nordvale Web Service behind IIS | Loopback only; blocked in the firewall |
| 3389 | RDP | Inbound | Administrative access | VPN only |
| 443 | HTTPS | Outbound | License validation (`licensing.nordvale.example`) | Allowed |
| 5432 or 1433 | TCP | Outbound | External PostgreSQL or SQL Server database | Database server only |
| 53 | UDP/TCP | Outbound | DNS resolution | Allowed |
| 123 | UDP | Outbound | NTP time synchronization | Allowed |
| 587 | TCP | Outbound | E-mail notifications (SMTP submission) | Mail relay only |

#### Firewall configuration

The installer creates basic inbound rules. To restrict the communications port to internal networks and to block the local web service port explicitly, replace them with the following rules in Windows Defender Firewall:

```powershell
# Remove the default rules created by the installer
Remove-NetFirewallRule -DisplayName "Nordvale*"

# Allow HTTPS to the IIS reverse proxy
New-NetFirewallRule -DisplayName "Nordvale Web (HTTPS)" -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow

# Allow the communications port from internal networks only
New-NetFirewallRule -DisplayName "Nordvale Communications" -Direction Inbound -Protocol TCP -LocalPort 6650 -RemoteAddress 10.0.0.0/8, 192.168.0.0/16 -Action Allow

# Block the local web service port from the network
New-NetFirewallRule -DisplayName "Nordvale Web Service (block)" -Direction Inbound -Protocol TCP -LocalPort 8443 -Action Block
```

#### Network performance requirements

| Edition | Minimum bandwidth | Recommended bandwidth | Maximum latency |
|---------|-------------------|-----------------------|-----------------|
| Standard (up to 10 users) | 100 Mbps | 500 Mbps | 50 ms |
| Professional (11&ndash;25 users) | 500 Mbps | 1 Gbps | 30 ms |
| Enterprise (26&ndash;250 users) | 1 Gbps | 10 Gbps | 20 ms |

#### DNS and domain configuration

Create one DNS record for the server. The web interface and the REST API share this name.

```text
nordvale.corp.example.    A    10.0.1.100
```

Domain requirements:

* Active Directory domain membership (recommended)
* Kerberos authentication support
* LDAP connectivity for user management
* A certificate authority for TLS certificates

#### Reverse proxy configuration

The installer configures IIS as the reverse proxy. For reference, the rewrite rule it adds to `C:\inetpub\nordvale\web.config` is shown below. Do not change the target address: the Nordvale Web Service accepts connections only on `127.0.0.1:8443`.

```xml
<configuration>
  <system.webServer>
    <rewrite>
      <rules>
        <rule name="Nordvale reverse proxy" stopProcessing="true">
          <match url="(.*)" />
          <action type="Rewrite" url="https://127.0.0.1:8443/{R:1}" />
        </rule>
      </rules>
    </rewrite>
  </system.webServer>
</configuration>
```

The rule requires the proxy feature of Application Request Routing to be enabled at the server level. The installer enables it; to check or enable it manually, run:

```powershell
Set-WebConfigurationProperty -PSPath "MACHINE/WEBROOT/APPHOST" -Filter "system.webServer/proxy" -Name "enabled" -Value "True"
```

> __Warning:__ Wireless access to Nordvale Server must be secured with WPA3-Enterprise authentication at minimum. Isolate all wireless traffic in a separate, monitored VLAN. Nordvale Server does not perform network-level security validation beyond initial authentication.

### Licenses and certificates

During configuration, Nordvale Server needs a license file and TLS certificates to validate the installation and to grant access to users with various roles. Before you continue, make sure that:

* The *license file*, `nordvale.lic`, is in `C:\Program Files\Nordvale\license\`
* The *authentication certificates* (`*.crt` files) and the private key are in `C:\Program Files\Nordvale\certs\`

#### Nordvale license editions

| Edition | Term | Maximum users | Available user roles | Support level |
|---------|------|---------------|----------------------|---------------|
| __Standard__ | 1 year | 10 | Admin, Developer, Client | E-mail |
| __Professional__ | 1 year | 25 | Admin, Supervisor, Developer, Client | Business hours |
| __Enterprise__ | 1 year | 250 | Auditor, Admin, Supervisor, Developer, Client | 24/7 |

#### User role definitions

| Role | Permissions | Typical usage |
|------|-------------|---------------|
| __Auditor__ | Read-only access to all projects, compliance reporting | Security audits, compliance reviews |
| __Admin__ | Full system administration, user management | System configuration, troubleshooting |
| __Supervisor__ | Project oversight, team management, reporting | Project management, resource allocation |
| __Developer__ | Code repository access, build management | Daily development tasks, code commits |
| __Client__ | Limited project access, view-only dashboards | Stakeholder reviews, progress monitoring |

#### Certificate requirements

* Issued by a trusted certificate authority (CA)
* RSA keys of at least 2048 bits, or ECC keys of at least 256 bits
* Subject Alternative Name (SAN) entry for `nordvale.corp.example`
* Wildcard certificates are supported

#### Certificate file locations

```text
C:\Program Files\Nordvale\certs\
├── server.crt          (server certificate)
├── server.key          (private key; restrict access to Administrators)
├── intermediate.crt    (intermediate CA certificate)
├── root.crt            (root CA certificate)
└── client-auth.crt     (optional: client authentication)
```

#### Certificate renewal schedule

* Server certificates: renew 30 days before expiration
* Client authentication certificates: renew 60 days before expiration
* Automated renewal is available through the ACME protocol, for example with Let's Encrypt

## Configuration

Configuring the system means applying the settings that the server needs. You can do this either through the GUI or through the command line. Both methods write the settings to the system configuration files (`*.scf`) in `C:\Program Files\Nordvale\config\`. For the file syntax and all available properties, see the *Nordvale Server Configuration File Reference*.

__Using the GUI__

Use the Nordvale __Administration Console__:

1. From the __Start__ menu, open __Nordvale Administration Console__.
2. Select __Tools > Settings__. The __Settings__ window opens.
3. Review the settings, which are grouped by function:
   * In the __Users__ group on the left, add or remove users, set their credentials and security groups, and assign the directories that hold the resources Nordvale Server manages for them.
   * In the __Resources__ group in the middle, set the directories where the system stores the resources it generates and manages.
   * In the __System__ group on the right, set the default values the system uses for storing and managing its data.
4. Click __Apply__, and then click __OK__.

__Using the CLI__

Use the configuration scripts in the `admin` directory:

1. Open PowerShell as an administrator.
2. Change to the `admin` directory:

   ```powershell
   Set-Location "C:\Program Files\Nordvale\admin"
   ```

3. Check that the license file is in `C:\Program Files\Nordvale\license\` and the certificates are in `C:\Program Files\Nordvale\certs\`.
4. Run the `sys_config.ps1` script:

   ```powershell
   .\sys_config.ps1
   ```

   Expected output:

   ```text
   Nordvale System Configuration 8.5.0
   Checking prerequisites...
   License: 1 valid license found (Professional, 25 seats)
   Certificates: server certificate valid until 2027-12-31
   Initializing database schema... 100% complete
   Creating search indexes... 100% complete
   Configuration completed successfully
   ```

5. If any of these messages does not appear, stop the configuration procedure and see [Troubleshooting](#troubleshooting).

## System initialization

Before it can be used, the system must be initialized. Initialization verifies that the configured state is intact and that all required resources and connections are in place and accessible.

__Using the CLI__

1. Open PowerShell as an administrator and change to the `admin` directory:

   ```powershell
   Set-Location "C:\Program Files\Nordvale\admin"
   ```

2. Run the `sys_init.ps1` script with the certificate directory and the license file:

   ```powershell
   .\sys_init.ps1 -CertDir "C:\Program Files\Nordvale\certs" -LicenseFile "C:\Program Files\Nordvale\license\nordvale.lic"
   ```

   The script reports the status of each module as it initializes:

   ```text
   Nordvale System Initialization 8.5.0
   Validating system prerequisites...
   License validation: PASSED (Professional, 25 seats, expires 2027-12-31)
   Certificate validation: PASSED (valid until 2027-12-31)
   Database connectivity: PASSED (PostgreSQL 16.4)
   Admin module: OK
   Users module: OK
   Networking module: OK
   Initialization completed successfully
   ```

3. If a required file is missing or invalid, initialization pauses with an error message and a prompt. For example:

   ```text
   Certificate validation: FAILED
     ERROR 1122: Certificate file 'server.crt' not found in C:\Program Files\Nordvale\certs\
     Required files:
     - server.crt (server certificate)
     - server.key (private key)
     - intermediate.crt (CA chain)
   Install valid certificates, then press [R] to retry or [Q] to quit:
   ```

4. Resolve the problem (in this example, copy the missing certificate files to `C:\Program Files\Nordvale\certs\`), and then press __R__ to retry. Initialization resumes from the failed check. If you press __Q__, run the script again from step 2 after you fix the problem.

## System administration

Some tasks cannot be performed unattended. The system administrator performs them as described below.

### Availability and provisioning

Availability is determined by:

* The number of seats purchased with the license
* The number of seats that have already been provisioned
* Whether each seat, and the resources available to it, can be reached over the network with the assigned role

To provision a seat for a user, use one of the following methods.

__Using the GUI__

1. In the Administration Console, select __Properties > Seats__.
2. In the left panel, check the number of seats in use. If no seats are left, purchase additional seats or upgrade the license edition.
3. Check that the user's group matches that of an available seat.
4. In the middle panel, enter the user's credentials.
5. Click __Provision__.

__Using the CLI__

1. Open PowerShell as an administrator and change to the `users` directory:

   ```powershell
   Set-Location "C:\Program Files\Nordvale\users"
   Get-ChildItem | Format-Table Name
   ```

   Expected output (9 seats in use):

   ```text
   Name
   ----
   adm-3c47db38aa86f032.seat
   adm-78fc4496f3aa5b3f.seat
   cli-4a83c96fe68dfea5.seat
   cli-58c8dab0dd8c8fce.seat
   cli-869861562d411ee1.seat
   cli-d6407ede475985f0.seat
   cli-fb6985abc41894f4.seat
   cli-fc586256b8cbf654.seat
   sup-b51ae4a5c25e1658.seat
   prov_config.scf
   prov_seat.ps1
   ```

   Each provisioned seat is a `*.seat` file named after its role prefix and a 16-digit hexadecimal identifier. The `prov_config.scf` file contains the seat allocation settings of the `[provisioning]` component.

2. Check the maximum number of seats:

   ```powershell
   Select-String -Pattern "max_seats" -Path "prov_config.scf"
   ```

   Expected output:

   ```text
   prov_config.scf:18:max_seats = 25
   ```

3. Run the `prov_seat.ps1` script to provision the seat. The script checks license availability and creates the seat file:

   ```powershell
   .\prov_seat.ps1 -UserType "client" -Username "jane.roe" -Email "jane.roe@corp.example"
   ```

   Expected output:

   ```text
   Nordvale Seat Provisioning 8.5.0
   Checking license availability...
   Seats in use: 9 of 25 (16 available)
   Creating user profile for: jane.roe
   Generating security credentials...
   Seat provisioned successfully
   Seat ID: cli-747ba03cab6fe9c2
   Seats in use: 10 of 25 (15 available)
   ```

4. Verify that the seat file was created:

   ```powershell
   Get-ChildItem -Filter "*747ba03cab6fe9c2*" | Format-Table Name
   ```

   Expected output:

   ```text
   Name
   ----
   cli-747ba03cab6fe9c2.seat
   ```

### Troubleshooting

Troubleshoot systematically to identify, diagnose, and resolve problems.

#### General troubleshooting procedure

1. __Collect error information:__ note the error ID, message, timestamp, and user context.
2. __Check system status:__ verify service status, resource usage, and network connectivity.
3. __Consult the error reference:__ use the [error reference table](#error-reference-table) for an initial diagnosis.
4. __Test the fix:__ where possible, test the solution in a non-production environment first.
5. __Document the resolution:__ record the steps that resolved the issue.
6. __Escalate if necessary:__ contact the [Nordvale hotline](#nordvale-hotline).

#### Log file locations

| Component | Log file | Contents |
|-----------|----------|----------|
| __System core__ | `C:\ProgramData\Nordvale\logs\system.log` | Core system operations and errors |
| __Authentication__ | `C:\ProgramData\Nordvale\logs\auth.log` | User authentication and authorization |
| __REST API__ | `C:\ProgramData\Nordvale\logs\api.log` | API requests and responses |
| __Database__ | `C:\ProgramData\Nordvale\logs\database.log` | Database queries and connection issues |
| __Build engine__ | `C:\ProgramData\Nordvale\logs\builds.log` | Build processing and compilation errors |
| __Network__ | `C:\ProgramData\Nordvale\logs\network.log` | Connectivity and reverse proxy issues |

#### Diagnostic commands

Run these commands from `C:\Program Files\Nordvale\admin`:

```powershell
# Check the status of the Nordvale services
.\nordvalectl.exe status

# Verify database connectivity
.\db_test.ps1 -ConnectionTest -ReportHealth

# Test the REST API endpoints
.\api_test.ps1 -TestAll -ShowLatency
```

#### Error reference table

| Error ID | Error message | Category | Root cause | Recommended action | Urgency |
|----------|---------------|----------|------------|--------------------|---------|
| __1001__ | Service startup failed | System | Insufficient memory or disk space | Free up resources; check the server requirements | High |
| __1002__ | Database connection timeout | Database | Network issues or database server down | Verify database server status and connectivity | Critical |
| __1003__ | License validation failed | Licensing | Invalid, expired, or corrupted license file | Reinstall a valid license; contact licensing support | High |
| __1004__ | TLS certificate error | Security | Certificate expired, invalid, or missing | Renew or replace the certificate; verify the CA chain | High |
| __1122__ | Authentication certificates not found | Security | Missing certificate files | Install the required certificates in the `certs` directory | Medium |
| __1123__ | Certificate authority not trusted | Security | CA not in the trusted store | Import the CA certificate into the trusted root store | Medium |
| __2001__ | Memory allocation error | Performance | Insufficient RAM or memory leak | Restart the services; add RAM if the error persists | High |
| __2002__ | Disk space critically low | Storage | Less than 5% free disk space | Free up disk space; expand storage | Critical |
| __2003__ | Network connection lost | Network | Network infrastructure failure | Check cabling, switches, and DNS resolution | High |
| __2004__ | Reverse proxy unreachable | Network | IIS stopped or rewrite rule misconfigured | Check the IIS site and the rewrite rule | Medium |
| __2244__ | Certificate validation failed | Security | Certificate not recognized by the authority | Replace with a valid CA-signed certificate | High |
| __3001__ | User authentication failed | Security | Invalid credentials or account lockout | Reset the password; check the account status | Low |
| __3002__ | Access denied to resource | Security | Insufficient user permissions | Review and adjust the user's role | Medium |
| __3003__ | Session expired | Security | Session timeout reached | Log in again; adjust the session timeout | Low |
| __3344__ | Certificate expired | Security | Certificate past its expiration date | Renew the certificate immediately | High |
| __4001__ | Build process failed | Build | Source code errors or missing dependencies | Review the build log; fix compilation errors | Medium |
| __4002__ | Repository synchronization error | Version control | Repository connectivity or authentication | Check version control credentials and connectivity | Medium |
| __4003__ | API rate limit exceeded | API | Too many requests from a single source | Throttle requests; review API usage | Low |
| __5001__ | Database query timeout | Performance | Slow query or database lock | Optimize queries; check database performance | Medium |
| __5002__ | Search index corruption | Performance | Index files damaged or incomplete | Rebuild the search indexes; check disk integrity | Medium |
| __6001__ | E-mail notification failed | Integration | SMTP configuration error | Verify the SMTP settings and credentials | Low |
| __6002__ | External API integration error | Integration | Third-party service unavailable | Check the third-party service; review API keys | Medium |
| __7001__ | Backup process failed | Maintenance | Insufficient space or permissions | Check the backup destination and its permissions | Medium |
| __7002__ | System cleanup failed | Maintenance | File system permissions or locks | Run the cleanup from an elevated prompt | Low |

#### Performance troubleshooting

```powershell
# Record performance metrics every 10 seconds for 5 minutes
.\perf_monitor.ps1 -Duration 300 -Interval 10 -ExportCSV

# List the 10 processes using the most CPU time
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Test disk I/O on the data directory
.\disk_io_test.ps1 -TestPath "C:\Program Files\Nordvale\data" -Duration 60
```

The following PostgreSQL queries help diagnose database performance. The slow-query check requires the `pg_stat_statements` extension; the `mean_exec_time` column is available in PostgreSQL 13 and later.

```sql
-- Count active connections
SELECT COUNT(*) AS active_connections FROM pg_stat_activity WHERE state = 'active';

-- List the 10 slowest queries (mean execution time over 1 second)
SELECT query, mean_exec_time, calls FROM pg_stat_statements
WHERE mean_exec_time > 1000 ORDER BY mean_exec_time DESC LIMIT 10;

-- List Nordvale tables by total size, including indexes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size
FROM pg_tables WHERE schemaname = 'nordvale'
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC;
```

#### Network troubleshooting

```powershell
# Test the web interface and REST API through IIS
Test-NetConnection -ComputerName "nordvale.corp.example" -Port 443

# Test the communications port
Test-NetConnection -ComputerName "nordvale.corp.example" -Port 6650

# Check DNS resolution
Resolve-DnsName "nordvale.corp.example" -Type A
```

#### Certificate troubleshooting

```powershell
# Report certificates that expire within 30 days
.\cert_check.ps1 -CertDir "C:\Program Files\Nordvale\certs" -WarnDays 30

# Verify the certificate chain with the built-in Windows tool
certutil -verify "C:\Program Files\Nordvale\certs\server.crt"
```

If OpenSSL is installed on the server, you can inspect the certificate and verify the full chain, supplying the intermediate certificate as untrusted input:

```powershell
openssl x509 -in "C:\Program Files\Nordvale\certs\server.crt" -text -noout
openssl verify -CAfile "C:\Program Files\Nordvale\certs\root.crt" -untrusted "C:\Program Files\Nordvale\certs\intermediate.crt" "C:\Program Files\Nordvale\certs\server.crt"
```

### Decommissioning

If the system no longer meets your needs, decommission it as follows. All backups in this procedure are written to a single timestamped directory outside the installation directory, which the uninstaller does not touch.

__Using the CLI__

1. Open PowerShell as an administrator, change to the `admin` directory, and define the backup directory:

   ```powershell
   Set-Location "C:\Program Files\Nordvale\admin"
   $backupDir = "D:\Backups\Nordvale_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
   New-Item -ItemType Directory -Path $backupDir
   ```

2. Generate an inventory of all resources and dependencies:

   ```powershell
   .\decomm_sys.ps1 -GenerateReport -BackupPath $backupDir
   ```

   Expected output:

   ```text
   Nordvale Decommissioning Tool 8.5.0
   Analyzing system configuration...
   Active user sessions: 7
   Project repositories: 156 projects, 45.2 GB
   Database schema: 47 tables, 2.3 million records
   Report saved: D:\Backups\Nordvale_20260926_140512\system_inventory.csv
   Decommissioning analysis complete
   ```

3. Notify users and stop all Nordvale services, so that no data changes during the backup:

   ```powershell
   .\nordvalectl.exe stop --notify-users --grace-period 300
   ```

   Expected output:

   ```text
   Sending shutdown notification to 7 active users
   Grace period: 5 minutes
   Stopping Nordvale Core Service... STOPPED
   Stopping Nordvale Web Service... STOPPED
   Stopping Nordvale Build Engine... STOPPED
   All services stopped
   ```

4. Back up the database, configuration, license, certificates, and projects:

   ```powershell
   # Export the database with schema and data
   .\db_backup.ps1 -BackupPath "$backupDir\database_backup.sql" -IncludeSchema -IncludeData

   # Back up configuration files, the license, and certificates
   Copy-Item -Path "C:\Program Files\Nordvale\config" -Destination "$backupDir\config" -Recurse
   Copy-Item -Path "C:\Program Files\Nordvale\license" -Destination "$backupDir\license" -Recurse
   Copy-Item -Path "C:\Program Files\Nordvale\certs" -Destination "$backupDir\certs" -Recurse

   # Back up project repositories with their history
   .\backup_projects.ps1 -BackupPath "$backupDir\projects" -IncludeHistory
   ```

5. Remove the certificates from the certificate store and revoke all authentication tokens:

   ```powershell
   .\cert_manager.ps1 -Action Release -RevokeTokens
   ```

   Expected output:

   ```text
   Removing certificates from the LocalMachine\My store...
   Revoking 10 seat credentials and 42 API tokens...
   Certificate cleanup completed
   ```

6. Deactivate the license so that its seats can be reused on another server:

   ```powershell
   .\license_manager.ps1 -Action Deactivate -LicenseFile "C:\Program Files\Nordvale\license\nordvale.lic"
   ```

   Expected output:

   ```text
   Deactivating Nordvale Professional license...
   Contacting licensing.nordvale.example...
   License deactivated; 25 seats released for reuse
   ```

7. Uninstall Nordvale Server, keeping the logs for audit purposes:

   ```powershell
   .\uninst_sys.ps1 -RemoveData -PreserveLogs
   ```

   Expected output:

   ```text
   Nordvale System Uninstaller 8.5.0
   Removing application files...
   Removing Windows services...
   Cleaning registry entries...
   Preserving log files for audit trail...
   Uninstallation completed
   Preserved: C:\ProgramData\Nordvale\logs
   ```

#### Post-decommissioning tasks

```powershell
# Verify that no Nordvale services remain
Get-Service -Name "Nordvale*"

# List startup entries that still reference Nordvale (remove any you find)
Get-CimInstance -ClassName Win32_StartupCommand | Where-Object { $_.Command -like "*Nordvale*" }

# Remove the firewall rules
Remove-NetFirewallRule -DisplayName "Nordvale*"

# Remove the scheduled tasks
Get-ScheduledTask -TaskName "*Nordvale*" | Unregister-ScheduledTask -Confirm:$false
```

> __Note:__ Store the following items securely in case you need to restore the system:
>
> * The database backup
> * All certificate files, including private keys (in encrypted storage)
> * The license file and activation records
> * Configuration files and custom scripts
> * User access logs and audit trails
>
> Keep decommissioning backups for at least 3 years for compliance and disaster recovery purposes.

---

## Nordvale hotline

If you cannot resolve an issue with the available user assistance material, contact Nordvale free of charge for expert advice:

*Phone*: +1 850-555-0167

*E-mail*: [support@nordvale.example](mailto:support@nordvale.example)
