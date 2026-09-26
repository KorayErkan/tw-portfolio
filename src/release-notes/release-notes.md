# Nordvale Server 8.5.0 Release Notes

**Release date:** 2026-08-18
**Previous version:** 8.4.11

This document describes the changes in Nordvale Server 8.5.0.

> **Note:** Nordvale, its products, and all hostnames in this document are fictitious. This is a portfolio sample.

## Table of contents

* [About this release](#about-this-release)
* [Upgrade requirements](#upgrade-requirements)
  * [Before you upgrade](#before-you-upgrade)
  * [Upgrade procedure](#upgrade-procedure)
  * [After you upgrade](#after-you-upgrade)
* [Summary of changes](#summary-of-changes)
  * [New features](#new-features)
  * [Performance improvements](#performance-improvements)
  * [Security fixes](#security-fixes)
  * [Permission changes](#permission-changes)
  * [Bug fixes](#bug-fixes)
  * [Deprecations](#deprecations)
* [Known issues](#known-issues)

---

## About this release

Nordvale Server 8.5.0 is a minor release. It adds features, raises the repository size limit, fixes four security vulnerabilities, and fixes a number of defects reported against 8.4.x.

The release is backward compatible with 8.4.x configuration files (`*.scf`), license files, and project data: no manual migration is required. The features listed under [Deprecations](#deprecations) still work in 8.5.0 but log a warning when used, and they will be removed in Nordvale Server 9.0.

All customers running 8.0.0 through 8.4.11 should upgrade because of the [security fixes](#security-fixes) in this release.

## Upgrade requirements

You can upgrade to 8.5.0 directly from any 8.3.x or 8.4.x release. To upgrade from an earlier release, first upgrade to 8.4.11.

The following requirements changed in this release:

| Requirement | 8.4.x | 8.5.0 |
|-------------|-------|-------|
| Operating system | Windows Server 2019, 2022 | Unchanged |
| .NET Runtime | 6.0 | **8.0 (LTS)**; .NET 6 is no longer supported |
| PostgreSQL | 12 to 15 | **13 to 16**; PostgreSQL 12 is no longer supported |
| Microsoft SQL Server | 2019, 2022 | Unchanged |
| Memory | 16 GB (Standard, up to 10 users), 32 GB (Professional, 11&ndash;25 users), 64 GB (Enterprise, 26&ndash;250 users) | Unchanged |

Install the .NET 8 Runtime, and upgrade PostgreSQL if necessary, *before* you run the 8.5.0 installer. The installer stops if either requirement is not met.

### Before you upgrade

1. Schedule a maintenance window. A typical upgrade takes 1 to 2 hours, most of which is the database schema update.
2. Download `nordvale_x64.msi` for 8.5.0 from the [downloads](https://www.nordvale.example/downloads) page.
3. Open PowerShell as an administrator, stop the Nordvale services, and back up the configuration, license, and certificates:

   ```powershell
   Set-Location "C:\Program Files\Nordvale\admin"
   .\nordvalectl.exe stop

   $backupDir = "D:\Backups\Nordvale_$(Get-Date -Format 'yyyyMMdd')"
   New-Item -ItemType Directory -Path $backupDir
   Copy-Item -Path "C:\Program Files\Nordvale\config" -Destination "$backupDir\config" -Recurse
   Copy-Item -Path "C:\Program Files\Nordvale\license" -Destination "$backupDir\license" -Recurse
   Copy-Item -Path "C:\Program Files\Nordvale\certs" -Destination "$backupDir\certs" -Recurse
   ```

4. Back up the database. For PostgreSQL:

   ```powershell
   pg_dump --format=custom --file="$backupDir\nordvale_db.dump" nordvale
   ```

### Upgrade procedure

Run the 8.5.0 installer from the folder that contains it. The installer upgrades the existing installation in place and keeps your configuration, license, and certificates.

```powershell
Start-Process msiexec.exe -Wait -ArgumentList '/i nordvale_x64.msi INSTALLDIR="C:\Program Files\Nordvale" /qn /l*v nordvale_upgrade.log'
```

### After you upgrade

1. Check the service status with `.\nordvalectl.exe status`. The output should report version 8.5.0.
2. Review user permissions. Because of the [permission changes](#permission-changes), users with the Supervisor role can now edit user-scope settings.
3. Check your integrations (issue tracker, Microsoft Teams, webhooks).
4. Run `.\nordvalectl.exe benchmark --quick` to record a new performance baseline.

## Summary of changes

### New features

#### Repositories and version control

* **Larger repositories:** The maximum repository size is raised from 16 GB to 64 GB.
* **Semantic versioning for Git and Subversion:** Version numbers are now updated automatically from tags and commit messages in Git and Subversion repositories.
* **Document viewer:** The management console displays PDF, DOCX, and XLSX files without an external application.

#### Builds

* **Build cache:** Build outputs of unchanged modules are reused across builds. See [Performance improvements](#performance-improvements) for measured results.
* **Additional build agents:** Build agents installed on other Windows servers can now connect to the communications port (6650) and share the build queue.
* **Workflow builder:** A visual editor in the web interface creates CI/CD pipelines without editing pipeline files by hand.

#### Security and compliance

* **Single sign-on:** SAML 2.0 and OpenID Connect are supported in addition to Active Directory and LDAP.
* **Tamper-evident audit log:** Each audit log entry now includes a hash of the previous entry, so that deleted or altered entries can be detected. Use `.\nordvalectl.exe audit --verify` to check the log.
* **Code scanning gates:** A pipeline can now fail a build when an integrated static analysis tool reports findings above a configured severity.

#### Reporting and notifications

* **Technical debt charts:** The dashboard shows technical debt per module against the targets set for the project.
* **Notifications:** Build and pipeline notifications can be sent to Microsoft Teams channels, e-mail, and webhooks.

### Performance improvements

The following results were measured on a Professional edition reference server (8 cores, 32 GB RAM) with a project of about 500,000 lines of code and 60,000 commits.

| Measurement | 8.4.11 | 8.5.0 |
|-------------|--------|-------|
| Average build time (build cache enabled) | 12 min | 5.5 min |
| Median REST API response time | 320 ms | 85 ms |
| Dashboard load time | 45 s | 3.5 s |

Results depend on hardware, project size, and how many modules change between builds.

### Security fixes

| ID | Severity | Affected versions | Description |
|----|----------|-------------------|-------------|
| NVS-2026-0012 | Critical | 8.0.0 to 8.4.11 | SQL injection in the login form allowed an unauthenticated attacker to read user records. |
| NVS-2026-0013 | High | 8.2.0 to 8.4.11 | Stored cross-site scripting (XSS) in dashboard widget titles. |
| NVS-2026-0014 | Medium | 8.3.0 to 8.4.11 | Reflected cross-site scripting (XSS) in the report export page. |
| NVS-2026-0015 | High | 8.0.0 to 8.4.11 | Session fixation: session tokens were not rotated after login. Tokens are now rotated at login and every 30 minutes. |

There are no workarounds for these vulnerabilities. Upgrade to 8.5.0.

### Permission changes

* **Editing user-scope settings (#4322):** Editing the `USER` options of a complex property in a `*.scf` file no longer requires the Admin role; the Supervisor role is sufficient. `ADMIN` and `SYSTEM` options still require the Admin role. This change follows the principle of least privilege: supervisors no longer need full administrative rights to adjust user defaults.

### Bug fixes

#### Configuration files

* Enumerated constants written with dot notation (for example, `compression = Compression.lz4`) no longer cause a parse error in `*.scf` files. (#4321)
* Component names with three or more levels (for example, `[a.b.c]`) are now parsed correctly. (#5321)
* The document viewer now opens each file with the application associated with its file type. (#5323)

#### Performance and stability

* Fixed a memory leak in the build engine that slowed builds down after several days without a restart. (#3201)
* Fixed inefficient database queries that delayed loading of projects larger than 10 GB by 5 to 8 seconds. (#3202)
* Fixed a race condition that caused some parallel builds to fail. (#3203)

#### Web interface

* Fixed slow dashboard rendering for projects with more than 50,000 commits. (#4101)
* Fixed layout problems in the web interface on tablet-sized screens. (#4102)
* Fixed inconsistent colors in dark mode. (#4103, #4104)

#### Integrations and REST API

* Fixed timeouts on REST API responses larger than 10 MB. (#6101)
* Fixed webhook deliveries that were dropped during periods of high load. Failed deliveries are now retried up to five times. (#6102)
* Fixed gaps in commit history after synchronizing Git repositories. (#6103)
* The health check endpoint (`/api/v1/health`) now reports `maintenance` instead of `healthy` during scheduled maintenance. (#7102)

#### Reporting

* Fixed report generation timeouts for projects with more than 100,000 commits. (#8101)
* Fixed incorrect values in trend charts and burn-down reports. (#8102, #8103)

### Deprecations

The following features are deprecated in 8.5.0. They still work but log a warning when used, and they will be removed in Nordvale Server 9.0.

| Deprecated feature | Replacement |
|--------------------|-------------|
| Assigning team members to a fixed team lead | Teams are now created at the top level, without a team lead |
| Single-hierarchy project directories | Modules can be grouped at any level of the project |
| Regrouping lower-level modules by group identity | Group identity is now assigned automatically and inherited from the top level |

## Known issues

The following issues are known in this release.

* Ownership tracking:
  * When the owner of a source file changes their name, ID, or e-mail address, the system does not update the database and loses track of the owner, orphaning the source files. (#1234)
  * When ownership of a source file is delegated to a user who does not exist in the database, the file becomes orphaned without a warning, although the tracking system displays the new owner's ID. (#1235)
  * Once ownership of a resource has been delegated, it cannot be delegated again to another user. (#1236)
  * When a delegated source file is deleted without a commit, its earlier versions remain in the system and cannot be removed from the trunk. (#1237)
* Configuration files:
  * The system reads only `*.scf` configuration files; XML-based configuration files are not recognized. (#2345)
  * In a complex property, a quoted string that contains a semicolon, for example `{DEFAULT: "a;b"}`, is split at the semicolon. Workaround: avoid semicolons in quoted option values. (#2347)

These issues will be addressed in a future release.

---

&copy; Nordvale Corporation 2026. All information contained herein is provided "AS IS". Although Nordvale is committed to making sure that this information is up to date and accurate, it makes no claims or representations in these regards.
