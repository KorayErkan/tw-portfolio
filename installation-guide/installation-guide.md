# ProSoft v8.7.14 Installation Guide

This document provides information about the system requirements of ProSoft v8.7.14, as well as the procedure for installing it.

## Introduction

ProSoft is an engineering solution for managing the CI/CD pipeline automation in software development. The system keeps track of the modifications and additions made&mdash;including acceptance, unit, and integration tests&mdash;and the commits to source control, builds an automated pipeline for building release candidates, and charts the progress of various aspects of the project at any stage.

The system is compliant with the requirements and logic of CI/CD as it has been laid out in RFC 3265-A and RFC 3265-B.

## System Requirements

### Hardware

For an average team of 10-15 developers, the system requires at least 5 x 2.5GHz quadcore 7i processors, 64GB of RAM, and 1TB of disk space.

Also, a 100Base-TX Ethernet network connection is recommended for effective use.

### Dependencies

The installer checks the presence of the following components:

* Microsoft Visual C++ Redistributable: this is required for the MSVC libraries
* A strictly compliant SQL server (such as PostgreSQL 15 and above, Microsoft SQL Server 2018 and above, Oracle DBMS 2016 and above, etc.): the system keeps significant amounts of data in a relational database
* .NET 5 or higher
* IIS 6 or higher

## License Terms
