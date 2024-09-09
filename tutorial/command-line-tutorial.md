# Searching Files With PowerShell

[_John Saysitall_](mailto:John.saysitall@goodcode.com)

This document explains how some _PowerShell_ cmdlets—i.e. programs you can run from a terminal as commands—can be used to manage files in batch.

---

## Table of Contents

* [Introduction](#introduction)
* [Some Commonly Used Cmdlets](#some-commonly-used-cmdlets)
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

Command line use may not be popular among ordinary users, but once mastered, it _does_ provide quite a few advantages the biggest one of which can be to avoid the tedium of manually managing large numbers of files. A simple command, when used with judiciously selected parameters and piped through a formatting cmdlet, can quickly get the types of documents we want.

The reason the command line is not as popular as the graphical user interface is the necessity to remember the specific (and frequently cryptic) _names_ of various commands, their _switches_, and their _parameter types_, etc. No doubt, there is a learning curve. With the GUI, you find your way around just by using the visual cues the graphical layout on the screen provides, which is much simpler and intuitive in the beginning.

However, using the command line for a few weeks may reveal that because you can adjust the granularity of what you intend to do at every level, it is much more powerful. You can set the parameters with a very concise syntax to express the details of what you want to achieve. Once you get the hang of the specifics of the commands involved (i.e. what their output looks like, what can be garnered from that output, etc.), you can carry out multiple tasks with just a few lines.

We will try to illustrate these points below.

> <span id="note-byline">We will touch upon only the aspects of the PowerShell cmdlets (pronounced '_command-let_') that are relevant to the task at hand. We will _not_ do a thorough investigation of each of them. </span>

## Some Commonly Used Cmdlets

Before we begin, make sure you have opened a _Windows Terminal_ and navigated to a typical folder such as `Documents` with the `cd` command.

The list of cmdlets we will learn are quite small, but they are most commonly used for searching the contents of directories, filtering them based on certain criteria, looking for certain strings in them, updating their contents in batch, etc.:

|Cmdlet|Purpose|
|-|-|
|`Get-ChildItem`|List the objects in directories|
|`Format-Table`|Format the output of a command's output for easier reading on the screen|
|`Where-Object`|Filter objects based on various criteria|
|`Get-Content`|Print the contents of a file on the screen|
|`Select-String`|Look for a specific piece of text in a file|

Each of these, except `Where-Object`, can be used independently or in combination with the others. We will take a closer look at each of these below and explain them in isolation. Later on, we will learn how to combine them for more accurate results.

We will start with the first which is also the simplest.

## Listing Directory Objects

One of the most commonly used cmdlets of PowerShell is `Get-ChildItem` which lists the contents of the current directory. Its basic syntax (i.e. its most frequently-used switches and parameters) is as follows:

<pre id="ebnf-text">
get-childitem-statement ::= Get-ChildItem [-Recurse]
    [-Path] &lt;path&gt;
    [(-Include | -Exclude) &lt;file-types&gt;]
    [(-Fıle | -Directory) &lt;regular-expression&gt;]
</pre>

Its typical use is pretty straightforward:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem .
</pre>

Here, the dot after the command is a shorthand for specifying the directory we are in. The cmdlet assumes that this is the parameter for its `Path` switch.

> <span id="note-byline">In most command line interpreter implementations on various operating systems, it is a widely-adopted convention to represent the current directory with '`.`' and the parent directory with '`..`'</span>

Using that switch, any arbitrary directory&mdash;including those on other drives&mdash;can be listed regardless of what the current directory is. It is also possible to list multiple directories by separating their names with a comma:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem -Path ".\Documents", ".\Reports", "H:\Backup\Reports"
</pre>

You can also list the contents of the directories above the current one equally easily by typing:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem ..
</pre>

> <span id="note-byline">Certain switches of cmdlets allow multiple values if it is reasonable to do so. The values should be specified as a comma-separated list, and although it is not necessary to place them in quotes (single or double), it is a good practice to do so for readability</span>

Here, the '`.\`' before the directory names tells the cmdlet to look for these directories under the current one. You can omit it since it is the default.

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

> <span id="note-byline">A `ReparsePoint` in _Windows_ is known as a _hard link_ in UNIX operating systems. It is a direct link to a directory, and nagivating to and from it as simple as a typical `cd` call</span>

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

We are not limited with seeing only what is inside the directory we have specified, though. We can use that directory as a starting point for a search.

## Listing Subdirectories

It is possible to list everything under the current directory including the nested ones. Using its `-Recurse` switch, we can check what is inside the current directory as well as all its subdirectories.

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

The command first lists the objects under the current directory, then those under each those under it, repeating the same process for each directory in turn. It terminates when there are no more subdirectories to look into.

## Searching By File Type

One of the primary uses of enumerating the objects in directories is to look for files of a specific type, disregarding the rest. A common technique to search them is to use the file extension. The following looks for _Microsoft Word_ documents. Note that we are using the regular expression "`*.docx`" for this:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . "*.docx"

    Directory: C:\Users\john\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        01/08/2023     16:15          17510 Drafts.docx
-a----        21/08/2023     10:36          16803 Tutoring.docx
</pre>

The cmdlet assumes that the "`*.docx`" parameter specified is for the `-Include` switch. Using this switch, we can look for multiple file types by specifying their extensions:

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
-a----        01/06/2021     11:34          16803 Survey.csv
</pre>

Here, we see every file under the current directory except for those with the "`*.html`" extension.

Finally, we can also specify that we're only looking for directories in our search without specifying their names:

## Composing Cmdlets

At this point, we will mention a technique known as _piping_. This is a technique used to _compose_ the functionality of multiple commands. It is achieved by placing a '|' character after the command and its parameters to feed the output to another command:

<pre -id="ebnf-text">
&lt;command&gt; &lt;parameters&gt; '|' &lt;command&gt; &lt;parameters&gt;
</pre>

The purpose of this is to avoid having to manually manipulate the output of a command to use it as input for the next one. To illustrate, after listing the objects in the current directory, we can pipe the results to a call to `Get-Content` to see what is inside them.

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem -Recurse . -Include "Notes.txt" | Get-Content
Reports\Notes.txt:1:Don't forget to write the report for Q1-2022

Minutes\Notes.txt:1:The minutes for the Q3-2021 meeting must be summarized.
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

C:\Users\john\Documents\Minutes\Q2-2021.docx
</pre>

Experimenting with various combinations of the two commands should yield results closer to what you would like to see reported on the screen.

## Using Variables

At this point, we should mention one of the very useful features of PowerShell: being able to use variables.

As our command line entries become more complicated, they may become unwieldy and difficult to manipulate. If we're working deeply nested directory structures, it may become difficult to fit the text in the terminal window. It may also become tedious to type certains strings such as paths of filenames. In such situations, defining variables and assigning various command line tokens we are using to them will most certainly become handy.

The basic syntax is very simple:

<pre id="ebnf-text">
'$'&lt;variable-name&gt; '=' &lt;expression&gt;
</pre>

Defining variables in order to avoid typing the same lengthy pieces of text&mdash;paths, properties, phrases to be found in files, etc&mdash;is always good practice when using complicated use of the command line.

For example, if we're searching things in multiple directories, it makes sense to declare a variable for this:

<pre id="cmdln-text">
C:\Users\John\Documents>$directories = "Reports", "Minutes"
C:\Users\John\Documents>Get-ChildItem $directories

   Directory: C:\Users\John\Documents\Reports

C:\Users\john\Documents\Reports\Q1-2021.txt
C:\Users\john\Documents\Reports\Q3-2021.docx

   Directory: C:\Users\John\Documents\Minutes

C:\Users\john\Documents\Minutes\Q2-2021.docx
</pre>

Here, we have specified only two directories to look for items in, and calling that list was enough to get the items in those directories.

> <span id="warning-byline">When storing a list of values such as two or more directory names in a variable, each of these items must be quoted, and they must be separated by commas. That is because in order for what is stored in variables to be correctly interpreted by _PowerShell_, the value stored in the variable must be an _expression_.
>
> This can get confusing because a string is also an expression. However, a string is interpreted only as a value. If an expression involving switches or other cmdlets are entered as a string, those will _not_ be evaluated.</span>

We will see what other types of variables we can create to streamline our work below.

## Refining Queries

It is frequently not enough to list objects by their name and type. We may want to pick those that possess other properties such as having a specific phrase in its name, being above a certain size, having been created before a specific date, etc. In that case, we have to use the `Where-Object` cmdlet.

This cmdlet makes it possible to specify qualifies that the object should possess with the following syntax:

<pre id="ebnf-text">
where-statement ::= Where-Object { $_.&lt;property-name&gt; &lt;comparison&gt; &lt;parameter&gt; }
                  | Where-Object -Property &lt;property-name&gt; &lt;comparison&gt; &lt;parameter&gt;
comparison ::= -match | -notmatch
             | -like | -notlike
             | -contains
             | -gt | -ge | -lt | -le | -eq | -neq
</pre>

Let's illustrate its use with an example:

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

The _-match_ comparison operator is for regular expressions. We can use it, for example, to select multiple types of files:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . | Where-Object -Property Extension -match "(docx|html)"

    Directory: C:\Users\john\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        01/08/2021     16:15          17510 Drafts.docx
-a----        21/05/2021     10:36          16803 Tutoring.docx
-a----        02/09/2023     16:15           2580 ToC.html
</pre>

As you might have guessed, we can further narrow down our search by using piping.

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem . |
    Where-Object -Property Extension -match "(docx|html) |
    Where-Object -Property LastWriteTime -ge 5/1/2022"

    Directory: C:\Users\john\Documents

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        02/09/2023     16:15           2580 ToC.html
</pre>

We have queried for all _Microsoft Word_ documents and HTML files, then we selected only those that were created or updated after May 1, 2022.

Let's use variables to streamline our work:

<pre id="cmdln-text">
C:\Users\John\Documents>$directories = "Reports", "Minutes"
C:\Users\John\Documents>$only_word_files = {$_.Extension -match 'docx'}
C:\Users\John\Documents>$only_newest = {$_.LastWriteTime -ge '1/1/2021'}

C:\Users\John\Documents>Get-ChildItem $directories | Where-Object $only_word_files | Where-Object $only_newest

   Directory: C:\Users\John\Documents\Reports

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        01/08/2021     16:15          17510 Drafts.docx

   Directory: C:\Users\John\Documents\Minutes

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        02/05/2021     13:07          14750 Q2-2021.docx
</pre>

Very clean and easy to follow. To further refine our search, we have to query what is inside the files.

## Displaying Contents

Frequently, you may want to have an idea on some random file in case it contains what you are looking for. If the file is in a text format, PowerShell offers a convenient cmdlet named `Get-Content` to display the contents of the file on the terminal.

Assuming you know the name of the file whose contents you want to display, the syntax is:

<pre id="ebnf-text">
get-content-statement ::= Get-Content -Path &lt;file-name&gt;
</pre>

The use of the cmdlet in this form is very simple and straightforward:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-Content -Path .\Reports\Q1-2020.txt
2020 QUARTERLY REPORT

This is the report for the 1st quarter of 2020. We will provide
a brief summary of all the events that have been organized
and carried out.
...
</pre>

However, the cmdlet is much more flexible, and as it can read the so-called standard input you can use it with piping after looking for specific files:

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem .\Reports | Where-Object {$_.Name -like "*Q1*"} | Get-Content
2020 QUARTERLY REPORT

This is the report for the 1st quarter of 2020. We will provide
a brief summary of all the events that have been organized
and carried out.
...
</pre>

If you do not want to manually check the contents of the files, however, there's an even more powerful cmdlet to find what you are looking for.

## Advanced Text Search

The cmdlet in question is `Select-String`, and it can be used to query the text data inside the files we have discovered in a directory.

This commandlet searches for phrases and patterns in text files, and its basic syntax is:

<pre id="ebnf-text">
select-string-statement ::= Select-String
    -Pattern (&lt;regular-expression&gt; | &lt;plain-expression&gt; -SimpleMatch)
    -Path &lt;filename&gt;
    [-CaseSensitive]
</pre>

As can be seen from the syntax, we specify a pattern which is assumed to be a regular expression by default&mdash;if we want a verbatim match, we override the default by using the `-SimpğleMatch` switch&mdash; then we enter the path of the file.

The use of the cmdlet is straightforward:

<pre id="cmdln-text">
C:\Users\John\Documents>Select-String -Pattern "QUARTERLY" -SimpleMatch -Path .\Reports\Q1-2020.txt
2020 QUARTERLY REPORT

This is the report for the 1st quarter of 2020. We will provide
a brief summary of all the activities that have been organized
and carried out.
...
</pre>

Like `Get-Content`, this cmdlet also reads the standard input so it can be used with piping.

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem .\Reports | Select-String -Pattern "QUARTERLY"
2020 QUARTERLY REPORT

This is the report for the 1st quarter of 2020. We will provide
a brief summary of all the activities that have been organized
and carried out.
...
</pre>

Finally, using the powerful syntax of regular expressions, we can specify multiple pieces of text, and `Select-String` will spot it for you.

<pre id="cmdln-text">
C:\Users\John\Documents>Get-ChildItem -Path ".\Reports", ".\Minutes" | Select-String -Pattern "(report|events)"
2020 QUARTERLY REPORT

This is the report for the 1st quarter of 2020. We will provide
a brief summary of all the activites that have been organized
and carried out.
...

2021 QUARTERLY MEETING MINUTES

These minutes were recorded to report the results of the events
that were organized this quarter.
...
</pre>

Here, PowerShell found two files one of them containing '`report`' the other '`event`', and printed the files on the screen.

## Conclusion

The commands we have presented above, when combined imaginatively, should make it very easy to find what you are looking for. Whether it is the directories that are likely to contain the files you are looking for, whether it is properties such as extension, date of creation, or size that is likely to identify the file, or whether it is certain pieces of text that they may contain, PowerShell can spot what you are looking for and enumerate them on the terminal. It all depends on how concise and precise you are in specifying what you are searching for.

Good luck learning to use these very powerfull cmdlets.

<hr>

_Copyright&copy; 2024, John Saysitall_
