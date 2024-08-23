# ProSoft v8.4.11 System Configuration Guide

This document includes ProSoft proprietary or confidential information and may not be redistributed or disclosed without prior written permission.

All information contained herein is provided "*AS IS*" based on the state of the ProSoft system as of the release date. ProSoft reserves the right to make changes to this document without prior notice.

## Disclaimer

NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, IS MADE IN RELATION TO THE CONTENTS OF THIS DOCUMENT REGARDING INCLUDING BUT NOT LIMITED TO AVAILABILITY, ACCURACY, RELIABILITY, NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PURPOSE. IN NO EVENT SHALL PROSOFT BE LIABLE FOR ANY DAMAGES, INCLUDING BUT NOT LIMITED TO DIRECT, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR DUE TO BUSINESS INTERRUPTION, OR ANY LOSS OF PROFIT, REVENUE, BUSINESS OPPORTUNITY, OR DATA THAT MAY ARISE FROM THE USE OF THE INFORMATION IN THIS DOCUMENT.

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

## About this guide

This guide was prepared to aid administrators in configuring, administrating, and troubleshooting the software system. It is assumed that the software system has been installed previously with the required hadrware configuration and networking infrastructure.

## Preliminary tasks

In order for the configuration procedure to continue without any errors or interruption, the servers where the system was installed, the network devices to be used to access the server and the clients, and the licenses and certificates required to use the software system must be ready and in place. To meet these prerequisites, follow the instructions below.

### Server requirements

The system has to be installed on a server that meets the following minimum hardware requirements:

* 7 quad-core 64-bit AMD processors
* 128 GB RAM
* A 2 TB SSD
* 2 x 1 TB SCSI hard drives for redundancy

### Networking

Since the system will be accessed over a network, the following networking hardware must be in place and in working condition:

* A 1000BASE-T (i.e. gigabit) Ethernet
* A proxy to manage the server traffic listening on port 9595
* TCP/IP protocol in place on the server

### Licenses and certificates

During the configuration of the system, licenses and certificates will be required for the system to validate the installation and give access to administrative users. Make sure

* the licenses (i.e. the 2 `*.lic` files) are in the root directory where the server is to be installed
* the authentification certificates are in the `./cert` directory under the root

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
C:\>cd \ProSoft\admin
C:\ProSoft\admin>
</pre>

* At this point, you should have the licenses (the `*.lic` files) under the root&mdash;i.e. the `C:\ProSoft\` directory&mdash;and the certificates (the `*.cert` files) under the `C:\ProSoft\admin\` directory. Run the script named `sys_config.ps` and check the output messages

<pre id="cmdln-text">
C:\>ProSoft\admin\sys_config.ps
>>> Configuring system...
>>> Licenses discovered
>>> Certificates discovered
>>> Disks partitioned: 100%
>>> Indexes created
>>> Done
C:\>ProSoft\admin
</pre>

* If any of these messages do not appear, you should suspend the configuration procedure and troubleshoot. For this, see the [Troubleshooting](#troubleshooting) section below
* After the script has completed, you can exit the terminal
</span>

## System initialization

Before it can be used, the system has to be initialized to verify that its configured state is intact and that all the resources and connections it needs are in place and accessible. The initialization process is carried out as follows.

<span id="cli-byline">

To carry out system initialization using the command line,

* Open a terminal with elevated privileges and navigate to the admin directory
* Run the `sys_init.ps` script entering the required directories, and check the output

<pre id="cmdln-text">
C:\>cd \ProSoft\admin
C:\ProSoft\admin>sys_init.ps --cert-dir=..\cert --licence-files=.\purchased.lic
>>> Initializing system...
>>> Looking for licenses...
</pre>

As the system proceeds with initialization, the status is reported on the command prompt:

<pre id="cmdln-text">
C:\>cd \ProSoft\admin
C:\ProSoft\admin>sys_init.ps --cert-dir=..\cert --licence-files=.\purchased.lic
>>> Initializing system...
>>> Licenses: Found
>>> Admin module: OK
>>> Users module initializing: \ 97%
</pre>

If any of the required files&mdash;e.g. certificates&mdash;are missing, the initialization procedure halts, and prompts what needs to be done:

<pre id="cmdln-text">
C:\>cd \ProSoft\admin
C:\ProSoft\admin>sys_init.ps --cert-dir=..\cert --licence-files=.\purchased.lic
>>> Initializing system...
>>> Licenses: Found
>>> Admin module: OK
>>> Users module: OK
>>> Networking module initializing: 24% -> ERROR
    Certificate(s) required to initialize the module missing.
    Place a valid certificate in the "..\cert" directory: Resume? [Y/N]
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
* Navigate to the root directory
</span>

### Troubleshooting

An essential part of system administration and maintanence is diagnosing the root causes of issues and resolving them. All troubleshooting must be done using the following general procedure:

* Check the __error code__ and the __error message__: Every error report provides a specific error id and a message explaining the exceptional that has been raised. The message will provide hints on how to proceed
* Find the __error code__ in the lookup table attached to this guide: The list of error codes contain useful hints about the source and possible causes of the error
* Follow the instructions for diagnosing the root cause of the problem: The error code table provides possible actions and workarounds to resolve the issue
* If the error persists, consult the hot line for expert advice from __ProSoft__

### Decommissioning

If for some reason the system fails to meet your needs, there are a number of steps to take to decommission it. These are:

* Running the `.\admin\decomm_sys.ps` script to gather information about the current state of the resources the system has been using in order to generate a report
* Backing up all this legacy data based on the report generated
* Releasing the certificates
* Removing the licenses
* Uninstalling the software
