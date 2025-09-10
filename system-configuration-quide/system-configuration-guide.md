# ProSoft v8.4.11 System Configuration Guide

This document includes ProSoft proprietary or confidential information and may not be redistributed or disclosed without prior written permission.

All information contained herein is provided "*AS IS*" based on the state of the ProSoft system as of the release date. ProSoft reserves the right to make changes to this document without prior notice.

---

## Disclaimer

NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, IS MADE IN RELATION TO THE CONTENTS OF THIS DOCUMENT REGARDING INCLUDING BUT NOT LIMITED TO AVAILABILITY, ACCURACY, RELIABILITY, NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PURPOSE. IN NO EVENT SHALL PROSOFT BE LIABLE FOR ANY DAMAGES, INCLUDING BUT NOT LIMITED TO DIRECT, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR DUE TO BUSINESS INTERRUPTION, OR ANY LOSS OF PROFIT, REVENUE, BUSINESS OPPORTUNITY, OR DATA THAT MAY ARISE FROM THE USE OF THE INFORMATION IN THIS DOCUMENT.

---

## Copyright

__ProSoft__ is a registered trademark of ProSoft Corporation. Other products mentioned in this document may be trademarks of their respective owners.

&copy; ProSoft 2024.

---

## Table of Contents

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

---

## About this guide

This guide was prepared to aid administrators in configuring, administrating, and troubleshooting the software system. It is assumed that the software system has been installed previously with the required hadrware configuration and networking infrastructure.

## Preliminary tasks

In order for the configuration procedure to continue without any errors or interruption, the servers where the system was installed, the network devices to be used to access the server and the clients, and the licenses and certificates required to use the software system must be ready and in place. To meet these prerequisites, follow the instructions below.

### Server requirements

The system requires server hardware that meets specific performance and reliability criteria based on your deployment size and user load.

#### Minimum Configuration (Small Teams: 10-50 users)

| Component | Specification | Purpose |
|-----------|---------------|---------|
| **CPU** | Intel Xeon E5-2690 v4 (14 cores, 2.6GHz) or AMD EPYC 7351P (16 cores, 2.4GHz) | Core processing and build management |
| **Memory** | 64GB DDR4-2133 ECC RAM | System operations and build caching |
| **Primary Storage** | 1TB NVMe SSD (PCIe 3.0, minimum 3,000 MB/s read) | Operating system and application data |
| **Secondary Storage** | 4TB SATA III HDD (7200 RPM) | Long-term data storage and backups |
| **Network** | Dual 1GbE NICs with failover support | Redundant network connectivity |
| **Power** | Redundant 750W PSUs with UPS backup | High availability power management |

#### Recommended Configuration (Medium Teams: 50-150 users)

| Component | Specification | Purpose |
|-----------|---------------|---------|
| **CPU** | Intel Xeon Gold 6248R (24 cores, 3.0GHz) or AMD EPYC 7542 (32 cores, 2.9GHz) | Enhanced processing for concurrent operations |
| **Memory** | 128GB DDR4-2666 ECC RAM | Improved performance for large repositories |
| **Primary Storage** | 2TB NVMe SSD RAID 1 (PCIe 4.0, minimum 5,000 MB/s read) | High-performance redundant storage |
| **Secondary Storage** | 8TB SAS HDD RAID 5 (10,000 RPM) | Enterprise-grade backup storage |
| **Network** | Dual 10GbE NICs with LACP aggregation | High-bandwidth network connectivity |
| **Power** | Redundant 1000W PSUs with extended UPS | Enhanced power reliability |

#### Enterprise Configuration (Large Teams: 150+ users)

