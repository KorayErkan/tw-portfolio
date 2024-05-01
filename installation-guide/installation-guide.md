# __ProSoft__&trade; Installation Guide

This document provides information about the system requirements of ProSoft v5.3.14, as well as the procedure for installing it.

## Table of Contents

* [Introduction](#introduction)
* [System Requirements](#system-requirements)
  * [Hardware](#hardware)
  * [Dependencies](#dependencies)
* [Installation](#installation)
* [Configuration](#configuration)
* [License Terms](#license-terms)

## Introduction

__ProSoft__&trade; is an engineering solution for managing CI/CD pipeline automation in software development. The system keeps track of the modifications and additions made to the codebase&mdash;including acceptance, unit, and integration tests&mdash;and the commits to source control, creates an automated pipeline for building release candidates, updates version numbers using *semantic versioning*, calculates *technical debt* based on targets, and charts the progress of various aspects of the project to provide a global picture.

The system is compliant with the requirements and logic of CI/CD as it has been laid out in RFC 3265-A and RFC 3265-B.

## System Requirements

### Hardware

For an average team of 25 developers, the system requires at least 5 x 2.5GHz quadcore 7i processors, 64GB of RAM, and 1TB of disk space.

Also, a 100Base-TX Ethernet network connection is recommended for effective use.

### Dependencies

The installer checks the presence of the following components, and in case any of them is not in place it terminates the installation process:

* Microsoft Visual C++ Redistributable: this is required for the MSVC libraries
* An ANSI SQL compliant database server (such as PostgreSQL 14.5 and above, Microsoft SQL Server 2018 and above, Oracle DBMS 2016 and above, etc.): the system keeps significant amounts of data in a relational database
* Microsoft .NET Framework 5 or higher: the system was developed with .NET and the runtime requires the presence of certain libraries
* Microsoft IIS 11.4 or higher: the system requires an internet connection for managing cloud storage and connecting to our servers for patches and updates

The system locale is *en-us* by default but can be set to any locale.

## Installation

The following steps are based on the 64-bit version, but they are identical for the 32-bit version. Before you start the installation, check that the above-mentioned prerequisite components are in place.

* From the __ProSoft__ [downloads](https://www.prosoft.com/downloads) page, download the `prosoft_x64.msi` file to the `C:\Users\<user-name>\Downloads` directory of your server
* Double-click the file to start the installation and follow the on-screen instructions
* By default, the server is installed in the `C:\Programs\ProSoft` directory. It is strongly recommended that this directory is *not* changed
* Confirm the settings on the configuration page of the installer. It is recommend that the default values for cache size, disk size, API endpoints, communication ports, and others are left as they are unless you have a good reason to change them
* If you need to change the locale setting, you will be prompted to select one on the next page of the installer
* Finally, click `Ok` to start the installation process. Because the system creates partitions for more efficient marshalling of data, it may take up to 15 for this stage to complete.

## Configuration

After the installation process completes

* Copy the `prosoft.lic` file sent to you via e-mail to the `bin` subdirectory of the installation folder. You will be prompted the first time you launch the program to point to this file for activation
* Install the security certificates the system needs under the `cert` subdirectory of the installation folder
* Make sure that your proxy server, if any, is configured to allow traffic at ProSoft's default communication ports: 4096 and 6650
* Check the security settings of the server before starting to add users that will have access to the system. The users should have Read, Write, and Execute privileges

## License Terms

This software is valid for one major upgrade amd all the minor upgrades in between. The number of seats is limited 25 for the *Professional* and 50 for the *Enterprise* versions. In order to renew licenses or add more seats, please visit our [licensing page](https://www.profost.com/licensing).

---

This document is __ProSoft__&copy; 2024 and its contents is subject to change without prior notice.
