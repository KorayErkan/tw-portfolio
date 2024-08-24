# __ProSoft__&trade; Installation Guide

This document provides information about the system requirements of ProSoft v8.4.11, as well as the procedure for installing it.

## Disclaimer

NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, IS MADE IN RELATION TO THE CONTENTS OF THIS DOCUMENT REGARDING INCLUDING BUT NOT LIMITED TO AVAILABILITY, ACCURACY, RELIABILITY, NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PURPOSE. IN NO EVENT SHALL PROSOFT BE LIABLE FOR ANY DAMAGES, INCLUDING BUT NOT LIMITED TO DIRECT, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR DUE TO BUSINESS INTERRUPTION, OR ANY LOSS OF PROFIT, REVENUE, BUSINESS OPPORTUNITY, OR DATA THAT MAY ARISE FROM THE USE OF THE INFORMATION IN THIS DOCUMENT.

## Copyright

__ProSoft__ is registered trademark of ProSoft Corporation. Other products mentioned in this document may be trademarks of their respective owners. This document is is subject to change without prior notice.

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
C:\> winget www.prosoft.com/downloads/prosoft_x64.msi
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

* It is recommend that the default values for cache size, disk size, API endpoints, communication ports, and others are left as they are unless you have a good reason to change them. To confirm these settings, type `Y` (for __Yes__) for each when prompted on the command line

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

After the installation process completes,

* Copy the `prosoft.lic` file sent to you via e-mail to the `bin` subdirectory of the installation folder. You will be prompted the first time you launch the program to point to this file for activation
* Install the security certificates the system needs under the `cert` subdirectory of the installation folder
* Make sure that your proxy server, if any, is configured to allow traffic at ProSoft's default communication ports: 4096 and 6650
* Check the security settings of the server before starting to add users that will have access to the system. The users should have *Read*, *Write*, and *Execute* privileges

## License Terms

This software is valid for one major upgrade amd all the minor upgrades in between. The number of seats is limited 25 for the *Professional* and 50 for the *Enterprise* versions. In order to renew licenses or add more seats, please visit our [licensing page](https://www.profost.com/licensing).
