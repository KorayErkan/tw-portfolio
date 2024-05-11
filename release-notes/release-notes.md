# __ProSoft__&trade; v8.4.11 Release Notes

This document contains information about the current release of Prosoft&trade;.

## Table of contents

* [About this release](#about-this-release)
* [End-user requirements](#end-user-requirements)
* [Summary of changes](#summary-of-changes)
  * [New features](#new-features)
  * [Bugfixes](#bugfixes)
  * [Deprecations](#deprecations)
* [Known issues](#known-issues)

## About this release

The current release of ProSoft&trade; contains many bugfixes, removes some inconsistencies in the semantic versioning and ownership tracking facilities, and improves storage management; compatibility with various source, configuration, and log file types; and CI/CD-compatible source file marshalling functionality.

## End-user requirements

Users will have to backup their log and configuration files, uninstall their existing system, update their IIS to include bugfixes listed [here](https://www.bogus-bugfixes.com), and then install the current release.

## Summary of changes

Below are the summary of the changes in this version.

### New features

There are some important new features designed to ease management of large code bases.

* The system can now handle up to 64GB of repository resources, significantly increasing the project's development capability
* The semantic versioning system can now be directly synchronized with the version control mechanisms, and thereby never loses track of builds, published APIs, and backward compatibility status

### Bugfixes

There are many bugfixes, particularly related to the handling of parsing of configuration files and formats with nested structure.

### Deprecations

Some functions of the semantic versioning system have been deprecated in favor of the newly released ones.

## Known issues

There are known issues with the ownership tracking functionality:

* When the owner of a source file changes his name, id, or e-mail address, the system cannot update the database accordingly and loses track of the owner, orphaning the source files.
* When the owner wants to delegate the ownership of a source file, the future owner has to exist in the database. Otherwise, even though the tracking system displays the delegated owner's id, the source file becomes orphaned.

We will try to address these issues in future releases.
