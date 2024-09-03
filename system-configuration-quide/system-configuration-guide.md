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

The system has to be installed on a server that meets the following minimum hardware requirements:

* 2 blades with 8 quad-core 64-bit AMD processors each
* 128 GB RAM
* A 2 TB SSD
* 2 x 1 TB SCSI hard drives for redundancy

> <span id="note-byline">To maintain a robust level of security while managing the traffic, it is strongly advised that the server be placed behind a proxy
> </span>

### Networking

Since the system will be accessed over a network, the following networking hardware must be in place and in working condition:

* A 1000BASE-T (i.e. gigabit) Ethernet
* A proxy to manage the server traffic listening on port 9595
* TCP/IP protocol in place on the server

> <span id="note-byline">All wireless access must be monitored with cybersecurity software as once access is is given to the server system, the software does __not__ perform any further security checks.
> </span>

### Licenses and certificates

During the configuration of the system, licenses (i.e. the `*.lic` files) and certificates (i.e. the `*.cert` files) will be required for the system to validate the installation and give access to users with various roles. Make sure that

* *Licenses* are in the root directory where the server is to be installed&mdash;assuming the default is not changed, that will be `C:\ProSoft`
* *Authentification Certificates* are in the `.\cert` directory under the root

The licensing scheme used by __ProSoft__ is as follows:

|License|Duration|Number of Users|Types|
|-|-|-|-|
|*Enterprise*|1 Year|250|*Admin*, *Auditor*, *Supervisor*, *Client*|
|*Professional*|1 Year|100|*Admin*, *Supervisor*, *Client*|
|*SMB*|1 Year|50|*Admin*,*Client*|

Certificates must be digitally signed by a recognized CA, and must be renewed after expiry dates.

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

* The seats already in use are the ones listed as `*.seat` files with hexadecimal numbers in their names. The file named `prov_config.cfg` contains the relevant data for seat allocation. Find the line in it with the entry `MAX_USER` using `Select-String` to learn the maximum seats available for the license. If the number of `*.seat` files is less than that number, you can provision a seat. If not, you need to purchase additional seats.

<pre id="cmdln-text">
C:\ProSoft\users>Select-String -Pattern "MAX_USER" -Path provision.cfg

provision.cfg:18:MAX_USER=50
</pre>

* The script named `prov_seat.ps` can be run to do this automatically. Running the script with the required parameters will either provision the seat, or, in case there are no available seats, report an error.

<pre id="cmdln-text">
C:\ProSoft\users>prov_seat.cfg --user-type=client
>>> Checking availability ...
>>> Provisioning ...
>>> The seat with the id '747ba03cab6fe9c' was provisioned
</pre>

* If a seat was successfully provisioned, listing the id will show that a new seat file has been created in the directory.

<pre id="cmdln-text">
C:\ProSoft\users>ls '*747ba03cab6fe9c*' | ft Name

cli-747ba03cab6fe9c.seat
</pre>

</span>

### Troubleshooting

An essential part of system administration and maintanence is diagnosing the root causes of issues and resolving them. All troubleshooting must be done using the following general procedure:

* Check the __error code__ and the __error message__: the error dialog provides a specific error number to identify the error, and a message explaining the exception that has been raised. The message will provide hints as to how to proceed
* Find the __error code__ in the lookup table attached to this guide. It contains useful hints about the possible sources of the error
* Follow the instructions for diagnosing the root cause of the problem. The table provides possible actions and workarounds to resolve the issue
* If the error persists, consult the [__ProSoft__ hotline](#prosoft-hotline) for expert advice

### Decommissioning

If for some reason the system fails to meet your needs, there are a number of steps to take to decommission it.

<span id="cli-byline">

To decommission the system,

* Open a terminal window with elevated privileges
* Navigate to `C:\ProSoft\admin` with using `cd`
* Run the `.\decomm_sys.ps` script to gather information about the current state of the resources the system uses. This script will generate a report named `res_info.csv` under the `.\admin` directory

<pre id="cmdln-text">
C:\ProSoft\users>decomm_sys.ps
>>> Initializing decommissioning system ...
>>> Resource list is being generated ...
>>> Done

C:\ProSoft\users>ls *csv | ft Name

sys_res.csv
</pre>

* Using the report, back up all the legacy data. These are the `*.dat`, `*.dbx`, `*.idx`, `*.cfg`, `*.ps`, and `*.md` files
* Release the certificates by running the `cert_rel.ps` script

<pre id="cmdln-text">
C:\ProSoft\users>cert_rel.ps
>>> Releasing certificates ...
>>> Done
</pre>

* Remove the licenses by running the `uninst_lic.ps` script

<pre id="cmdln-text">
C:\ProSoft\users>uninst_lic.ps
>>> Uninstalling license ...
>>> Done
</pre>

> <span id="warning-byline">Keep the certificates and licenses in a safe place in case the system needs to be reinstalled in the future
> </span>

* Finally, uninstall the software by running the `uninst_sys.ps` script

After the uninstall process completes, the `C:\ProSoft` root directory and the `.\admin` and `.\cert` directories under it will remain. You can delete these manually.

> <span id="warning-byline">It is strongly recommended that you back up the `C:\ProSoft`, `C:\ProSoft\admin`, and the `C:\ProSoft\cert` directories before you delete them.
>
> It is also recommended that the directory structure of the resources at the time of decommissioning is not tampered with during or after the back up process.
> </span>

</span>

---

## __ProSoft__ Hotline

In case there are issues you are unable to resolve using available *User Assistance* material, you can reach __ProSoft__ free of charge for expert advice through:

*Phone*: 850-555-6677

*E-mail*: [support@prosoft.com](support@prosoft.com)

---