| Component | Specification | Purpose |
|-----------|---------------|---------|
| **CPU** | Dual Intel Xeon Platinum 8280 (56 cores total, 2.7GHz) or AMD EPYC 7742 (64 cores, 2.25GHz) | Maximum processing capability |
| **Memory** | 256GB+ DDR4-3200 ECC RAM | Large-scale concurrent user support |
| **Primary Storage** | 4TB NVMe SSD RAID 10 (PCIe 4.0, minimum 7,000 MB/s read) | Enterprise-grade performance and redundancy |
| **Secondary Storage** | 16TB+ SAS HDD RAID 6 (15,000 RPM) with hot-swap capability | Maximum data protection and capacity |
| **Network** | Dual 25GbE NICs with redundant switch connections | Enterprise network performance |
| **Power** | Redundant 1600W PSUs with N+1 UPS configuration | Maximum uptime assurance |

#### Additional Hardware Requirements

**Server Form Factor Recommendations:**
- **Small/Medium**: 2U rack-mount server or tower server
- **Enterprise**: 4U rack-mount server with hot-swappable components

**Environmental Specifications:**
- Operating temperature: 10°C to 35°C (50°F to 95°F)
- Humidity: 20% to 80% non-condensing
- Cooling: Minimum 2,000 BTU/hr cooling capacity for enterprise configurations

> **Security Note**: Deploy the server behind a network firewall and proxy server. For enterprise deployments, implement a DMZ configuration with intrusion detection systems.

### Networking

The ProSoft system requires a robust network infrastructure to ensure reliable performance and security for all connected users and services.

#### Network Infrastructure Requirements

| Component | Specification | Purpose |
|-----------|---------------|---------|
| **Core Switch** | Managed Layer 3 switch with 24+ GbE ports, VLAN support | Primary network backbone |
| **Firewall** | Enterprise firewall with IDS/IPS capabilities (minimum 1Gbps throughput) | Security perimeter defense |
| **Proxy Server** | Reverse proxy with SSL termination and load balancing | Traffic management and security |
| **DNS Server** | Primary and secondary DNS with Active Directory integration | Name resolution and directory services |
| **Network Monitoring** | SNMP-capable monitoring with 24/7 alerting | Infrastructure health monitoring |

#### Required Network Ports

| Port | Protocol | Direction | Service | Security Level |
|------|----------|-----------|---------|----------------|
| 443 | HTTPS | Inbound | Web interface (secure) | Public |
| 4096 | TCP | Inbound/Outbound | API services | Restricted |
| 6650 | TCP | Inbound | Client connections | Internal only |
| 9595 | TCP | Inbound | Proxy management | Admin only |
| 22/3389 | SSH/RDP | Inbound | Administrative access | VPN only |
| 53 | UDP/TCP | Outbound | DNS resolution | Allowed |
| 123 | UDP | Outbound | NTP time synchronization | Allowed |
| 25/587 | TCP | Outbound | Email notifications | Restricted |

#### Firewall Configuration

**Recommended firewall rules for ProSoft deployment:**

```bash
# Allow HTTPS traffic to ProSoft web interface
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow API communication from internal networks only
iptables -A INPUT -p tcp --dport 4096 -s 192.168.0.0/16 -j ACCEPT
iptables -A INPUT -p tcp --dport 4096 -s 10.0.0.0/8 -j ACCEPT

# Allow client connections from corporate network
iptables -A INPUT -p tcp --dport 6650 -s 10.0.0.0/8 -j ACCEPT

# Block all other traffic to ProSoft ports
iptables -A INPUT -p tcp --dport 4096 -j DROP
iptables -A INPUT -p tcp --dport 6650 -j DROP
iptables -A INPUT -p tcp --dport 9595 -j DROP
```

#### Network Performance Requirements

| User Count | Minimum Bandwidth | Recommended Bandwidth | Latency Requirement |
|------------|------------------|---------------------|-------------------|
| 10-50 users | 100 Mbps | 500 Mbps | <50ms |
| 50-150 users | 500 Mbps | 1 Gbps | <30ms |
| 150+ users | 1 Gbps | 10 Gbps | <20ms |

#### DNS and Domain Configuration

