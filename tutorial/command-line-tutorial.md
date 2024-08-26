# Managing Files With PowerShell

[_John Saysitall_](mailto:John.saysitall@goodcode.com)

This document explains how some _PowerShell_ cmdlets—i.e. programs you can run from a terminal as commands—can be used to manage files in batch.

## Table of Contents

* [Introduction](#introduction)
* [Common Commands for Managing Files](#common-commands-for-managing-files)
* [Searching and Finding](#searching-and-finding)
* [Formatting Output](#formatting-output)
* [Updating a Collection of Files](#updating-a-collection-of-files)

## Introduction

Command line use may not be popular among ordinary users, but once mastered, it _does_ provide quite a few advantages the biggest one of which can be to avoid the tedium of manually managing large numbers of files. A simple command, when used with judiciously selected parameters and piped through a formatting cmdlet, can quickly get the types of documents we want.

The reason the command line is not as popular as the graphical user interface is we have to remember the specific names of various commands, their _switches_, and their _parameter types_. With the GUI, you just try to find your way around just by using the visual cues the graphical objects on the screen provide. However, using the command line for a few weeks makes it apparent that it is more powerful because you can set the granularity of what you are seeking to do more precisely. And once you get the hang of specific commands (i.e. what their output looks like, what can be garnered from that output, etc.), you can carry out multiple tasks with just a few lines in one place.

We will try to illustrate these points with file management tasks.

## Common Commands for Managing Files

We will summarize the cmdlets (read as "commandlets") used for searching the contents of directories, filtering them based on certain criteria, looking for certain strings in them, updating their contents in batch, etc. Those we will cover are:

|Cmdlet|Purpose|
|-|-|
|`Get-ChildItem`|List the objects in directories|
|`Where-Object`|Filter object based on various criteria|
|`Select-String`|Look for a specific piece of text in a file|
|`Get-Content`|Print the contents of a file on the screen|
|`Set-Content`|Update the contents of a file|
|`Format-Table`|Format the output of a command's output for easier reading on the screen|
|`Measure-Object`|Gather information like number of objects, their sizes, etc.|

We will take a closer look at each of these below.

## Searching and Finding

One of the most commonly used cmdlets of PowerShell is `Get-ChildItem` which lists the contents of the current directory. Its most basic use is as follows:

<pre id="cmdln-byline">
C:\Users\John\Documents>Get-ChildItem .
</pre>

Here, the "." after the command represents the current directory. The default output is like this:

<pre id="cmdln-byline">
C:\Users\John\Documents>Get-ChildItem .
d-----        24/12/2022     12:03                PowerShell
d-r---        07/12/2020     11:58                Links
-a----        21/10/2023     14:59           2365 Notes.txt
</pre>

The first column, where we either have letters or dashes (6 in total), indicates what is known as the _attributes_ of the objects. A dash indicates that the object does not have that attribute:

|Letter|Attribute|
|-|-|
|`d-----`|Directory|
|`-a----`|Archive|
|`--r---`|Read Only|
|`---h--`|Hidden|
|`----s-`|System|
|`-----l`|Link|

The above output indicates that `PowerShell` is a directory, `Links` is a read-only directory, and `Notes.txt` (a text file) is an archive. By default, hidden and system directories and files are _not_ listed. If we wanted to see, for example, the hidden directories under the current directory, we use the `-Attributes` switch of this cmdlet.

<pre id="cmdln-byline">
C:\Users\John\Documents>Get-ChildItem . -Attributes Hidden
d--hsl        07/12/2020     07:39                Music
d--hsl        07/12/2020     07:39                Pictures
</pre>

The first column indicates that these two are **d**irectories, they are **h**idden, they are **s**ystem directories, and they are **l**inks.

To look for files of a specific type, a common technique is to use the file extension. The following looks for _Microsoft Word_ documents. Note that we are using the regular expression "\*.docx" for this:

<pre id="cmdln-byline">
C:\Users\John\Documents>Get-ChildItem . "*.docx"
-a----        01/08/2023     16:15          17510 Drafts.docx
-a----        21/08/2023     10:36          16803 Tutoring.docx
</pre>

## Formatting Output

<pre id="cmdln-byline">
C:\Users\John\Documents>Get-ChildItem -Recurse \*.docx | Format-Table Fullname

Fullname
--------
C:\Users\John\Documents\Budget-2023.docx
C:\Users\John\Documents\Personal\Career\CV.docx
C:\Users\John\Documents\Personal\School\College\Alumni.docx
C:\Users\John\Documents\Recipes\Vegetarian\Mediterranean.docx
C:\Users\John\Documents\Reports\Annual-2019.docx
C:\Users\John\Documents\Reports\Quarterly-2021-1.docx
C:\Users\John\Documents\Reports\Quarterly-2020-4.docx
</pre>

> <span id="note-byline">This can also be achieved using _Explorer_. However, we have to navigate to the top folder, then enter the regular expression "*.docx" in a drop-down box, and—once the documents are located-stay in that pane to carry out the planned tasks we have</span>

## Updating a Collection of Files

Updating files in batch—for example to change or remove a phrase in a group of files, to update the names of the files in a directory, to move them collectively to another directory, etc.— is a task that is frequently well-suited to command-line use. In this section, we will show you how to carry out those tasks with ease.

> <span id="note-byline">Be careful when you are updating multiple files, and make sure that the modifications you intend to make are valid for all of them. It is strongly advised that you back them up before making any changes</span>
