# __ProSoft__&trade; v8.4.11 Release Notes

This document contains information about the current release of ProSoft&trade;.

## Table of contents

* [About this release](#about-this-release)
* [End-user requirements](#end-user-requirements)
* [Summary of changes](#summary-of-changes)
  * [New features](#new-features)
  * [Bugfixes](#bugfixes)
  * [Deprecations](#deprecations)
* [Known issues](#known-issues)

## About this release

The current release contains many bugfixes, removes some inconsistencies in the semantic versioning and ownership tracking facilities, and improves storage management, compatibility with various source, configuration, and log file types, and CI/CD-compatible source file marshalling functionality.

## End-user requirements

Users will have to back up their log and configuration files, uninstall their existing system, update their __CMX__ server to include bugfixes listed [here](https://www.bogus-bugfixes.com), and then install the current release.

## Summary of changes

This version brings a number of important changes. These include the following.

### New features

There are some important new features designed to ease management of large code bases.

* The system can now handle up to 64GB of repository resources, significantly increasing the project's development capability
* The semantic versioning system can now be directly synchronized with the version control mechanisms, and thereby never loses track of builds, published APIs, and backward compatibility status
* PDF files can now be directly viewed from within the ProSoft management console

### Bugfixes

There are many bugfixes, particularly related to the handling of configuration files and formats with nested structures.

* CFGX files can now process enumerated constants using the dot syntax (e.g. "_enumName.Constant_") (BUG ID: #4321)
* CFGX files no longer require _admin_ privileges to be edited (BUG ID: #4322)
* GAML files now support nested properties enclosed in square brackets (BUG ID: #5321)
* You can now assign a viewer application for specific file types in GAML files&mdash;for example Microsoft Word for _*.docx_ files (BUG ID: #5323)

### Deprecations

Some features of the system have been deprecated in favor of the newly developed ones:

* User grouping for creation of teams are now supported at the top level, and there is no need to assign team members to a pre-determined team lead
* Using a single hierarchy for project directories is now replaced with clustering of modules at any desired level
* Group identity assignment is now done automatically at the top level and is hierarchical; regrouping of lower level modules based on group identity is no longer available

## Known issues

There are some known issues with the system regarding

* Ownership tracking functionality:
  * When the owner of a source file changes his name, id, or e-mail address, the system cannot update the database accordingly and loses track of the owner, orphaning the source files (BUG ID: #1234)
  * When the owner wants to delegate the ownership of a source file, the future owner has to exist in the database. Otherwise, even though the tracking system displays the delegated owner's id, the source file becomes orphaned without any warning (BUG ID: #1235)
  * Once the ownership of a resource has been delegated, it is not possible to re-delegate it to another user (BUG ID: #1236)
  * When a delegated source gets deleted without a commit, the previously existing versions of the resource remain in the system, and it is not possible to remove them from the trunk (BUG ID: #1237)
* File format recognition:
  * The system can parse GAML, POML, and CFGX configuration files but it does not recognize XML-based formats (BUG ID: #2345)
  * POML files must enclose all values in double quotes, otherwise the system assumes the unquoted token is a stop word (BUG ID: #2346)
  * CFGX files must quote alphanumeric values. Otherwise they will be terminated at the first white space (BUG ID: #2347)

We will try to address these issues in future releases.
