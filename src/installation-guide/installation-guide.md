# Nordvale&trade; Server Installation Guide

This document describes the system requirements of Nordvale Server 8.5.0 and the procedure for installing it.

## Disclaimer

NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, IS MADE IN RELATION TO THE CONTENTS OF THIS DOCUMENT, INCLUDING BUT NOT LIMITED TO AVAILABILITY, ACCURACY, RELIABILITY, NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PURPOSE. IN NO EVENT SHALL NORDVALE BE LIABLE FOR ANY DAMAGES, INCLUDING BUT NOT LIMITED TO DIRECT, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR DUE TO BUSINESS INTERRUPTION, OR ANY LOSS OF PROFIT, REVENUE, BUSINESS OPPORTUNITY, OR DATA THAT MAY ARISE FROM THE USE OF THE INFORMATION IN THIS DOCUMENT.

---

## Copyright

__Nordvale__ is a registered trademark of Nordvale Corporation. Other products mentioned in this document may be trademarks of their respective owners.

This document is subject to change without prior notice.

&copy; Nordvale Corporation 2026.

> __Note:__ Nordvale, its products, and all hostnames in this document are fictitious. This is a portfolio sample.

---

## Table of contents

* [Introduction](#introduction)
* [System requirements](#system-requirements)
  * [Operating system](#operating-system)
  * [Hardware](#hardware)
  * [Network ports](#network-ports)
  * [Dependencies](#dependencies)
* [Installation](#installation)
  * [Install with the setup wizard](#install-with-the-setup-wizard)
  * [Install from the command line](#install-from-the-command-line)
* [Configuration](#configuration)
  * [Install the license](#install-the-license)
  * [Install the certificates](#install-the-certificates)
* [Post-installation verification](#post-installation-verification)
* [Troubleshooting](#troubleshooting)
* [License terms](#license-terms)

---

## Introduction

__Nordvale Server__ is an engineering solution for managing CI/CD pipeline automation in software development. The system keeps track of the modifications and additions made to the codebase&mdash;including acceptance, unit, and integration tests&mdash;and the commits to source control, creates an automated pipeline for building release candidates, updates version numbers using *semantic versioning*, calculates *technical debt* against targets, and charts the progress of various aspects of the project to provide a global picture.

## System requirements

### Operating system

Nordvale Server 8.5.0 is distributed as a 64-bit Windows Installer package (`nordvale_x64.msi`) and runs on the following operating systems only.

| Operating system | Version | Architecture |
|------------------|---------|--------------|
| Windows Server 2022 | Build 20348 or later | x64 |
| Windows Server 2019 | Build 17763 or later | x64 |

### Hardware

Size the server according to your license edition, which determines the maximum number of users (seats).

| Component | Standard (up to 10 users) | Professional (11&ndash;25 users) | Enterprise (26&ndash;250 users) |
|-----------|---------------------------|----------------------------------|---------------------------------|
| __CPU__ | 4 cores, 2.5 GHz or faster | 8 cores, 2.5 GHz or faster | 16 cores, 2.5 GHz or faster |
| __Memory__ | 16 GB | 32 GB | 64 GB ECC |
| __Storage__ | 250 GB SSD | 500 GB NVMe SSD | 1 TB NVMe SSD, RAID 1 |
| __Network__ | 1 Gigabit Ethernet | 1 Gigabit Ethernet | 10 Gigabit Ethernet |

In addition to the storage listed above, the installer requires 2 GB of free space on the system drive.

### Network ports

The web interface and REST API are published on port 443 by IIS, which acts as a reverse proxy on the same server. IIS terminates TLS and forwards requests to the Nordvale Web Service, which listens only on the loopback address at `https://127.0.0.1:8443`. Build agents connect directly to the communications port, 6650.

| Port | Protocol | Direction | Purpose |
|------|----------|-----------|---------|
| 443 | HTTPS | Inbound | Web interface and REST API (`/api/v1`), through the IIS reverse proxy |
| 443 | HTTPS | Outbound | License validation and update checks (`licensing.nordvale.example`) |
| 6650 | TCP (TLS) | Inbound | Communications port for build agents and desktop clients |
| 8443 | HTTPS | Local only | Nordvale Web Service (loopback); do not open in the firewall |
| 5432 | TCP | Outbound | PostgreSQL database, if hosted on another server |
| 1433 | TCP | Outbound | Microsoft SQL Server database, if hosted on another server |

The installer creates the inbound firewall rules for ports 443 and 6650. To create them manually, run the following commands in an elevated PowerShell session:

```powershell
New-NetFirewallRule -DisplayName "Nordvale Web (HTTPS)" -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow
New-NetFirewallRule -DisplayName "Nordvale Communications" -Direction Inbound -Protocol TCP -LocalPort 6650 -Action Allow
```

### Dependencies

The installer checks for the following components and stops if any required component is missing.

#### Required components

| Component | Version | Purpose |
|-----------|---------|---------|
| __Microsoft Visual C++ Redistributable (x64)__ | 2015&ndash;2022 (14.29 or later) | Runtime libraries for native components |
| __Microsoft .NET Runtime (x64)__ | 8.0 (LTS) | Application runtime |
| __Internet Information Services (IIS)__ | 10.0, with URL Rewrite 2.1 and Application Request Routing 3.0 | Reverse proxy and TLS termination on port 443 |
| __Database server__ | See the next table | Persistent data storage |

#### Supported databases

| Database | Supported versions | Notes |
|----------|--------------------|-------|
| __PostgreSQL__ | 13 to 16 | Recommended for new installations |
| __Microsoft SQL Server__ | 2019, 2022 | Standard or Enterprise edition |

#### Optional components

| Component | Version | Benefit |
|-----------|---------|---------|
| __Redis__ | 6.2 or later | Shared cache for the REST API |
| __Elasticsearch__ | 8.x | Full-text search across build logs |

The system locale is *en-US* by default. You can select any other supported locale during installation.

## Installation

Before you start the installation:

1. Check that the [required components](#required-components) are installed.
2. From the Nordvale [downloads](https://www.nordvale.example/downloads) page, download the `nordvale_x64.msi` file to the `Downloads` folder of the administrator account on the server.

By default, Nordvale Server is installed in `C:\Program Files\Nordvale`. It is strongly recommended that you do *not* change this directory.

### Install with the setup wizard

__Using the GUI__

1. Open __File Explorer__ and navigate to the __Downloads__ folder.
2. Double-click the `nordvale_x64.msi` file to start the setup wizard. If User Account Control prompts you, click __Yes__.
3. Accept the license agreement and keep the default installation directory, `C:\Program Files\Nordvale`.
4. On the __Configuration__ page, review the settings. Leave the default values for cache size, data disk size, and communications port (6650) unless you have a good reason to change them.
5. On the __Locale__ page, keep *en-US* or select another locale.
6. Click __Install__ to start the installation. Because the system creates data partitions during this stage, it may take up to 15 minutes to complete.
7. Click __Finish__.

### Install from the command line

__Using the CLI__

1. Open PowerShell as an administrator (right-click __Windows PowerShell__ and select __Run as administrator__).
2. If you have not downloaded the installation package yet, download it and change to the `Downloads` folder:

   ```powershell
   Set-Location "$env:USERPROFILE\Downloads"
   Invoke-WebRequest -Uri "https://www.nordvale.example/downloads/nordvale_x64.msi" -OutFile "nordvale_x64.msi"
   ```

3. Run the installer silently with the default settings, writing a verbose log to the current folder:

   ```powershell
   Start-Process msiexec.exe -Wait -ArgumentList '/i nordvale_x64.msi INSTALLDIR="C:\Program Files\Nordvale" /qn /l*v nordvale_install.log'
   ```

   To override a default, add the corresponding property to the argument list, for example `LOCALE=en-GB`. The following properties are available:

   | Property | Default | Description |
   |----------|---------|-------------|
   | `INSTALLDIR` | `C:\Program Files\Nordvale` | Installation directory |
   | `CACHE_SIZE` | `4096MB` | Application cache size |
   | `DATA_DISK_SIZE` | `50GB` | Initial size of the data partition |
   | `COMMS_PORT` | `6650` | Communications port for build agents and clients |
   | `WEB_PORT` | `8443` | Local port of the Nordvale Web Service (behind IIS) |
   | `LOCALE` | `en-US` | System locale |

4. Wait for the command to return. Because the system creates data partitions during this stage, it may take up to 15 minutes. A return code of 0 in the log file means that the installation succeeded.

> __Note:__ The `msiexec` arguments are wrapped in single quotes so that PowerShell passes the quoted `INSTALLDIR` path to the installer unchanged. If you use Command Prompt instead, run `msiexec /i nordvale_x64.msi INSTALLDIR="C:\Program Files\Nordvale" /qn /l*v nordvale_install.log`.

## Configuration

After the installation is complete, install the license and the certificates. Both tasks are performed from an elevated PowerShell session with the scripts in the `admin` subdirectory of the installation directory. The scripts are signed, so they run under the default `RemoteSigned` execution policy of Windows Server.

### Install the license

__Using the CLI__

1. Copy the `nordvale.lic` file that you received by e-mail to the `license` subdirectory of the installation directory:

   ```powershell
   Copy-Item -Path "$env:USERPROFILE\Downloads\nordvale.lic" -Destination "C:\Program Files\Nordvale\license\"
   ```

2. Change to the `admin` directory and run the `install_lic.ps1` script:

   ```powershell
   Set-Location "C:\Program Files\Nordvale\admin"
   .\install_lic.ps1 -LicenseFile "C:\Program Files\Nordvale\license\nordvale.lic"
   ```

   Expected output:

   ```text
   Installing license...
   License installed: Professional, 25 seats
   Done
   ```

> __Note:__ If you skip this step, Nordvale Server prompts you for the license file the first time you open the web interface.

### Install the certificates

Nordvale Server needs a server certificate, its private key, and the certificate chain of the issuing certificate authority (CA). In this example, the files are `server.crt`, `server.key`, `intermediate.crt`, and `root.crt`.

__Using the CLI__

1. Copy the certificate files to the `certs` subdirectory of the installation directory:

   ```powershell
   Copy-Item -Path "$env:USERPROFILE\Downloads\*.crt", "$env:USERPROFILE\Downloads\server.key" -Destination "C:\Program Files\Nordvale\certs\"
   ```

2. From the `admin` directory, run the `install_cert.ps1` script. The script validates the chain, imports the server certificate into the `LocalMachine\My` store, and binds it to the IIS site on port 443 and to the communications port:

   ```powershell
   .\install_cert.ps1 -CertDir "C:\Program Files\Nordvale\certs"
   ```

   Expected output:

   ```text
   Installing certificates...
   Certificate chain: valid (server.crt -> intermediate.crt -> root.crt)
   IIS binding on port 443: updated
   Done
   ```

3. If a proxy or firewall sits between the build agents and the server, allow traffic to port 6650.
4. Before you add users, check that the Nordvale service account has *Read*, *Write*, and *Execute* permissions on `C:\Program Files\Nordvale` and `C:\ProgramData\Nordvale`.

## Post-installation verification

After you complete the installation and configuration, verify that Nordvale Server is operating correctly.

### Check the service status

Run the following command from the `admin` directory:

```powershell
.\nordvalectl.exe status
```

Expected output:

```text
Nordvale Core Service:     RUNNING (PID 1234)
Nordvale Web Service:      RUNNING (PID 1235, https://127.0.0.1:8443)
Communications listener:   RUNNING (port 6650)
Database connection:       CONNECTED (PostgreSQL 16.4)
License status:            VALID (Professional, 25 seats, expires 2027-12-31)
```

### Test the web interface

1. Open a web browser and navigate to `https://nordvale.corp.example` (replace this with the host name of your server).
2. Log in as `nvadmin`. The one-time initial password is stored in `C:\ProgramData\Nordvale\initial-admin-password.txt`, and you must change it when you first log in.
3. Verify that the dashboard loads and displays system statistics.

### Test the REST API

```powershell
Invoke-RestMethod -Uri "https://nordvale.corp.example/api/v1/health" -Headers @{ Authorization = "Bearer <api-key>" }
```

Expected output:

```text
status  version uptime   database
------  ------- ------   --------
healthy 8.5.0   00:05:23 connected
```

### Run a performance baseline

```powershell
.\nordvalectl.exe benchmark --quick
```

Expected output:

```text
Running performance baseline...
Build processing:   450 builds/hour (target: > 400)
API response time:  85 ms average (target: < 100 ms)
Database query:     12 ms average (target: < 50 ms)
Memory usage:       2.1 GB (limit for this edition: 8 GB)
RESULT: All benchmarks PASSED
```

## Troubleshooting

### Common installation issues

| Problem | Symptoms | Solution |
|---------|----------|----------|
| __Insufficient permissions__ | Installation fails with "Access Denied" | Run the installer from an elevated prompt (__Run as administrator__) |
| __Port conflicts__ | A service fails to start with a port binding error | Check whether ports 443, 6650, and 8443 are in use: `Get-NetTCPConnection -LocalPort 443,6650,8443` |
| __Database connection failed__ | Setup cannot connect to the database | Verify that the database server is running and that the credentials are correct |
| __License validation failed__ | "Invalid license" error on startup | Check outbound HTTPS access to `licensing.nordvale.example`; verify that `nordvale.lic` is intact |
| __Insufficient disk space__ | Installation stops at 75% | Free up space; the installer needs 2 GB on the system drive in addition to the data storage |

### Log file locations

| Log | Location |
|-----|----------|
| Installer log (command-line installation) | The file passed to `/l*v`, for example `nordvale_install.log` in the current folder |
| Installer log (setup wizard) | `%TEMP%\MSI*.log` |
| Service logs | `C:\ProgramData\Nordvale\logs\` |

### Service management commands

Run these commands from `C:\Program Files\Nordvale\admin` in an elevated PowerShell session.

| Task | Command |
|------|---------|
| Start the services | `.\nordvalectl.exe start` |
| Stop the services | `.\nordvalectl.exe stop` |
| Restart the services | `.\nordvalectl.exe restart` |
| View live logs | `.\nordvalectl.exe logs --follow` |
| Validate the configuration | `.\nordvalectl.exe config --validate` |

---

## License terms

Each license is valid for the licensed major version, all minor and patch releases of that version, and one major upgrade. The number of seats is limited to 10 for the *Standard*, 25 for the *Professional*, and 250 for the *Enterprise* edition. To renew licenses or add more seats, visit the [licensing page](https://www.nordvale.example/licensing).
