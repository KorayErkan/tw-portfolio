# __ProSoft__&trade; Installation Guide

This document provides information about the system requirements of ProSoft v8.4.11, as well as the procedure for installing it.

## Disclaimer

NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, IS MADE IN RELATION TO THE CONTENTS OF THIS DOCUMENT REGARDING INCLUDING BUT NOT LIMITED TO AVAILABILITY, ACCURACY, RELIABILITY, NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PURPOSE. IN NO EVENT SHALL PROSOFT BE LIABLE FOR ANY DAMAGES, INCLUDING BUT NOT LIMITED TO DIRECT, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR DUE TO BUSINESS INTERRUPTION, OR ANY LOSS OF PROFIT, REVENUE, BUSINESS OPPORTUNITY, OR DATA THAT MAY ARISE FROM THE USE OF THE INFORMATION IN THIS DOCUMENT.

---

## Copyright

__ProSoft__ is registered trademark of ProSoft Corporation. Other products mentioned in this document may be trademarks of their respective owners.

This document is subject to change without prior notice.

&copy; ProSoft 2024.

---

## Table of Contents

* [Introduction](#introduction)
* [System Requirements](#system-requirements)
  * [Hardware](#hardware)
  * [Dependencies](#dependencies)
* [Installation](#installation)
* [Configuration](#configuration)
* [License Terms](#license-terms)

---

## Introduction

__ProSoft__&trade; is an engineering solution for managing CI/CD pipeline automation in software development. The system keeps track of the modifications and additions made to the codebase&mdash;including acceptance, unit, and integration tests&mdash;and the commits to source control, creates an automated pipeline for building release candidates, updates version numbers using *semantic versioning*, calculates *technical debt* based on targets, and charts the progress of various aspects of the project to provide a global picture.

The system is compliant with the requirements and logic of CI/CD as it has been laid out in RFC 3265-A and RFC 3265-B.

## System Requirements

### Operating System Compatibility

| Operating System | Version | Architecture | Status |
|------------------|---------|-------------|--------|
| Windows Server 2019 | Build 17763+ | x64 | Recommended |
| Windows Server 2022 | Build 20348+ | x64 | Recommended |
| Windows 10 Enterprise | Version 1909+ | x64 | Supported |
| Windows 11 Pro/Enterprise | Version 21H2+ | x64 | Supported |
| Ubuntu Server LTS | 20.04, 22.04 | x64 | Supported |
| Red Hat Enterprise Linux | 8.x, 9.x | x64 | Supported |

### Hardware Requirements

#### Minimum Requirements (Development Team: 10-25 users)

| Component | Specification |
|-----------|---------------|
| **CPU** | Intel Core i7-10700K (8 cores, 3.8GHz base) or AMD Ryzen 7 3700X (8 cores, 3.6GHz base) |
| **Memory** | 32GB DDR4-3200 RAM |
| **Storage** | 500GB NVMe SSD (minimum 3,500 MB/s read speed) |
| **Network** | Gigabit Ethernet (1000Base-T) |
| **GPU** | Integrated graphics sufficient |

#### Recommended Requirements (Development Team: 25-100 users)

| Component | Specification |
|-----------|---------------|
| **CPU** | Intel Xeon W-2245 (8 cores, 3.9GHz base) or AMD EPYC 7302P (16 cores, 3.0GHz base) |
| **Memory** | 128GB DDR4-3200 ECC RAM |
| **Storage** | 2TB NVMe SSD RAID 1 configuration (minimum 5,000 MB/s read speed) |
| **Network** | 10 Gigabit Ethernet or dual Gigabit NICs |
| **GPU** | Not required for server operation |

#### Enterprise Requirements (Development Team: 100+ users)

| Component | Specification |
|-----------|---------------|
| **CPU** | Dual Intel Xeon Gold 6248R (48 cores total) or AMD EPYC 7742 (64 cores, 2.25GHz base) |
| **Memory** | 256GB+ DDR4-3200 ECC RAM |
| **Storage** | 4TB+ NVMe SSD RAID 10 configuration with hot swap capability |
| **Network** | 10+ Gigabit Ethernet with redundant connections |
| **Backup** | Dedicated backup storage subsystem (8TB+ capacity) |

### Network Requirements

| Port | Protocol | Direction | Purpose |
|------|----------|-----------|---------|
| 443 | HTTPS | Outbound | License validation and updates |
| 4096 | TCP | Inbound/Outbound | API communication |
| 6650 | TCP | Inbound | Client connections |
| 8080 | HTTP | Inbound | Web management interface |
| 5432 | TCP | Inbound/Outbound | PostgreSQL database (if external) |
| 1433 | TCP | Inbound/Outbound | SQL Server database (if external) |

### Dependencies

The installer performs automated dependency checking. Installation will be terminated if any required components are missing.

#### Required Dependencies

| Component | Version | Architecture | Purpose |
|-----------|---------|-------------|---------|
| **Microsoft Visual C++ Redistributable** | 2019-2022 (14.29+) | x64 | Runtime libraries for MSVC compiled components |
| **Microsoft .NET Runtime** | 6.0.0 or 7.0.0+ | x64 | Primary application runtime environment |
| **Database Server** | See table below | x64 | Persistent data storage and repository management |
| **Web Server** | IIS 10.0+ or Apache 2.4+ | x64 | Web interface and API hosting |

#### Database Compatibility Matrix

| Database System | Supported Versions | Connection Method | Notes |
|----------------|-------------------|-------------------|-------|
| **PostgreSQL** | 13.0 - 15.x | TCP/IP, Local Socket | Recommended for new installations |
| **Microsoft SQL Server** | 2019, 2022 | TCP/IP, Named Pipes | Enterprise environments |
| **Oracle Database** | 19c, 21c | TCP/IP, Oracle Net | Large-scale deployments |
| **MySQL** | 8.0.28+ | TCP/IP | Community edition supported |

#### Optional Components

| Component | Version | Benefit |
|-----------|---------|---------|
| **Redis Cache** | 6.2+ | 60% faster API response times |
| **Elasticsearch** | 7.17+ or 8.x | Advanced search capabilities |
| **Docker Engine** | 20.10+ | Containerized deployment support |

#### Firewall Requirements

Ensure the following firewall exceptions are configured:

```powershell
# Windows Firewall configuration
New-NetFirewallRule -DisplayName "ProSoft API" -Direction Inbound -Protocol TCP -LocalPort 4096
New-NetFirewallRule -DisplayName "ProSoft Client" -Direction Inbound -Protocol TCP -LocalPort 6650
New-NetFirewallRule -DisplayName "ProSoft Web" -Direction Inbound -Protocol TCP -LocalPort 8080
```

The system locale is *en-US* by default but supports all ISO 639-1 language codes.

## Installation

The following steps are based on the 64-bit version, but they are identical for the 32-bit version. Before you start the installation, check that the above-mentioned prerequisite components are in place.

Before beginning the installation, from the __ProSoft__ [downloads](https://www.prosoft.com/downloads) page, download the `prosoft_x64.msi` file to the `C:\Users\<admin-name>\Downloads` directory of your server.

<span id="gui-byline">

* Open __Explorer__ and navigate to the __Downloads__ folder.
* Double-click the `prosoft_x64.msi` file to start the installation and follow the on-screen instructions
* By default, the server is installed in the `C:\Programs\ProSoft` directory. It is strongly recommended that this directory is *not* changed
* Confirm the settings on the configuration page of the installer. It is recommend that the default values for cache size, disk size, API endpoints, communication ports, and others are left as they are unless you have a good reason to change them
* If you need to change the locale setting, you will be prompted to select one on the next page of the installer
* Finally, click `Ok` to start the installation process. Because the system creates partitions for more efficient marshalling of data, it may take up to 15 for this stage to complete.

</span>

<span id="cli-byline">

* Open a terminal window with elevated (i.e. __admin__) privileges. If you haven't downloaded the installation (i.e. __*.msi__) file, you can do so on the command line by typing

<pre id="cmdln-text">
C:\> curl -L -o prosoft_x64.msi https://www.prosoft.com/downloads/prosoft_x64.msi
C:\> # Alternative: Use PowerShell's Invoke-WebRequest
C:\> Invoke-WebRequest -Uri "https://www.prosoft.com/downloads/prosoft_x64.msi" -OutFile "prosoft_x64.msi"
</pre>

* Navigate (i.e. `cd`) to the __Downloads__ directory of your server by typing:

<pre id="cmdln-text">
C:\> cd \Users\<admin-name>\Downloads
</pre>

* Start the installation by typing `prosoft_x64.msi`. You must specify the installation directory. By default, this is `C:\Programs\ProSoft` and It is strongly recommended that this directory is *not* changed. Follow the on-screen instructions

<pre id="cmdln-text">
C:\> prosoft_x64 install --target-dir=C:\Programs\ProSoft
>>> Installing...
</pre>

* It is recommended that the default values for cache size, disk size, API endpoints, communication ports, and others are *not* changed unless you have a good reason to do so. To confirm these settings, type `Y` (for __Yes__) for each when prompted on the command line

<pre id="cmdln-text">
>>> cache_size=4096KB? [Y/N]: Y
>>> disk_size=50MB? [Y/N]: Y
>>> api_endpoints=prosoft_api_server? [Y/N]: Y
>>> communications_port=6060? [Y/N]: Y
>>> default_user_count=50? [Y/N]: Y
</pre>

* You will be prompted to confirm or change the locale setting:

<pre id="cmdln-text">
>>> locale=en_US? [Y/N]: N
    Please specify the locale: en-GB
</pre>

* Finally, confirm the settings by typing `Y` to start the installation process.

<pre id="cmdln-text">
>>> Please confirm the settings to start the installation [Y/N]:
</pre>

Because the system creates partitions for more efficient marshalling of data, it may take up to 15 minutes for this stage to complete.

</span>

## Configuration

After the installation process is completed, the basic configuration needs to be made, and this has to be done through the command line. The process is as follows:

<span id="cli-byline">

* Copy the `prosoft.lic` file sent to you via e-mail to the `bin` subdirectory of the installation folder. It is advised that you rename this file using the name of your company. Here, we will use `company-name` for this.

<pre id="cmdln-text">
C:\Downloads>mv prosoft.lic company-name.lic
C:\Downloads>copy company-name.lic \ProSoft\bin
</pre>

* Navigate to the `admin` directory of the root, and install the license by running the `install_lic.ps` script

<pre id="cmdln-text">
C:\Downloads>cd \ProSoft\admin
C:\ProSoft\admin>install_lic.ps --license-file=company-name.lic
>>> Installing license ...
>>> Done
</pre>

> <span id="note-byline">If you do not introduce the license through the command line, you will be prompted the first time you launch the program to point to this file for activation.
> </span>

* Copy the security certificates (which we will call in our example `company-cert`) the system needs to the `cert` directory of the root, and instaşll them by running the `install_cert.ps` script:

<pre id="cmdln-text">
C:\ProSoft\admin>copy \Users\&lt;admin-name&gt;\company-cert-1.ca company-cert-2.ca ..\cert
C:\ProSoft\admin>install_cert.ps --install-dir=..\cert --certificates=..\cert\*.ca
>>> Installing certificates ...
>>> Done
</pre>

* Make sure that your proxy server, if any, is configured to allow traffic at ProSoft's default communication ports: 4096 and 6650

* Check the security settings of the server before starting to add users that will have access to the system. The users should have *Read*, *Write*, and *Execute* privileges

</span>

## Post-Installation Verification

After completing the installation and configuration, verify that ProSoft is operating correctly:

### Service Status Verification

<pre id="cmdln-text">
C:\ProSoft\admin> prosoftctl status
>>> ProSoft Core Service: RUNNING (PID: 1234)
>>> ProSoft API Server: RUNNING (PID: 1235)
>>> ProSoft Web Interface: RUNNING (PID: 1236)
>>> Database Connection: CONNECTED (PostgreSQL 14.5)
>>> License Status: VALID (25 seats, expires 2025-12-31)
</pre>

### Web Interface Test

1. Open a web browser and navigate to `https://your-server:8080`
2. Log in using the default administrator credentials:
   - **Username:** `prosoftadmin`
   - **Password:** `ProSoft2024!` (change immediately after first login)
3. Verify the dashboard loads and displays system statistics

### API Connectivity Test

<pre id="cmdln-text">
C:\> curl -k -X GET "https://your-server:4096/api/v1/health" -H "Authorization: Bearer YOUR_API_KEY"
>>> {"status":"healthy","version":"8.4.11","uptime":"00:05:23","database":"connected"}
</pre>

### Performance Baseline Test

<pre id="cmdln-text">
C:\ProSoft\admin> prosoftctl benchmark --quick
>>> Running performance baseline...
>>> Build processing: 450 builds/hour (target: >400)
>>> API response time: 85ms average (target: <100ms)  
>>> Database query time: 12ms average (target: <50ms)
>>> Memory usage: 2.1GB (limit: 4GB for this configuration)
>>> Disk I/O: 1200 IOPS (target: >1000)
>>> RESULT: All benchmarks PASSED
</pre>

## Troubleshooting

### Common Installation Issues

| Problem | Symptoms | Solution |
|---------|----------|----------|
| **Insufficient Permissions** | Installation fails with "Access Denied" | Run installer as Administrator; ensure UAC is temporarily disabled |
| **Port Conflicts** | Service fails to start, port binding errors | Check if ports 4096, 6650, 8080 are available using `netstat -an` |
| **Database Connection Failed** | Cannot connect to database during setup | Verify database server is running and credentials are correct |
| **License Validation Failed** | "Invalid license" error on startup | Check internet connectivity; verify license file integrity |
| **Insufficient Disk Space** | Installation stops at 75% completion | Free up additional space; minimum 2GB required beyond listed requirements |

### Installation Log Locations

- **Windows:** `C:\ProgramData\ProSoft\Logs\install.log`
- **Linux:** `/var/log/prosoft/install.log`

### Service Management Commands

<pre id="cmdln-text">
# Start ProSoft services
C:\ProSoft\admin> prosoftctl start

# Stop ProSoft services  
C:\ProSoft\admin> prosoftctl stop

# Restart ProSoft services
C:\ProSoft\admin> prosoftctl restart

# View real-time logs
C:\ProSoft\admin> prosoftctl logs --follow

# Check configuration validity
C:\ProSoft\admin> prosoftctl config --validate
</pre>

---

## License Terms

This software is valid for one major upgrade amd all the minor upgrades in between. The number of seats is limited to 25 for the *Professional* and 50 for the *Enterprise* versions. In order to renew licenses or add more seats, please visit our [licensing page](https://www.profost.com/licensing).