**Required DNS records:**
```dns
prosoft.company.com.     A     10.0.1.100
api.prosoft.company.com. A     10.0.1.100
proxy.prosoft.company.com. A  10.0.1.101
```

**Domain requirements:**
- Active Directory domain membership (recommended)
- Kerberos authentication support
- LDAP connectivity for user management
- Certificate authority for SSL certificates

#### Proxy Server Configuration

The ProSoft system requires a reverse proxy for security and performance optimization.

**Recommended proxy settings (nginx example):**
```nginx
upstream prosoft_backend {
    server 10.0.1.100:8080;
    server 10.0.1.101:8080 backup;
}

server {
    listen 9595 ssl;
    server_name proxy.prosoft.company.com;

    ssl_certificate /etc/ssl/certs/prosoft.crt;
    ssl_certificate_key /etc/ssl/private/prosoft.key;

    location / {
        proxy_pass http://prosoft_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_connect_timeout 30s;
        proxy_read_timeout 300s;
    }
}
```

> **Wireless Security Warning**: Wireless access to ProSoft systems must be secured with WPA3-Enterprise authentication minimum. All wireless traffic should be isolated in a separate VLAN with additional monitoring. The ProSoft application does not perform network-level security validation beyond initial authentication.

### Licenses and certificates

During the configuration of the system, licenses (i.e. the `*.lic` files) and certificates (i.e. the `*.cert` files) will be required for the system to validate the installation and give access to users with various roles. Make sure that

* *Licenses* are in the root directory where the server is to be installed&mdash;assuming the default is not changed, that will be `C:\ProSoft`
* *Authentification Certificates* are in the `.\cert` directory under the root

#### ProSoft Licensing Scheme

| License Edition | Duration | Max Users | Available User Roles | Annual Cost (USD) | Support Level |
|----------------|----------|-----------|---------------------|-------------------|---------------|
| **Enterprise** | 1 Year | 250 | Auditor, Admin, Supervisor, Developer, Client | $25,000 | 24/7 Premium |
| **Professional** | 1 Year | 100 | Admin, Supervisor, Developer, Client | $12,500 | Business Hours |
| **SMB** | 1 Year | 50 | Admin, Developer, Client | $6,000 | Email Support |
| **Startup** | 1 Year | 25 | Admin, Developer, Client | $2,500 | Community Forum |

#### User Role Definitions

| Role | Permissions | Typical Usage |
|------|-------------|---------------|
| **Auditor** | Read-only access to all projects, compliance reporting | Security audits, compliance reviews |
| **Admin** | Full system administration, user management | System configuration, troubleshooting |
| **Supervisor** | Project oversight, team management, reporting | Project management, resource allocation |
| **Developer** | Code repository access, build management | Daily development tasks, code commits |
| **Client** | Limited project access, view-only dashboards | Stakeholder reviews, progress monitoring |

#### Certificate Requirements

**SSL/TLS Certificates:**
- Must be issued by a trusted Certificate Authority (CA)
- Minimum 2048-bit RSA or 256-bit ECC encryption
- Subject Alternative Names (SAN) for all ProSoft hostnames
- Wildcard certificates supported for subdomain flexibility

**Certificate File Locations:**
```
C:\ProSoft\cert\
├── server.crt          (Primary SSL certificate)
├── server.key          (Private key - SECURE)
├── intermediate.crt    (CA intermediate certificates)
├── root.crt           (Root CA certificate)
└── client-auth.crt    (Optional: Client authentication)
```

