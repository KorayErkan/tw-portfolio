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

Users will have to backup their log and configuration files, uninstall their existing system, update their IIS to include bugfixes listed [here](https://www.bogus-bugfixes.com), and then install the current release.

## Summary of changes

Below are the summary of the changes in this version.

### New features

There are some important new features designed to ease management of large code bases.

* The system can now handle up to 64GB of repository resources, significantly increasing the project's development capability
* The semantic versioning system can now be directly synchronized with the version control mechanisms, and thereby never loses track of builds, published APIs, and backward compatibility status

### Bugfixes

There are many bugfixes, particularly related to the handling of configuration files and formats with nested structures.

* RINI files can now contain single-quoted tokens within double quoted strings
* GAML files now do not have to quote string values

### Deprecations

Some functions of the semantic versioning system have been deprecated in favor of the newly released ones.

## Known issues

There are known issues with the system regarding

* Ownership tracking functionality:
  * When the owner of a source file changes his name, id, or e-mail address, the system cannot update the database accordingly and loses track of the owner, orphaning the source files (BUG ID: #1234)
  * When the owner wants to delegate the ownership of a source file, the future owner has to exist in the database. Otherwise, even though the tracking system displays the delegated owner's id, the source file becomes orphaned without any warning (BUG ID: #1235)
  * Once the ownership of a resource has been delegated, it is not possible to re-delegate it to another user (BUG ID: #1236)
  * When a delegated source gets deleted without a commit, the previously existing versions of the resource remain in the system, and it is not possible to remove them from the trunk (BUG ID: #1237)
* File format recognition:
  * The system can parse JSON, TOML, and INI configuration files but it does not recognize XML-based formats (BUG ID: #2345)
  * JSON files must enclose all values in double quotes, otherwise the system assumes the unquoted token is a stop word (BUG ID: #2346)
  * INI files must quote string values. Otherwise they will be terminated at the first white space (BUG ID: #2347)

We will try to address these issues in future releases.
