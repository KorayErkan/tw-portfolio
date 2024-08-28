# Managing Files With PowerShell

[_John Saysitall_](mailto:John.saysitall@goodcode.com)

This document explains how some _PowerShell_ cmdlets—i.e. programs you can run from a terminal as commands—can be used to manage files in batch.

## Table of Contents

* [Introduction](#introduction)
* [Common Commands for Managing Files](#common-commands-for-managing-files)
* [Listing Directory Objects](#listing-directory-objects)
* [Listing Subdirectories](#listing-subdirectories)
* [Searching By File Type](#searching-by-file-type)
* [Piping](#piping)
* [Formatting Output](#formatting-output)
* [Use of Variables](#use-of-variables)
* [Refining Queries](#refining-queries)
* [Advanced Searching and Finding](#advanced-searching-and-finding)
* [Updating a Collection of Files](#updating-a-collection-of-files)

## Introduction

Command line use may not be popular among ordinary users, but once mastered, it _does_ provide quite a few advantages the biggest one of which can be to avoid the tedium of manually managing large numbers of files. A simple command, when used with judiciously selected parameters and piped through a formatting cmdlet, can quickly get the types of documents we want.

The reason the command line is not as popular as the graphical user interface is the necessity to remember the specific (and frequently cryptic) _names_ of various commands, their _switches_, and their _parameter types_, etc. With the GUI, you just try to find your way around just by using the visual cues the graphical objects on the screen provide. However, using the command line for a few weeks may reveal that that because you can adjust the granularity of what you intend to do. That is, you can set the parameters with a very concise syntax to express the details of the task to be carried. Once you get the hang of specific commands (i.e. what their output looks like, what can be garnered from that output, etc.), you can carry out multiple tasks with just a few lines in one place.

We will try to illustrate these points with some common file management tasks.

## Common Commands for Managing Files

We will summarize the cmdlets (read as "commandlets") used for searching the contents of directories, filtering them based on certain criteria, looking for certain strings in them, updating their contents in batch, etc. Those we will cover are:

|Cmdlet|Purpose|
|-|-|
|`Get-ChildItem`|List the objects in directories|
|`Format-Table`|Format the output of a command's output for easier reading on the screen|
|`Where-Object`|Filter object based on various criteria|
|`Select-String`|Look for a specific piece of text in a file|
|`Measure-Object`|Gather information like number of objects, their sizes, etc.|
|`Get-Content`|Print the contents of a file on the screen|
|`Set-Content`|Update the contents of a file|

We will take a closer look at each of these below.

## Listing Directory Objects

One of the most commonly used cmdlets of PowerShell is `Get-ChildItem` which lists the contents of the current directory. Its most basic use is as follows:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem .
</pre>

Here, the dot (".") after the command is a shorthand for specifying the current directory. The cmdlet assumes that this is the parameter for its `Path` switch. Using that switch, any arbitrary directory&mdash;including those on other drives&mdash;can be listed. For example:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem -Path H:\Backup\Reports
</pre>

It is also possible to list multiple directories by separating their names with a comma:

> <span id="note-byline">Certain switches of cmdlets allow multiple values if it is reasonable to do so. The values should be specified as a comma-separated list, and although it is not necessary to place them in quotes (single or double), it is a good practice to do so for readability</span>

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem -Path ".\Documents", ".\Reports"
</pre>

Here, the ".\" before the directory names tells the cmdlet to look for these directories under the current one.

Getting back to our example of listing the contents of the current directory, here's a typical output:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem .

    Directory: C:\Users\john\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        24/12/2022     12:03                PowerShell
d-r---        07/12/2020     11:58                Links
-a----        21/10/2023     14:59           2365 Notes.txt
</pre>

The first column (the one with the heading `Mode`) where we have either certain letters or dashes (6 placeholders in total) indicates what is known as the _attributes_ of the objects. A dash indicates that the object does not have that attribute:

|Letter|Attribute|
|-|-|
|`d-----`|Directory|
|`-a----`|Archive|
|`--r---`|Read Only|
|`---h--`|Hidden|
|`----s-`|System|
|`-----l`|Link -or- ReparsePoint|

The above output indicates that `PowerShell` is a directory, `Links` is a read-only directory, and `Notes.txt` (a text file) is an archive. By default, hidden and system directories and files are _not_ listed. If we wanted to see, for example, the hidden directories under the current directory, we use the `-Attributes` switch of this cmdlet.

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . -Attributes Hidden

    Directory: C:\Users\john\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d--hsl        07/12/2020     07:39                Music
d--hsl        07/12/2020     07:39                Pictures
</pre>

The mode indicates that these two objects are **d**irectories, they are **h**idden, they are **s**ystem directories, and they are **l**inks.

Multiple attributes can be specified to refine the query. For this, we have to list the attributes separating them with commas. The following lists objects that are read only and are reparse points:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . -Attributes Hidden, ReadOnly, RepoarsePoint

    Directory: C:\Users\john\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
dar--l        29/07/2024     23:43                OneDrive
d--hsl        07/12/2020     07:39                PrintHood
d--hsl        07/12/2020     07:39                Recent
</pre>

## Listing Subdirectories

Our directory listing command is not limited to listing only the current directory. Using its `-Recurse` switch, we can check what is inside the current directory as well as all its subdirectories.

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem -Recurse .

    Directory: C:\Users\john\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
dar--l        29/07/2024     23:43                OneDrive
d-----        11/06/2018     11:15                Reports
d-----        11/06/2018     11:15                Minutes
a-----        16/09/2021     09:56                ToC.html

    Directory: C:\Users\john\Documents\Reports

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        08/09/2020     06:41                Q1-2020.txt
-a----        15/06/2020     05:32                Q3-2021.txt

    Directory: C:\Users\john\Documents\Minutes

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        09/05/2020     16:24                Q3-2021.txt
</pre>

The command first lists the objects under the current directory, then those under each of the directories specified with the `Path` switch in turn.

## Searching By File Type

One of the primary uses of enumerating the objects in directories, other than seeing what is in them, is to look for files of a specific type. A common technique to search them is to use the file extension. The following looks for _Microsoft Word_ documents. Note that we are using the regular expression "\*.docx" for this:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . "*.docx"

    Directory: C:\Users\john\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        01/08/2023     16:15          17510 Drafts.docx
-a----        21/08/2023     10:36          16803 Tutoring.docx
</pre>

The cmdlet assumes that the `"*.docx"` parameter specified is for the `-Include` switch. Using this, we can look for multiple file types by specifying their extensions:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . -Include "*.docx", "*.html"

    Directory: C:\Users\john\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        01/08/2023     16:15          17510 Drafts.docx
-a----        21/08/2023     10:36          16803 Tutoring.docx
-a----        03/06/2023     11:48          17510 Report.html
</pre>

We can also `-Exclude` certain objects from our seach if we are not interested in them. For example:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . -Exclude "*.html"

    Directory: C:\Users\john\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        01/08/2023     16:15          17510 Drafts.docx
-a----        21/08/2023     10:36          16803 Tutoring.docx
-a----        02/07/2021     12:24          17510 Proposal.docx
-a----        01/06/2021     11:34          16803 Proposal.csv
</pre>

Here, we see every file under the current directory except for those with the "*.html" extension.

## Piping

At this point, we will mention a technique known as _piping_. This is a technique used to _compose_ the functionality of multiple commands. It is achieved by placing a '|' character after the command and its parameters to feed the output to another command:

<pre -id="ebnf-text">
&lt;command&gt; &lt;parameters&gt; '|' &lt;command&gt; &lt;parameters&gt;
</pre>

The purpose of this is to avoid having to manually manipulate the output of a command to use it as input for the next one. To illustrate, after listing the objects in the current directory, we can pipe the results to a call to `Get-Content` to see what is inside them.

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem -Recurse . -Include "Notes.txt" | Get-Content
TODO: Don't forget to write the report for Q1-2022

TODO: The minutes for the Q3-2021 meeting must be summarized.
</pre>

Here, we have iterated through the subdirectories of the current one to spot files named "Notes.txt" (which means there may be multiple files in different directories name "Notes.txt"), and printed their contents to the terminal window too see what is inside them

> <span id="warning-byline">This technique will not work with every cmdlet. If a command does not read the standard input for data entry, you won't be able to pipe the output of a command to it.</span>

A much more common use of piping, however, is manipulating the output of the previous command for further processing.

## Formatting Output

We do not have to settle for the default output of a command if the output is too complicated and therefore difficult to read. We can pick certain elements in it and present them in a simpler style using the `Format-Table` cmdlet:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . "*.docx" | Format-Table Fullname

Fullname
--------
C:\Users\John\Documents\Drafts.docx
C:\Users\John\Documents\Tutoring.docx
</pre>

Here, the parameter `Fullname` tells `Format-Table` to output only the full path of the file from the root.

We can select other attributes of the objects using this cmdlet if we specify them in a comma-separated list:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . "*.docx" | Format-Table -Property Fullname, Length -HideTableHeaders

C:\Users\john\Documents\Drafts.docx         17510
C:\Users\john\Documents\Tutoring.docx       16803
</pre>

Here, we see only the paths of the files we were looking for and their sizes in bytes. The comma-separated list is for the `-Property` switch to pick the properties we consider relevant, and the `-HideTableHeaders` removes their headers since we already know the order these will be presented in.

We can also use the `-GroupBy` switch for further streamlining of the output. This is especially useful when we recurse to the subdirectories.

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . -Recurse -Include "*.docx", "*.txt" | Format-Table -Property Fullname -GroupBy Directory -HideTableHeaders

   Directory: C:\Users\John\Documents

C:\Users\john\Documents\Drafts.docx
C:\Users\john\Documents\Tutoring.docx

   Directory: C:\Users\John\Documents\Reports

C:\Users\john\Documents\Reports\Q1-2021.txt
C:\Users\john\Documents\Reports\Q3-2021.docx

   Directory: C:\Users\John\Documents\Minutes

C:\Users\john\Documents\Minutes\Q3-2021.docx
</pre>

Experimenting with various combinations of the two commands should yield results closer to what you would like to see reported on the screen.

## Use of Variables

At this point, we should mention one of the very useful features of PowerShell: being able to use variables.

As our command line entries become more complicated, they may become unwieldy and difficult to manipulate. If we're working deeply nested directory structures, it may become difficult to fit the text in the terminal window. It may also become tedious to type certains strings such as paths of filenames. In such situations, defining variables and assigning various command line tokens we are using to them will most certainly become handy.

The basic syntax is very simple:

<pre id="ebnf-text">
"$"&lt;variable-name&gt; "=" &lt;value&gt;
</pre>

## Refining Queries

It is frequently not enough to list objects by their name and type. We may want to pick those that possess other properties such as having a specific phrase in its name, being above a certain size, having been created before a specific date, etc. In that case, we have to use the `Where-Object` cmdlet.

This cmdlet makes it possible to specify qualifies that the object should possess with the following syntax:

<pre id="ebnf-text">
Where-Object "{" "$_."&lt;property&gt; ("-like" | "-ge" | "-lt" | "-eq" | "-neq") &lt;parameter&gt; "}"
</pre>

Let us illustrate its use with an example:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . "*.docx" | Where-Object {$_.Name -like "Tutor"}

    Directory: C:\Users\john\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        21/08/2023     10:36          16803 Tutoring.docx
</pre>

We have queried for all _Microsoft Word_ documents that has the phrase "Tutor" in its name. Here is another one:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . "*.docx" | Where-Object {$_.Length -ge 17500}

    Directory: C:\Users\john\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        01/08/2023     16:15          17510 Drafts.docx
</pre>

This time, we queried for _Microsoft Word_ documents that are _greater than or equal to_ (which is what _-ge_ stands for) 17500 bytes.

## Advanced Searching and Finding

Now we will look into making a wider scoped search to find objects whose specific locations we may not know or remember.

<pre id="cmdln-text">
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
