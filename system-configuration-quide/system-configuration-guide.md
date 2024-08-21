# ProSoft v8.4.11 System Configuration Guide

This document includes ProSoft proprietary or confidential information and may not be redistributed or disclosed without prior written permission.

All information herein is provide "*AS IS*" based on the state of the ProSoft system as of the release date. ProSoft reserves the right to make changes to this document without prior notice.

## Disclaimer

NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, IS MADE IN RELATION TO THE CONTENTS OF THIS DOCUMENT REGARDING INCLUDING BUT NOT LIMITED TO AVAILABILITY, ACCURACY, RELIABILITY, NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PURPOSE. IN NO EVENT SHALL PROSOFT BE LIABLE FOR ANY DAMAGES, INCLUDING BUT NOT LIMITED TO DIRECT, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR DUE TO BUSINESS INTERRUPTION, OR ANY LOSS OF PROFIT, REVENUE, BUSINESS OPPORTUNITY, OR DATA THAT MAY ARISE FROM THE USE OF THE INFORMATION IN THIS DOCUMENT.

## Copyright

__ProSoft__ is registered trademark of ProSoft Corporation. Other products mentioned in this document may be trademarks of their respective owners.

&copy; ProSoft 2024.

---

## Table of Contents

* [About this guide](#about-this-guide)
* [Preliminary tasks](#preliminary-tasks)
  * [Server requirements](#server-requirements)
  * [Networking](#networking)
  * [Licenses and certificates](#licenses-and-certificates)
* [Configuration](#configuration)
  * [Using the GUI](#using-the-gui)
  * [Using a CLI](#using-the-cli)
* [System administration](#system-administration)
  * [Availability and provisioning](#availability-and-provisioning)
  * [Troubleshooting](#troubleshooting)
  * [Decommissioning](#decommissioning)

## About this guide

This guide was prepared to aid administrators in installing, configuring, administrating, and troubleshooting the software system.

## Preliminary tasks

In order for the installation procedure to continue without any errors or interruption, the servers to be used for the installation, the network devices to be used to access the server and the clients, and the licenses and certificates required to use the software system must be ready. To meet these prerequisites, follow the instructions below.

### Server requirements

The system has to be installed on a server that meets the following minimum hardware requirements:

* 7 quad-core 64-bit AMD processors
* 128 GB RAM
* A 2 TB SSD
* 2 x 1 TB SCSI hard drives for redundancy

### Networking

Since the system will be accessed over a network, the following must be in place:

* A 1000BASE-T (i.e. gigabit) Ethernet
* A proxy to manage the server traffic listening on port 9595
* TCP/IP protocol in place on the server

### Licenses and certificates

During the installation of the system, licenses and certificates will be required for the system to validate the installation and give access to administrative users. Make sure

* the licenses (i.e. the 2 `*.lic` files) are in the root directory where the server is to be installed
* the authentification certificates are in the `./cert` directory under the root

## Configuration

The system's configuration involves making the correct settings required by the server. This can be done either through the GUI or the CLI.

### Using the GUI

This involves using the application's Administration Console.

* Double-click the __ProSoft__ icon on the desktop to launch the console
* In the console window, pick the __Tools > Settings__ menu item. A window will pop up
* In __Settings__ window, various settings can be found grouped according to the functionality they are related to:
  * The __Users__ group on the left is where you can add or remove users, set their credentials and the security groups they belong to, and assign them the directories under which the resources managed by __ProSoft&copy;__ are located
  * The __Resources__ group in the middle is for setting the directories the system uses to store various resources it generates and manages
  * The __System__ group on the right is for assigning the various values the system uses as defaults for marshalling and managing its data

### Using the CLI

This involves running certain scripts&mdash;found in the `./admin` directory under the root&mdash;through the command line. The script to be run depends on the settings to be configured.

* Launch a terminal with elevated (i.e. __admin__) privileges
* On the command line, navigate to the root directory

```CLI
C:\> cd \ProSoft\admin
```

* Run the script named `init_config.ps` and check the output messages

```CLI
C:\>ProSoft\admin\init_config.ps
Configuring system...
```

## System initialization

The system has to be initialized as follows.

## System administration

The system can be administered by the... sys-admin... duh!

### Availability and provisioning

Availability is measured based on the following criteria:

* The purchased number of seats with the license
* How many seats have been provisioned
* Whether the provisioned seat and the resources available to it are accessible via the network and using the assigned credentials

To provide seats to users, the following procedure must be used:

* Using the __Properties__ menu, open the __Seats__ window
* Check the number of seats used on the left panel. If there are none left, you have to purchase additional seats
* Check the group the user is a member of to see whether it matches the use properties of the available seats
* Assign the user to the seat by filling in his credentials in the middle panel
* Finally, click on the __Provision__ button on the bottom right of the window

### Troubleshooting

Troublingshooting is an essential part of system maintanence. All troubleshooting must be done with the following general procedure:

* Check the error code, error message, and core-dump if any
* Find the error code in the lookup table attached to this guide
* Follow the instructions for diagnosing the root cause of the problem

### Decommissioning

If for some reason the system fails to meet your needs, there are a number of steps to decommission the system:

* Running the `./admin/decomm_sys.ps` script to gather the necessary information on what should be backed up
* Backing up the legacy data based the generated report
* Releasing the certificates
* Removing the license
* Uninstalling the software