**Certificate Renewal Schedule:**
- SSL certificates: Renew 30 days before expiration
- Client authentication certificates: Renew 60 days before expiration
- Automated renewal available with CloudFlow protocol (Let's Encrypt compatible)

## Configuration

The system's configuration involves making the correct settings required by the server. This can be done either through the GUI or the CLI.

<span id="gui-byline">

This involves using the application's __Administration Console__.

* Double click the __ProSoft__ icon on the desktop to launch the console
* In the console window, pick the __Tools > Settings__ menu item. A window will pop up
* In the __Settings__ window, various settings can be found grouped according to the functionality they are related to:
  * The __Users__ group on the left is where you can add or remove users, set their credentials and the security groups they belong to, and assign them the directories under which the resources managed by __ProSoft&copy;__ are located
  * The __Resources__ group in the middle is for setting the directories the system uses to store various resources it generates and manages
  * The __System__ group on the right is for assigning the various values the system uses as defaults for marshalling and managing its data

</span>

<span id="cli-byline">

This involves running certain scripts&mdash;found in the `.\admin` directory under the root&mdash;through the command line. The script to be run depends on the settings to be configured.

* Launch a terminal with elevated (i.e. __admin__) privileges
* On the command line, navigate to the root directory

<pre id="cmdln-text">
C:\> cd C:\ProSoft\admin
C:\ProSoft\admin>
</pre>

* At this point, you should have the licenses (the `*.lic` files) under the root&mdash;i.e. the `C:\ProSoft\` directory&mdash;and the certificates (the `*.crt` files) under the `C:\ProSoft\cert\` directory. Run the PowerShell script named `sys_config.ps1` and check the output messages

<pre id="cmdln-text">
C:\ProSoft\admin> .\sys_config.ps1
>>> ProSoft System Configuration v8.4.11
>>> Checking prerequisites...
>>> Licenses discovered: 1 valid license found
>>> Certificates discovered: SSL certificate valid until 2025-12-31
>>> Initializing database schema...
>>> Database initialization: 100% complete
>>> Creating search indexes...
>>> Search indexes: 100% complete
>>> Configuration completed successfully
C:\ProSoft\admin>
</pre>

* If any of these messages do not appear, you should suspend the configuration procedure and troubleshoot. For this, see the [Troubleshooting](#troubleshooting) section below
* After the script has completed, you can exit the terminal

</span>

## System initialization

Before it can be used, the system has to be initialized to verify that its configured state is intact and that all the resources and connections it needs are in place and accessible. The initialization process is carried out as follows.

<span id="cli-byline">

To carry out system initialization using the command line,

* Open a terminal with elevated privileges and navigate to the admin directory
* Run the `sys_init.ps1` script with the required parameters, and monitor the initialization progress

<pre id="cmdln-text">
C:\> cd C:\ProSoft\admin
C:\ProSoft\admin> .\sys_init.ps1 -CertDir "..\cert" -LicenseFile ".\purchased.lic"
>>> ProSoft System Initialization v8.4.11
>>> Validating system prerequisites...
>>> Checking license validity...
</pre>

As the system proceeds with initialization, detailed status information is displayed:

<pre id="cmdln-text">
C:\ProSoft\admin> .\sys_init.ps1 -CertDir "..\cert" -LicenseFile ".\purchased.lic"
>>> ProSoft System Initialization v8.4.11
>>> Validating system prerequisites...
>>> License validation: PASSED (Enterprise, 250 seats, expires 2025-12-31)
>>> SSL certificate validation: PASSED (valid until 2025-12-31)
>>> Database connectivity test: PASSED (PostgreSQL 14.5)
>>> Admin module initialization: COMPLETED
>>> User management module: INITIALIZING [████████████████████░] 95%
</pre>

If required files are missing or invalid, the initialization process will halt with specific error messages:

<pre id="cmdln-text">
C:\ProSoft\admin> .\sys_init.ps1 -CertDir "..\cert" -LicenseFile ".\purchased.lic"
>>> ProSoft System Initialization v8.4.11
>>> Validating system prerequisites...
>>> License validation: PASSED
>>> SSL certificate validation: FAILED
    ERROR: Certificate file 'server.crt' not found in C:\ProSoft\cert\
    Required certificates:
    - server.crt (SSL certificate)
    - server.key (Private key)
    - intermediate.crt (CA chain)

    Please install valid certificates and press [R] to retry, or [Q] to quit:
</pre>

In that case, follow the instructions to resolve the issue, and resume the process by typing `Y` at the prompt.

After the errors are resolved and the system initialization is completed, the process prompts the user with a status:

<pre id="cmdln-text">
C:\>cd \ProSoft\admin
C:\ProSoft\admin>sys_init.ps --cert-dir=..\cert --licence-files=.\purchased.lic
>>> Initializing system...
>>> Licenses: Found
>>> Admin module: OK
>>> Users module: OK
>>> Networking module initializing: 24% -> ERROR
    Certificate(s) required to initialize the module missing.
    Place a valid certificate in the "..\cert" directory: Resume? [Y/N] Y
>>> Networking module: OK
>>> PROCESS COMPLETED!
C:\ProSoft\admin>
</pre>

</span>

## System administration

The system has a number of facilities which cannot be offered unattended. To provide them, the system administrator has to perform the following tasks.

### Availability and provisioning

Availability is measured based on the following criteria:

* The purchased number of seats with the license
* The number of seats that have already been provisioned
* Whether the seat and the resources available to it are accessible via the network and using the assigned roles

To provide seats to users, the following procedure must be performed:

<span id="gui-byline">

To carry out this task using the graphical interface,

* From the __Properties__ menu, open the __Seats__ window
* Check the number of seats already in use in the left panel. If there are no seats left, you have to purchase additional seats
* Check the group that the user is a member of to see whether it matches that of any of the available seats
* Assign the user to the seat by filling in his credentials in the middle panel
* Finally, click on the __Provision__ button on the bottom right

</span>

<span id="cli-byline">

To carry out this task using the command line,

* Open a terminal with elevated privileges
* Navigate to `users` directory under the root, i.e. `C:\ProSoft\users`, and list the files in the directory

<pre id="cmdln-text">
C:\ProSoft\users>ls * | ft Name

adm-3c47db38aa86f032.seat
adm-78fc4496f3aa5b3f.seat
cli-4a83c96fe68dfea5.seat
cli-d6407ede475985f0.seat
cli-58c8dab0dd8c8fce.seat
cli-869861562d411ee1.seat
cli-fc586256b8cbf654.seat
cli-fb6985abc41894f4.seat
sup-b51ae4a5c25e1658.seat
prov_seat.ps
prov_config.cfg
</pre>

* The seats already in use are listed as `*.seat` files with hexadecimal identifiers. The configuration file `prov_config.cfg` contains seat allocation settings. Query the maximum available seats using PowerShell:

<pre id="cmdln-text">
C:\ProSoft\users> Select-String -Pattern "MAX_USER" -Path "prov_config.cfg"

prov_config.cfg:18:MAX_USER=50
</pre>

* Use the PowerShell script `prov_seat.ps1` to automatically provision user seats. The script validates license availability and creates the appropriate seat configuration:

<pre id="cmdln-text">
C:\ProSoft\users> .\prov_seat.ps1 -UserType "client" -Username "john.doe" -Email "john.doe@company.com"
>>> ProSoft Seat Provisioning v8.4.11
>>> Checking license availability...
>>> Available seats: 42 of 50 (8 seats in use)
>>> Creating user profile for: john.doe
>>> Generating security credentials...
>>> Seat provisioned successfully
>>> Seat ID: cli-747ba03cab6fe9c
>>> User can now access ProSoft with provided credentials
</pre>

* Verify seat provisioning by listing the newly created seat file:

<pre id="cmdln-text">
C:\ProSoft\users> Get-ChildItem -Filter "*747ba03cab6fe9c*" | Format-Table Name

Name
----
cli-747ba03cab6fe9c.seat
</pre>

</span>

### Troubleshooting

Effective troubleshooting requires a systematic approach to identify, diagnose, and resolve system issues. Follow this structured methodology for all ProSoft-related problems.

#### General Troubleshooting Procedure

1. **Collect Error Information**: Note the exact error code, message, timestamp, and user context
2. **Check System Status**: Verify service status, resource utilization, and network connectivity
3. **Consult Error Reference**: Use the comprehensive error table below for initial diagnosis
4. **Apply Systematic Testing**: Test solutions in isolated environments before production
5. **Document Resolution**: Record successful resolution steps for future reference
6. **Escalate if Necessary**: Contact [ProSoft support](#prosoft-hotline) for complex issues

#### Log File Locations

| Component | Log File Path | Purpose |
|-----------|---------------|---------|
| **System Core** | `C:\ProSoft\logs\system.log` | Core system operations and errors |
| **Authentication** | `C:\ProSoft\logs\auth.log` | User authentication and authorization |
| **API Services** | `C:\ProSoft\logs\api.log` | REST API requests and responses |
| **Database** | `C:\ProSoft\logs\database.log` | Database queries and connection issues |
| **Build Engine** | `C:\ProSoft\logs\builds.log` | Build processing and compilation errors |
| **Network** | `C:\ProSoft\logs\network.log` | Network connectivity and proxy issues |

#### Diagnostic Commands

**System Health Check:**
```powershell
# Check ProSoft service status
C:\ProSoft\admin> .\prosoftctl.ps1 -Action "status" -Verbose

# Verify database connectivity
C:\ProSoft\admin> .\db_test.ps1 -ConnectionTest -ReportHealth

# Test API endpoints
C:\ProSoft\admin> .\api_test.ps1 -TestAll -ShowLatency
```

#### Comprehensive Error Reference Table

| Error ID | Error Message | Category | Root Cause | Recommended Action | Urgency |
|----------|---------------|----------|------------|-------------------|---------|
| **1001** | Service startup failed | System | Insufficient memory or disk space | Free up resources; check system requirements | High |
| **1002** | Database connection timeout | Database | Network issues or database server down | Verify database server status and connectivity | Critical |
| **1003** | License validation failed | Licensing | Invalid, expired, or corrupted license file | Reinstall valid license; contact licensing support | High |
| **1004** | SSL certificate error | Security | Certificate expired, invalid, or missing | Renew/replace SSL certificate; verify CA chain | High |
| **1122** | Authentication certificates not found | Security | Missing certificate files for user authentication | Install required authentication certificates | Medium |
| **1123** | Certificate authority not trusted | Security | CA not in trusted store | Import CA certificate to trusted root store | Medium |
| **2001** | Memory allocation error | Performance | Insufficient RAM or memory leak | Restart services; upgrade RAM if persistent | High |
| **2002** | Disk space critically low | Storage | Less than 5% free disk space | Free up disk space; expand storage capacity | Critical |
| **2003** | Network connection lost | Network | Network infrastructure failure | Check network cables, switches, DNS resolution | High |
| **2004** | Proxy server unreachable | Network | Proxy configuration or network routing | Verify proxy settings and network routes | Medium |
| **2244** | Certificate validation failed | Security | Certificate not recognized by authority | Replace with valid CA-signed certificate | High |
| **3001** | User authentication failed | Security | Invalid credentials or account lockout | Reset password; check account status | Low |
| **3002** | Access denied to resource | Security | Insufficient user permissions | Review and adjust user role permissions | Medium |
| **3003** | Session expired | Security | User session timeout reached | Re-authenticate; adjust session timeout settings | Low |
| **3344** | Certificate expired | Security | SSL certificate past expiration date | Renew certificate immediately | High |
| **4001** | Build process failed | Build | Source code errors or missing dependencies | Review build logs; fix compilation errors | Medium |
| **4002** | Repository synchronization error | Version Control | Git/SVN connectivity or authentication | Check version control credentials and connectivity | Medium |
| **4003** | API rate limit exceeded | API | Too many requests from single source | Implement request throttling; review API usage | Low |
| **5001** | Database query timeout | Performance | Slow query or database lock | Optimize queries; check database performance | Medium |
| **5002** | Search index corruption | Performance | Index files damaged or incomplete | Rebuild search indexes; verify disk integrity | Medium |
| **6001** | Email notification failed | Integration | SMTP server configuration error | Verify SMTP settings and authentication | Low |
| **6002** | External API integration error | Integration | Third-party service unavailable | Check third-party service status; review API keys | Medium |
| **7001** | Backup process failed | Maintenance | Insufficient space or permission issues | Check backup destination and permissions | Medium |
| **7002** | System cleanup failed | Maintenance | File system permissions or locks | Run cleanup with elevated privileges | Low |

#### Performance Troubleshooting

**System Performance Monitoring:**
```powershell
# Monitor system performance metrics
C:\ProSoft\admin> .\perf_monitor.ps1 -Duration 300 -Interval 10 -ExportCSV

# Identify resource-intensive processes
C:\ProSoft\admin> Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Check disk I/O performance
C:\ProSoft\admin> .\disk_io_test.ps1 -TestPath "C:\ProSoft\data" -Duration 60
```

**Database Performance:**
```sql
-- Check database connection count
SELECT COUNT(*) as active_connections FROM pg_stat_activity WHERE state = 'active';

-- Identify slow queries
SELECT query, mean_time, calls FROM pg_stat_statements
WHERE mean_time > 1000 ORDER BY mean_time DESC LIMIT 10;

-- Check table sizes and indexes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables WHERE schemaname = 'prosoft' ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

#### Network Troubleshooting

**Network Connectivity Tests:**
```powershell
# Test ProSoft API connectivity
C:\ProSoft\admin> Test-NetConnection -ComputerName "api.prosoft.company.com" -Port 4096

# Check DNS resolution
C:\ProSoft\admin> Resolve-DnsName "prosoft.company.com" -Type A

# Test proxy server connectivity
C:\ProSoft\admin> Test-NetConnection -ComputerName "proxy.prosoft.company.com" -Port 9595
```

#### Security Issue Resolution

**Certificate Management:**
```powershell
# Check certificate expiration
C:\ProSoft\admin> .\cert_check.ps1 -CertPath "C:\ProSoft\cert" -WarnDays 30

# Test SSL certificate validity
C:\ProSoft\admin> openssl x509 -in C:\ProSoft\cert\server.crt -text -noout

# Verify certificate chain
C:\ProSoft\admin> openssl verify -CAfile C:\ProSoft\cert\root.crt C:\ProSoft\cert\server.crt
```

### Decommissioning

If for some reason the system fails to meet your needs, there are a number of steps to take to decommission it.

<span id="cli-byline">

#### System Backup Procedures (Before Decommissioning)

Before decommissioning ProSoft, create a comprehensive backup of all system data, configurations, and licenses.

**Complete System Backup:**
```powershell
# Create backup directory with timestamp
C:\ProSoft\admin> $backupDir = "C:\ProSoft_Backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
C:\ProSoft\admin> New-Item -ItemType Directory -Path $backupDir

# Export database with full schema and data
C:\ProSoft\admin> .\db_backup.ps1 -BackupPath "$backupDir\database_backup.sql" -IncludeSchema -IncludeData

# Backup configuration files
C:\ProSoft\admin> Copy-Item -Path "C:\ProSoft\config\*" -Destination "$backupDir\config" -Recurse

# Backup licenses and certificates
C:\ProSoft\admin> Copy-Item -Path "C:\ProSoft\cert\*" -Destination "$backupDir\certificates" -Recurse
C:\ProSoft\admin> Copy-Item -Path "C:\ProSoft\*.lic" -Destination "$backupDir\licenses" -Recurse

# Backup user data and project repositories
C:\ProSoft\admin> .\backup_projects.ps1 -BackupPath "$backupDir\projects" -IncludeHistory
```

#### Decommissioning Procedure

To safely decommission the ProSoft system:

* Open an elevated PowerShell terminal and navigate to the admin directory
* Run the system analysis script to catalog all resources and dependencies

<pre id="cmdln-text">
C:\ProSoft\admin> .\decomm_sys.ps1 -GenerateReport -BackupPath "C:\ProSoft_Decommission"
>>> ProSoft Decommissioning Tool v8.4.11
>>> Analyzing system configuration...
>>> Cataloging active user sessions: 23 active users found
>>> Scanning project repositories: 156 projects, 45.2 GB data
>>> Analyzing database schema: 47 tables, 2.3 million records
>>> Generating resource inventory report...
>>> Report saved: C:\ProSoft_Decommission\system_inventory.csv
>>> Decommissioning analysis complete
</pre>

* Create final data backup using the comprehensive backup procedure above
* Gracefully stop all ProSoft services and notify users

<pre id="cmdln-text">
C:\ProSoft\admin> .\service_manager.ps1 -Action Stop -NotifyUsers -GracePeriod 300
>>> Sending shutdown notification to 23 active users
>>> Grace period: 5 minutes
>>> Stopping ProSoft Core Service... STOPPED
>>> Stopping ProSoft API Service... STOPPED
>>> Stopping ProSoft Build Engine... STOPPED
>>> All services stopped successfully
</pre>

* Release SSL certificates and revoke authentication tokens

<pre id="cmdln-text">
C:\ProSoft\admin> .\cert_manager.ps1 -Action Release -RevokeTokens
>>> Releasing SSL certificates from certificate store...
>>> Revoking 156 active authentication tokens...
>>> Clearing certificate cache...
>>> Certificate cleanup completed successfully
</pre>

* Deactivate software license to free up seat allocation

<pre id="cmdln-text">
C:\ProSoft\admin> .\license_manager.ps1 -Action Deactivate -License "Enterprise" -Confirm
>>> Deactivating ProSoft Enterprise license...
>>> Contacting licensing server...
>>> License deactivated successfully
>>> 250 seats released for reuse
>>> License key archived for future reactivation
</pre>

* Perform final system cleanup and uninstallation

<pre id="cmdln-text">
C:\ProSoft\admin> .\uninst_sys.ps1 -RemoveData -PreserveLogs
>>> ProSoft System Uninstaller v8.4.11
>>> Removing application files...
>>> Cleaning registry entries...
>>> Preserving log files for audit trail...
>>> Removing Windows services...
>>> Uninstallation completed successfully
>>>
>>> Preserved directories:
>>> - C:\ProSoft\logs (system logs)
>>> - C:\ProSoft\backup (backup files)
>>> - C:\ProSoft\decommission (decommission data)
</pre>

#### Post-Decommissioning Tasks

**Final Cleanup:**
```powershell
# Verify all services are stopped
Get-Service | Where-Object {$_.Name -like "*ProSoft*"}

# Remove ProSoft from Windows startup programs
Get-WmiObject -Class Win32_StartupCommand | Where-Object {$_.Command -like "*ProSoft*"}

# Clean up firewall rules
Remove-NetFirewallRule -DisplayName "ProSoft*"

# Remove scheduled tasks
Get-ScheduledTask | Where-Object {$_.TaskName -like "*ProSoft*"} | Unregister-ScheduledTask -Confirm:$false
```

> **Critical Data Preservation**: Store the following items securely for potential system restoration:
> - Complete database backup with transaction logs
> - All certificate files including private keys (encrypted storage required)
> - License files and activation records
> - System configuration files and custom scripts
> - User access logs and audit trails
>
> **Recommended Retention**: Keep decommissioning backups for minimum 3 years for compliance and disaster recovery purposes.

</span>

---

## __ProSoft__ Hotline

In case there are issues you are unable to resolve using available *User Assistance* material, you can reach __ProSoft__ free of charge for expert advice through:

*Phone*: 850-555-6677

*E-mail*: [support@prosoft.com](support@prosoft.com)

---
