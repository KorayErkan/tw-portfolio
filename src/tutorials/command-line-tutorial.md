# Searching Files With PowerShell

[_John Saysitall_](mailto:john.saysitall@goodcode.example)

This document explains how some _PowerShell_ cmdlets (small programs you can run from a terminal as commands) can be used to manage files in batch.

---

## Table of Contents

* [Introduction](#introduction)
* [Some Commonly Used Cmdlets](#some-commonly-used-cmdlets)
* [The Sample Folder](#the-sample-folder)
* [Listing Directory Objects](#listing-directory-objects)
* [Listing Subdirectories](#listing-subdirectories)
* [Searching By File Type](#searching-by-file-type)
* [Composing Cmdlets](#composing-cmdlets)
* [Formatting Output](#formatting-output)
* [Using Variables](#using-variables)
* [Refining Queries](#refining-queries)
* [Displaying Contents](#displaying-contents)
* [Advanced Text Search](#advanced-text-search)
* [Conclusion](#conclusion)

---

## Introduction

Command line use may not be popular among ordinary users, but once mastered, it _does_ provide quite a few advantages, the biggest of which is avoiding the tedium of manually managing large numbers of files. A simple command, used with judiciously selected parameters and piped through a formatting cmdlet, can quickly find the documents we want.

The command line is less popular than the graphical user interface because you have to remember the specific (and frequently cryptic) _names_ of commands, their _switches_, their _parameter types_, and so on. There is no doubt a learning curve. With the GUI, you find your way around by using the visual cues on the screen, which is simpler and more intuitive in the beginning.

However, a few weeks of command-line use may reveal that it is much more powerful, because you can adjust the granularity of what you do at every level. Once you get the hang of the commands involved (what their output looks like and what can be garnered from it), you can carry out multiple tasks with just a few lines.

We will try to illustrate these points below.

> <span id="note-byline">We will touch upon only the aspects of the PowerShell cmdlets (pronounced '_command-let_') that are relevant to the task at hand. We will _not_ do a thorough investigation of each of them.</span>

## Some Commonly Used Cmdlets

Before we begin, open a _Windows Terminal_ running PowerShell 7 and navigate to the sample folder described in the next section with the `cd` command.

The list of cmdlets we will learn is quite short, but they are the ones most commonly used for listing the contents of directories, filtering them based on certain criteria, and looking for certain strings in them:

|Cmdlet|Purpose|
|-|-|
|`Get-ChildItem`|List the objects in directories|
|`Format-Table`|Format a command's output for easier reading on the screen|
|`Where-Object`|Filter objects based on various criteria|
|`Get-Content`|Print the contents of a file on the screen|
|`Select-String`|Look for a specific piece of text in a file|

Each of these, except `Where-Object`, can be used independently or in combination with the others. We will first look at each of them in isolation, and later learn how to combine them for more accurate results.

## The Sample Folder

All the examples in this tutorial run against the same (imaginary) `Documents` folder of a user named _John_:

<pre id="cmdln-text">
C:\Users\John\Documents
├── Links\               (read-only directory)
├── Minutes\
│   ├── Notes.txt
│   ├── Q2-2021.docx
│   └── Q3-2021.txt
├── My Music\            (hidden system junction to C:\Users\John\Music)
├── My Pictures\         (hidden system junction to C:\Users\John\Pictures)
├── Reports\
│   ├── Notes.txt
│   ├── Q1-2020.txt
│   └── Q3-2021.docx
├── Drafts.docx
├── Notes.txt
├── Proposal.docx
├── Survey.csv
├── ToC.html
└── Tutoring.docx
</pre>

The dates in the outputs below are shown in the _dd/MM/yyyy_ format; your terminal displays them according to your regional settings.

## Listing Directory Objects

One of the most commonly used PowerShell cmdlets is `Get-ChildItem`, which lists the contents of a directory. Its basic syntax (that is, its most frequently used switches and parameters) is as follows:

<pre id="ebnf-text">
get-childitem-statement ::= Get-ChildItem
    [[-Path] &lt;path&gt; {"," &lt;path&gt;}]
    [[-Filter] &lt;wildcard&gt;]
    [(-Include | -Exclude) &lt;wildcard&gt; {"," &lt;wildcard&gt;}]
    [-Recurse]
    [-File | -Directory]
    [-Attributes &lt;attribute-expression&gt;]
    [-Force]
</pre>

`-Recurse`, `-File`, `-Directory`, and `-Force` are _switches_: they take no value, and simply turn a behavior on.

Its typical use is pretty straightforward:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem .
</pre>

Here, the dot after the command is a shorthand for the directory we are in. The cmdlet assumes that this is the value of its `-Path` parameter.

> <span id="note-byline">In most command-line interpreters, on various operating systems, it is a widely adopted convention to represent the current directory with '`.`' and the parent directory with '`..`'.</span>

Using that parameter, any directory&mdash;including those on other drives&mdash;can be listed regardless of what the current directory is. It is also possible to list multiple directories by separating their names with commas:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem -Path ".\Reports", ".\Minutes", "D:\Backup\Reports"
</pre>

Here, the '`.\`' before the directory names tells the cmdlet to look for these directories under the current one. You can omit it, since relative paths are resolved from the current directory anyway.

> <span id="note-byline">Certain parameters of cmdlets accept multiple values when it is reasonable to do so. The values are specified as a comma-separated list, and although it is not necessary to place them in quotes (single or double) unless they contain spaces, it is a good practice to do so for readability.</span>

You can also list the contents of the directory above the current one equally easily by typing:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem ..
</pre>

Getting back to our example of listing the contents of the current directory, here is the output:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem .

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-r--          07/12/2020    11:58                Links
d----          10/10/2021    10:05                Minutes
d----          10/01/2022    08:20                Reports
-a---          01/08/2023    16:15          17510 Drafts.docx
-a---          21/10/2023    14:59             55 Notes.txt
-a---          02/07/2021    12:24          15872 Proposal.docx
-a---          01/06/2021    11:34           1204 Survey.csv
-a---          02/09/2023    16:15           2580 ToC.html
-a---          21/08/2023    10:36          16803 Tutoring.docx
</pre>

The first column (the one with the heading `Mode`) contains letters or dashes in five positions, which indicate the _attributes_ of the objects. A dash means that the object does not have that attribute:

|Letter|Attribute|
|-|-|
|`d----`|Directory|
|`l----`|Link (a reparse point such as a symbolic link or junction)|
|`-a---`|Archive|
|`--r--`|Read-only|
|`---h-`|Hidden|
|`----s`|System|

> <span id="note-byline">This tutorial uses PowerShell 7. The older _Windows PowerShell 5.1_ displays a six-character `Mode` column, with the link flag `l` in the last position instead of the first.</span>

The above output indicates that `Links` is a read-only directory, `Minutes` and `Reports` are ordinary directories, and the rest are files with the archive attribute set. By default, hidden and system objects are _not_ listed. To see, for example, the hidden objects under the current directory, we use the `-Attributes` parameter:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . -Attributes Hidden

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
l--hs          07/12/2020    07:39                My Music -> C:\Users\John\Music
l--hs          07/12/2020    07:39                My Pictures -> C:\Users\John\Pictures
</pre>

The mode indicates that these two objects are **l**inks, they are **h**idden, and they are **s**ystem objects. The arrow shows the directory each link points to.

> <span id="note-byline">A _reparse point_ is the NTFS mechanism behind symbolic links and directory junctions. A junction is closer to a UNIX _symbolic link_ than to a hard link: it is a separate entry that redirects to another directory. Navigating into it is as simple as a typical `cd` call.</span>

Multiple attributes can be combined to refine the query:

* Joining attributes with a plus sign (`+`) means **AND**: the object must have _all_ of them.
* Separating attributes with a comma (`,`) means **OR**: the object must have _at least one_ of them.

The following lists objects that are hidden **and** reparse points:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . -Attributes Hidden+ReparsePoint

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
l--hs          07/12/2020    07:39                My Music -> C:\Users\John\Music
l--hs          07/12/2020    07:39                My Pictures -> C:\Users\John\Pictures
</pre>

The following lists objects that are read-only **or** reparse points. Because the reparse points here are also hidden, we add the `-Force` switch, which includes hidden and system objects in the listing:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . -Attributes ReadOnly, ReparsePoint -Force

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-r--          07/12/2020    11:58                Links
l--hs          07/12/2020    07:39                My Music -> C:\Users\John\Music
l--hs          07/12/2020    07:39                My Pictures -> C:\Users\John\Pictures
</pre>

We are not limited to seeing only what is inside the directory we have specified, though. We can use that directory as a starting point for a search.

## Listing Subdirectories

Using the `-Recurse` switch, we can list what is inside the current directory as well as inside all its subdirectories:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem -Recurse .

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-r--          07/12/2020    11:58                Links
d----          10/10/2021    10:05                Minutes
d----          10/01/2022    08:20                Reports
-a---          01/08/2023    16:15          17510 Drafts.docx
-a---          21/10/2023    14:59             55 Notes.txt
-a---          02/07/2021    12:24          15872 Proposal.docx
-a---          01/06/2021    11:34           1204 Survey.csv
-a---          02/09/2023    16:15           2580 ToC.html
-a---          21/08/2023    10:36          16803 Tutoring.docx

    Directory: C:\Users\John\Documents\Minutes

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          10/10/2021    10:05             57 Notes.txt
-a---          02/07/2021    13:07          14750 Q2-2021.docx
-a---          09/10/2021    16:24            164 Q3-2021.txt

    Directory: C:\Users\John\Documents\Reports

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          10/01/2022    08:20             47 Notes.txt
-a---          08/04/2020    09:41            172 Q1-2020.txt
-a---          15/10/2021    17:32          14212 Q3-2021.docx
</pre>

The command first lists the objects in the current directory, then those in each of its subdirectories, repeating the same process for every directory it finds. It stops when there are no more subdirectories to look into. (`Links` is empty, so it has no section of its own.)

## Searching By File Type

One of the primary uses of listing directories is to look for files of a specific type. A common technique is to use the file extension. The following looks for _Microsoft Word_ documents. Note that "`*.docx`" is a _wildcard_ pattern, not a regular expression: `*` stands for any sequence of characters.

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . "*.docx"

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          01/08/2023    16:15          17510 Drafts.docx
-a---          02/07/2021    12:24          15872 Proposal.docx
-a---          21/08/2023    10:36          16803 Tutoring.docx
</pre>

The cmdlet binds the second positional value, "`*.docx`", to its `-Filter` parameter. `-Filter` accepts only a single pattern. To look for multiple file types, we use the `-Include` parameter instead:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem .\* -Include "*.docx", "*.html"

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          01/08/2023    16:15          17510 Drafts.docx
-a---          02/07/2021    12:24          15872 Proposal.docx
-a---          02/09/2023    16:15           2580 ToC.html
-a---          21/08/2023    10:36          16803 Tutoring.docx
</pre>

> <span id="warning-byline">`-Include` only takes effect when the path ends in a wildcard (`.\*`, as above) or when `-Recurse` is used. `Get-ChildItem . -Include "*.docx", "*.html"` returns nothing at all.</span>

We can also `-Exclude` certain objects from our search if we are not interested in them. For example:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . -Exclude "*.html"

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-r--          07/12/2020    11:58                Links
d----          10/10/2021    10:05                Minutes
d----          10/01/2022    08:20                Reports
-a---          01/08/2023    16:15          17510 Drafts.docx
-a---          21/10/2023    14:59             55 Notes.txt
-a---          02/07/2021    12:24          15872 Proposal.docx
-a---          01/06/2021    11:34           1204 Survey.csv
-a---          21/08/2023    10:36          16803 Tutoring.docx
</pre>

Here, we see every object in the current directory except `ToC.html`, the only one matching "`*.html`".

Finally, we can ask for directories only, without specifying their names, by using the `-Directory` switch (its counterpart, `-File`, lists files only):

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . -Directory

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-r--          07/12/2020    11:58                Links
d----          10/10/2021    10:05                Minutes
d----          10/01/2022    08:20                Reports
</pre>

## Composing Cmdlets

At this point, we will introduce a technique known as _piping_, which _composes_ the functionality of multiple commands. It is achieved by placing a '`|`' character after a command and its parameters to feed its output to another command:

<pre id="ebnf-text">
&lt;command&gt; &lt;parameters&gt; '|' &lt;command&gt; &lt;parameters&gt;
</pre>

The purpose of this is to avoid having to manually manipulate the output of one command to use it as input for the next. To illustrate, after listing the objects in the current directory and its subdirectories, we can pipe the results to `Get-Content` to see what is inside them:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem -Recurse . -Include "Notes.txt" | Get-Content
The minutes for the Q3-2021 meeting must be summarized.
Don't forget to write the report for Q1-2022.
Back up the Reports and Minutes folders every Friday.
</pre>

Here, we have searched the current directory and its subdirectories for files named `Notes.txt` (there is one in each of `Minutes`, `Reports`, and `Documents` itself), and printed their contents to the terminal window. Note that `Get-Content` prints only the lines of the files; it does not say which file each line came from.

> <span id="warning-byline">Unlike UNIX shells, PowerShell does not pipe plain text: it passes _objects_. The receiving cmdlet binds each incoming object (or one of its properties, such as a file's path) to one of its parameters. If a cmdlet has no parameter that accepts pipeline input of that kind, piping to it will fail.</span>

A much more common use of piping, however, is manipulating the output of the previous command for further processing.

## Formatting Output

We do not have to settle for the default output of a command if it is too detailed to read easily. We can pick certain properties and present them in a simpler style using the `Format-Table` cmdlet:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . "*.docx" | Format-Table FullName

FullName
--------
C:\Users\John\Documents\Drafts.docx
C:\Users\John\Documents\Proposal.docx
C:\Users\John\Documents\Tutoring.docx
</pre>

Here, the property name `FullName` tells `Format-Table` to output only the full path of each file.

We can select several properties if we specify them in a comma-separated list:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . "*.docx" | Format-Table -Property FullName, Length -HideTableHeaders

C:\Users\John\Documents\Drafts.docx    17510
C:\Users\John\Documents\Proposal.docx  15872
C:\Users\John\Documents\Tutoring.docx  16803
</pre>

Here, we see only the paths of the files and their sizes in bytes. The comma-separated list is the value of the `-Property` parameter, and the `-HideTableHeaders` switch removes the column headers, since we already know the order the properties are presented in.

We can also use the `-GroupBy` parameter to organize the output further. This is especially useful when we recurse into subdirectories:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . -Recurse -Include "*.docx", "*.txt" | Format-Table -Property FullName -GroupBy Directory -HideTableHeaders

   Directory: C:\Users\John\Documents\Minutes

C:\Users\John\Documents\Minutes\Notes.txt
C:\Users\John\Documents\Minutes\Q2-2021.docx
C:\Users\John\Documents\Minutes\Q3-2021.txt

   Directory: C:\Users\John\Documents\Reports

C:\Users\John\Documents\Reports\Notes.txt
C:\Users\John\Documents\Reports\Q1-2020.txt
C:\Users\John\Documents\Reports\Q3-2021.docx

   Directory: C:\Users\John\Documents

C:\Users\John\Documents\Drafts.docx
C:\Users\John\Documents\Notes.txt
C:\Users\John\Documents\Proposal.docx
C:\Users\John\Documents\Tutoring.docx
</pre>

Experimenting with various combinations of the two cmdlets should yield results closer to what you would like to see on the screen.

## Using Variables

At this point, we should mention one of the very useful features of PowerShell: variables.

As our command lines become more complicated, they may become unwieldy. If we are working in deeply nested directory structures, the text may not fit in the terminal window, and it may become tedious to type certain strings, such as paths or file names, again and again. In such situations, assigning the tokens we use to variables comes in handy.

The basic syntax is very simple:

<pre id="ebnf-text">
'$'&lt;variable-name&gt; '=' &lt;expression&gt;
</pre>

Defining variables to avoid typing the same lengthy pieces of text&mdash;paths, properties, phrases to be found in files, and so on&mdash;is always good practice when your command lines grow complicated.

For example, if we are searching in multiple directories, it makes sense to declare a variable for them:

<pre id="cmdln-text">
PS C:\Users\John\Documents> $directories = "Reports", "Minutes"
PS C:\Users\John\Documents> Get-ChildItem $directories

    Directory: C:\Users\John\Documents\Reports

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          10/01/2022    08:20             47 Notes.txt
-a---          08/04/2020    09:41            172 Q1-2020.txt
-a---          15/10/2021    17:32          14212 Q3-2021.docx

    Directory: C:\Users\John\Documents\Minutes

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          10/10/2021    10:05             57 Notes.txt
-a---          02/07/2021    13:07          14750 Q2-2021.docx
-a---          09/10/2021    16:24            164 Q3-2021.txt
</pre>

Here, we have stored two directory names in a variable, and passing that variable to `Get-ChildItem` was enough to list the items in both directories.

> <span id="warning-byline">To store a list of values, such as two or more directory names, in a variable, quote each item and separate the items with commas. PowerShell then stores an _array_ of strings. If you instead put the whole list inside a single pair of quotes, you store one string, and PowerShell will look for a single directory with that literal name.</span>

We will see what other kinds of values we can store in variables to streamline our work below.

## Refining Queries

It is frequently not enough to list objects by their name and type. We may want to pick those that possess other properties, such as having a specific phrase in their name, being above a certain size, or having been modified after a specific date. In that case, we use the `Where-Object` cmdlet.

This cmdlet makes it possible to specify the qualities that an object should possess, with the following syntax:

<pre id="ebnf-text">
where-statement ::= Where-Object { $_.&lt;property-name&gt; &lt;comparison&gt; &lt;value&gt; }
                  | Where-Object -Property &lt;property-name&gt; &lt;comparison&gt; &lt;value&gt;
comparison ::= -match | -notmatch
             | -like | -notlike
             | -contains
             | -gt | -ge | -lt | -le | -eq | -ne
</pre>

In the first form, `$_` stands for the object currently passing through the pipeline.

Let's illustrate its use with an example:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . "*.docx" | Where-Object {$_.Name -like "*Tutor*"}

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          21/08/2023    10:36          16803 Tutoring.docx
</pre>

We have queried for all _Microsoft Word_ documents that have the phrase "Tutor" in their names. `-like` compares against a wildcard pattern, so the asterisks on both sides are needed: `-like "Tutor"` would match only a file named exactly `Tutor`. Here is another example:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . "*.docx" | Where-Object {$_.Length -ge 17500}

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          01/08/2023    16:15          17510 Drafts.docx
</pre>

This time, we queried for _Microsoft Word_ documents whose size is _greater than or equal to_ (which is what `-ge` stands for) 17500 bytes.

The `-match` comparison operator is for regular expressions. We can use it, for example, to select multiple types of files:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . | Where-Object -Property Extension -Match "(docx|html)"

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          01/08/2023    16:15          17510 Drafts.docx
-a---          02/07/2021    12:24          15872 Proposal.docx
-a---          02/09/2023    16:15           2580 ToC.html
-a---          21/08/2023    10:36          16803 Tutoring.docx
</pre>

As you might have guessed, we can narrow down our search further by piping again. A line that ends with `|` continues on the next line, which PowerShell marks with a `>>` prompt:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem . |
>>     Where-Object -Property Extension -Match "(docx|html)" |
>>     Where-Object -Property LastWriteTime -GE "2022-05-01"

    Directory: C:\Users\John\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          01/08/2023    16:15          17510 Drafts.docx
-a---          02/09/2023    16:15           2580 ToC.html
-a---          21/08/2023    10:36          16803 Tutoring.docx
</pre>

We have queried for all _Microsoft Word_ documents and HTML files, then selected only those whose `LastWriteTime`, that is, the time they were last _modified_, is on or after May 1, 2022. Writing the date as _yyyy-MM-dd_ keeps it unambiguous whatever your regional settings are.

Let's use variables to streamline our work. This time, the variables hold _script blocks_, the filter expressions in curly braces:

<pre id="cmdln-text">
PS C:\Users\John\Documents> $directories = "Reports", "Minutes"
PS C:\Users\John\Documents> $only_word_files = {$_.Extension -match "docx"}
PS C:\Users\John\Documents> $only_newest = {$_.LastWriteTime -ge [datetime]"2021-01-01"}
PS C:\Users\John\Documents> Get-ChildItem $directories | Where-Object $only_word_files | Where-Object $only_newest

    Directory: C:\Users\John\Documents\Reports

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          15/10/2021    17:32          14212 Q3-2021.docx

    Directory: C:\Users\John\Documents\Minutes

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          02/07/2021    13:07          14750 Q2-2021.docx
</pre>

Very clean and easy to follow. To refine our search further, we have to query what is inside the files.

## Displaying Contents

Frequently, you may want to take a quick look at a file in case it contains what you are looking for. If the file is in a text format, PowerShell offers a convenient cmdlet named `Get-Content` to display its contents in the terminal.

Assuming you know the name of the file whose contents you want to display, the syntax is:

<pre id="ebnf-text">
get-content-statement ::= Get-Content [-Path] &lt;file-name&gt;
</pre>

The use of the cmdlet in this form is very simple:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-Content -Path .\Reports\Q1-2020.txt
2020 QUARTERLY REPORT

This is the report for the 1st quarter of 2020. We will provide
a brief summary of all the activities that have been organized
and carried out.
</pre>

The cmdlet is more flexible than that, however. Because it accepts file objects from the pipeline (it binds the path of each incoming file to its own path parameter), you can use it after looking for specific files:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem .\Reports | Where-Object {$_.Name -like "*Q1*"} | Get-Content
2020 QUARTERLY REPORT

This is the report for the 1st quarter of 2020. We will provide
a brief summary of all the activities that have been organized
and carried out.
</pre>

If you do not want to check the contents of the files manually, however, there is an even more powerful cmdlet to find what you are looking for.

## Advanced Text Search

If you want to search inside the files directly, the cmdlet you need is `Select-String`. It queries the text inside the files we have found in a directory.

This cmdlet searches for phrases and patterns in text files, and its basic syntax is:

<pre id="ebnf-text">
select-string-statement ::= Select-String
    [-Pattern] &lt;pattern&gt; [-SimpleMatch]
    [-Path] &lt;file-name&gt;
    [-CaseSensitive]
</pre>

As can be seen from the syntax, we specify a pattern, which is treated as a regular expression by default (if we want a verbatim match instead, we add the `-SimpleMatch` switch), and then the path of the file. The search is case-insensitive unless we add `-CaseSensitive`.

`Select-String` does not print whole files. For every line that matches, it prints the file name, the line number, and the matching line, separated by colons:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Select-String -Pattern "QUARTERLY" -SimpleMatch -Path .\Reports\Q1-2020.txt

Reports\Q1-2020.txt:1:2020 QUARTERLY REPORT
</pre>

Like `Get-Content`, this cmdlet accepts file objects from the pipeline:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem .\Reports | Select-String -Pattern "QUARTERLY"

Reports\Q1-2020.txt:1:2020 QUARTERLY REPORT
</pre>

Finally, using the syntax of regular expressions, we can look for several pieces of text at once, and `Select-String` will spot every line that contains any of them:

<pre id="cmdln-text">
PS C:\Users\John\Documents> Get-ChildItem -Path ".\Reports", ".\Minutes" | Select-String -Pattern "(report|events)"

Reports\Notes.txt:1:Don't forget to write the report for Q1-2022.
Reports\Q1-2020.txt:1:2020 QUARTERLY REPORT
Reports\Q1-2020.txt:3:This is the report for the 1st quarter of 2020. We will provide
Minutes\Q3-2021.txt:3:These minutes were recorded to report the results of the events
</pre>

Here, PowerShell found four matching lines in three files. Because the search is case-insensitive, "`REPORT`" on the first line of `Q1-2020.txt` matched too. The `.docx` files were searched as well, but since Word documents are compressed, their text cannot be matched this way.

## Conclusion

The cmdlets presented above, when combined imaginatively, make it easy to find what you are looking for. Whether it is the directories likely to contain the files, properties such as extension, modification date, or size that identify them, or pieces of text they contain, PowerShell can spot them and list them in the terminal. It all depends on how precisely you specify what you are searching for.

Good luck learning to use these very powerful cmdlets.

<hr>

_Copyright&copy; 2024, John Saysitall_
