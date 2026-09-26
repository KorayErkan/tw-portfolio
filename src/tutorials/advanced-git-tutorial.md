# Advanced Git Version Control

[_John Saysitall_](mailto:john.saysitall@goodcode.example)

This document explains how advanced Git commands can be used to manage complex project histories, collaborate effectively with teams, and maintain clean, professional codebases.

---

## Table of Contents

* [Introduction](#introduction)
* [Essential Advanced Commands](#essential-advanced-commands)
* [Visualizing Commit History](#visualizing-commit-history)
* [Interactive Rebasing](#interactive-rebasing)
* [Branch Management Strategies](#branch-management-strategies)
* [Stashing Work](#stashing-work)
* [Cherry-picking Commits](#cherry-picking-commits)
* [Recovery and Debugging](#recovery-and-debugging)
* [Advanced Merging Techniques](#advanced-merging-techniques)
* [Collaborative Workflows](#collaborative-workflows)
* [Conclusion](#conclusion)

---

## Introduction

While basic Git commands like `add`, `commit`, and `push` are sufficient for simple projects, professional software development requires mastery of Git's more sophisticated features. These advanced capabilities become essential when working with multiple developers, managing complex feature branches, or maintaining production codebases where history cleanliness and precise change control matter.

The difference between a novice and expert Git user often lies not in knowing _more_ commands, but in understanding _when_ and _how_ to use powerful tools like interactive rebasing, cherry-picking, and the reflog. These features can transform chaotic development workflows into clean, traceable histories that tell the story of how your project evolved.

Several of these operations rewrite history, so for each one we note when it is safe to use.

> <span id="note-byline">This tutorial assumes familiarity with basic Git concepts including repositories, commits, branches, and merging. We focus exclusively on advanced techniques that experienced developers use to manage complex projects.</span>

## Essential Advanced Commands

Before diving into specific workflows, let's examine the core advanced commands that separate expert Git users from beginners. Each of these serves a specific purpose in professional development environments:

|Command|Purpose|
|-|-|
|`git log --oneline`|Display condensed commit history for easy navigation|
|`git rebase -i`|Interactively rewrite commit history|
|`git stash`|Temporarily save uncommitted work|
|`git cherry-pick`|Apply specific commits from other branches|
|`git reflog`|View complete history of HEAD movements for recovery|
|`git bisect`|Use binary search to locate bug-introducing commits|

Unlike basic Git commands that primarily add new information to your repository, these advanced tools frequently _modify_ existing history or provide sophisticated views into that history. This makes them powerful but potentially dangerous if used incorrectly.

The most important principle when using these commands is understanding whether you're working with _local_ history (safe to modify) or _shared_ history (dangerous to modify after pushing). We'll emphasize this distinction throughout our examples.

## Visualizing Commit History

Before manipulating Git history, you need to understand what that history looks like. The `git log --oneline` command provides the most useful condensed view of your project's development:

<pre id="cmdln-text">
$ git log --oneline
3f9a2c1 Fix authentication bug in login module
7b4e8d2 Add user profile picture upload feature
c2d61a5 Refactor database connection pooling
9e05b37 Update README with installation instructions
1a7f4e0 Initial project setup
</pre>

This format shows the abbreviated commit hash on the left and the commit message on the right, making it easy to quickly scan through project history. The most recent commits appear at the top.

You can limit the output to see only recent commits by specifying a number:

<pre id="cmdln-text">
$ git log --oneline -3
3f9a2c1 Fix authentication bug in login module
7b4e8d2 Add user profile picture upload feature
c2d61a5 Refactor database connection pooling
</pre>

For branches with complex histories, adding the `--graph` option reveals the branching structure. On the `develop` branch of the same project, for example, the profile-upload work was merged in from a feature branch instead of being committed directly:

<pre id="cmdln-text">
$ git log --oneline --graph develop
*   5d3c9f8 Merge branch 'feature/profile-upload' into develop
|\
| * e81b0a6 Add image validation to upload
| * 46fa2d9 Implement profile picture storage
|/
* c2d61a5 Refactor database connection pooling
* 9e05b37 Update README with installation instructions
* 1a7f4e0 Initial project setup
</pre>

This visualization becomes invaluable when planning rebase operations or understanding how different branches relate to each other. The commit hashes shown here are what you'll use with commands like `cherry-pick` and interactive rebase.

> <span id="note-byline">Commit hashes in Git are actually 40-character SHA-1 values, but Git allows you to use abbreviated versions (typically the first 7 hexadecimal digits) as long as they're unique within your repository.</span>

## Interactive Rebasing

Interactive rebasing is Git's most powerful history-editing tool. It allows you to rewrite commit history by combining, reordering, editing, or removing commits. This is essential for maintaining clean project histories before sharing work with others.

The basic syntax for interactive rebase is:

<pre id="cmdln-text">
$ git rebase -i HEAD~3
</pre>

This opens an editor listing the last 3 commits, _oldest first_ (the reverse of `git log`), with options for how to handle each:

<pre id="cmdln-text">
pick c2d61a5 Refactor database connection pooling
pick 7b4e8d2 Add user profile picture upload feature
pick 3f9a2c1 Fix authentication bug in login module

# Rebase 9e05b37..3f9a2c1 onto 9e05b37 (3 commands)
#
# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like "squash", but discard this commit's log message
# d, drop = remove commit
# ...
</pre>

The most common operations are:

**Rewording commit messages** using the `reword` command. Change `pick` to `reword` (or just `r`) for any commit whose message you want to improve:

<pre id="cmdln-text">
pick c2d61a5 Refactor database connection pooling
r 7b4e8d2 Add user profile picture upload feature
pick 3f9a2c1 Fix authentication bug in login module
</pre>

After you save and close this file, Git replays the commits in order and stops at the specified commit and allow you to edit its message:

<pre id="cmdln-text">
Add comprehensive user profile picture upload feature

- Supports JPEG, PNG, and WebP formats
- Includes client-side image compression
- Validates file size limits (max 5MB)
- Integrates with existing user management system
</pre>

**Squashing multiple commits** combines several related commits into one. This is useful when you've made multiple small commits while developing a feature. For example, had we run `git rebase -i develop` on the `feature/profile-upload` branch before merging it, we could have folded its three commits into one:

<pre id="cmdln-text">
pick 46fa2d9 Implement profile picture storage
squash e81b0a6 Add image validation to upload
squash 0c9d8e4 Fix upload error handling
</pre>

Git will combine these commits and prompt you to write a new commit message that represents all the combined changes.

**Reordering commits** is accomplished by simply changing the order of lines in the interactive rebase file. However, be careful that reordered commits don't have dependencies on each other.

> <span id="warning-byline">Never rebase commits that have already been pushed to shared repositories unless you're absolutely certain no one else is working with those commits. Rewriting shared history can create serious problems for collaborators.</span>

## Branch Management Strategies

Effective branch management becomes crucial as projects grow in complexity. Advanced Git users leverage specific branching patterns to maintain clean histories and enable parallel development workflows.

The key to professional branch management is understanding the relationship between different types of branches and when to use linear history versus merge commits:

<pre id="cmdln-text">
$ git branch --list
  develop
* feature/payment-integration
  feature/user-authentication
  hotfix/security-patch
  main
</pre>

Git lists branches alphabetically and marks the one you have checked out with an asterisk.

**Feature branches** should maintain clean, focused histories. Before merging a feature branch, use interactive rebase to ensure commits are logical and well-documented:

<pre id="cmdln-text">
$ git checkout feature/payment-integration
$ git rebase -i main
</pre>

This rebases your feature branch onto the latest main branch and allows you to clean up commits before integration.

**Cleaning up merged branches** prevents repository clutter. After a feature branch has been successfully merged, remove both local and remote tracking references:

<pre id="cmdln-text">
$ git branch -d feature/user-authentication
$ git push origin --delete feature/user-authentication
$ git remote prune origin
</pre>

The `-d` flag safely deletes branches that have been merged, while `--delete` removes the remote branch. The `prune` command cleans up stale remote-tracking branches.

**Branch naming conventions** improve team coordination. Use descriptive prefixes that indicate the branch purpose:

* `feature/` for new functionality
* `hotfix/` for urgent production fixes
* `bugfix/` for non-urgent bug repairs
* `refactor/` for code improvement without functional changes

**Fast-forward merges** maintain linear history when possible. If your feature branch is based on the current tip of the target branch, Git can perform a fast-forward merge:

<pre id="cmdln-text">
$ git checkout main
$ git merge --ff-only feature/payment-integration
</pre>

The `--ff-only` flag ensures the merge will fail if a fast-forward isn't possible, preventing unexpected merge commits.

## Stashing Work

The `git stash` command provides a temporary storage mechanism for uncommitted changes, allowing you to quickly switch contexts without making premature commits. This becomes essential when you need to handle urgent tasks while in the middle of developing a feature.

**Basic stashing** saves both staged and unstaged changes to tracked files (add `-u` to include untracked files as well):

<pre id="cmdln-text">
$ git status
On branch feature/user-dashboard
Changes to be committed:
  modified:   src/dashboard.js
Changes not staged for commit:
  modified:   src/utils.js

$ git stash
Saved working directory and index state WIP on feature/user-dashboard: 8c1e5fa Add dashboard framework

$ git status
On branch feature/user-dashboard
nothing to commit, working tree clean
</pre>

Your working directory is now clean, allowing you to switch branches or pull updates without conflicts.

**Managing multiple stashes** requires descriptive messages. Suppose that, back on the feature branch, you have started restyling the dashboard and have to switch context again. This time, give the stash a meaningful description:

<pre id="cmdln-text">
$ git status --short
 M src/dashboard.css

$ git stash push -m "Dashboard styling in progress - responsive grid layout"
Saved working directory and index state On feature/user-dashboard: Dashboard styling in progress - responsive grid layout
</pre>

View your stash list to see all saved work:

<pre id="cmdln-text">
$ git stash list
stash@{0}: On feature/user-dashboard: Dashboard styling in progress - responsive grid layout
stash@{1}: WIP on feature/user-dashboard: 8c1e5fa Add dashboard framework
stash@{2}: On feature/user-authentication: Login form validation
</pre>

**Applying stashed changes** can be done in several ways. To apply the most recent stash and remove it from the stash list:

<pre id="cmdln-text">
$ git stash pop
</pre>

Alternatively, to apply a specific stash without removing it from the list:

<pre id="cmdln-text">
$ git stash apply stash@{1}
</pre>

Note that the indexes shift down whenever an entry is removed: after a `pop`, the former `stash@{1}` becomes `stash@{0}`.

This is useful when you want to apply the same changes to multiple branches.

**Selective stashing** allows you to stash only specific files or even specific lines within files:

<pre id="cmdln-text">
$ git stash push -m "Only utility functions" src/utils.js
$ git stash push --patch -m "Selected dashboard changes"
</pre>

The `--patch` option lets you interactively choose which changes to stash, providing fine-grained control over what gets saved.

**Creating branches from stashes** is useful when stashed work grows into a larger feature:

<pre id="cmdln-text">
$ git stash branch feature/responsive-design stash@{0}
</pre>

This creates a new branch from the commit where the stash was created and applies the stashed changes, providing a clean starting point for continued development.

## Cherry-picking Commits

Cherry-picking allows you to apply specific commits from one branch to another, providing surgical precision when you need particular changes without merging entire branches. This technique is invaluable for applying hotfixes across multiple release branches or selectively incorporating features.

**Basic cherry-picking** uses the commit hash from `git log --oneline`:

<pre id="cmdln-text">
$ git log --oneline feature/security-improvements
b6e2f47 Add input validation to user forms
58ad0c3 Implement rate limiting for API endpoints
f13c9e8 Update password hashing algorithm
2d7a4b9 Fix SQL injection vulnerability
</pre>

To apply just the password hashing improvement to your current branch:

<pre id="cmdln-text">
$ git cherry-pick f13c9e8
[feature/user-auth 6a0d5e2] Update password hashing algorithm
 Date: Wed Oct 15 14:30:22 2023 -0400
 2 files changed, 15 insertions(+), 8 deletions(-)
</pre>

Git creates a new commit with the same changes but a different hash, since the commit now exists in a different context.

**Cherry-picking multiple commits** can be done in one command. To apply the SQL injection fix and the rate limiting change:

<pre id="cmdln-text">
$ git cherry-pick 2d7a4b9 58ad0c3
</pre>

This applies the commits in the order specified, which may be different from their original chronological order.

**Range cherry-picking** applies a series of consecutive commits:

<pre id="cmdln-text">
$ git cherry-pick 2d7a4b9..58ad0c3
</pre>

This picks all commits after `2d7a4b9` (exclusive) up to `58ad0c3` (inclusive), that is, `f13c9e8` and `58ad0c3`. To include the first commit as well, write `2d7a4b9^..58ad0c3`. Be careful with ranges to ensure you're picking the commits you intend.

**Handling cherry-pick conflicts** requires the same conflict resolution skills as merging:

<pre id="cmdln-text">
$ git cherry-pick 2d7a4b9
Auto-merging src/auth.js
CONFLICT (content): Merge conflict in src/auth.js
error: could not apply 2d7a4b9... Fix SQL injection vulnerability
hint: After resolving the conflicts, mark them with
hint: "git add/rm &lt;pathspec&gt;", then run
hint: "git cherry-pick --continue".
hint: You can instead skip this commit with "git cherry-pick --skip".
hint: To abort and get back to the state before "git cherry-pick",
hint: run "git cherry-pick --abort".
</pre>

Resolve conflicts manually, then continue:

<pre id="cmdln-text">
$ git add src/auth.js
$ git cherry-pick --continue
</pre>

If the conflicts are too complex, you can abort the cherry-pick:

<pre id="cmdln-text">
$ git cherry-pick --abort
</pre>

**Cherry-picking without committing** allows you to review changes before finalizing them:

<pre id="cmdln-text">
$ git cherry-pick --no-commit f13c9e8
$ git status
On branch feature/user-auth
Changes to be committed:
  modified:   src/password-utils.js
  modified:   tests/auth-tests.js
</pre>

This stages the changes but doesn't create a commit, giving you the opportunity to modify or combine the changes before committing.

## Recovery and Debugging

Even experienced Git users occasionally make mistakes that seem to lose work or create confusing repository states. Git's reflog and bisect commands provide powerful recovery and debugging capabilities that can save both time and sanity.

**The reflog is Git's safety net.** It records every change to HEAD, including commits, merges, resets, and rebases. Even if commits seem "lost," they're usually recoverable through the reflog. Here is the reflog of `main` after the reword rebase from the [Interactive Rebasing](#interactive-rebasing) section:

<pre id="cmdln-text">
$ git reflog
0e6b7d5 HEAD@{0}: rebase (finish): returning to refs/heads/main
0e6b7d5 HEAD@{1}: rebase (pick): Fix authentication bug in login module
a4c19e3 HEAD@{2}: rebase (reword): Add comprehensive user profile picture upload feature
7b4e8d2 HEAD@{3}: rebase: fast-forward
c2d61a5 HEAD@{4}: rebase (start): checkout HEAD~3
3f9a2c1 HEAD@{5}: commit: Fix authentication bug in login module
7b4e8d2 HEAD@{6}: commit: Add user profile picture upload feature
</pre>

The rebase gave the reworded commit and every commit after it new hashes (`a4c19e3` and `0e6b7d5`), but the originals (`7b4e8d2` and `3f9a2c1`) are still listed. Resetting the branch to one of these entries, for example with `git reset --hard HEAD@{5}`, would bring back the pre-rebase history.

**Recovering from hard resets** is a common reflog use case. Suppose you accidentally ran `git reset --hard` and lost recent work:

<pre id="cmdln-text">
$ git reset --hard HEAD~4
HEAD is now at 1a7f4e0 Initial project setup
$ git log --oneline
1a7f4e0 Initial project setup

$ git reflog
1a7f4e0 HEAD@{0}: reset: moving to HEAD~4
0e6b7d5 HEAD@{1}: rebase (finish): returning to refs/heads/main
0e6b7d5 HEAD@{2}: rebase (pick): Fix authentication bug in login module
</pre>

Your recent commits still exist and can be restored:

<pre id="cmdln-text">
$ git reset --hard HEAD@{1}
HEAD is now at 0e6b7d5 Fix authentication bug in login module
$ git log --oneline
0e6b7d5 Fix authentication bug in login module
a4c19e3 Add comprehensive user profile picture upload feature
c2d61a5 Refactor database connection pooling
9e05b37 Update README with installation instructions
1a7f4e0 Initial project setup
</pre>

> <span id="note-byline">The reflog is local to your clone, and its entries expire (by default, entries for commits no longer on any branch after 30 days). Recover lost work promptly.</span>

**Binary search debugging with bisect** helps locate the specific commit that introduced a bug. Start by identifying a known good commit and a known bad commit:

<pre id="cmdln-text">
$ git bisect start
$ git bisect bad HEAD
$ git bisect good v2.1.0
Bisecting: 6 revisions left to test after this (roughly 3 steps)
[4f8b1c6e0a93d27f51b8c4e6a2d09f7b3c15e8a4] Implement caching for database queries
</pre>

Git checks out a commit halfway between good and bad. Test your application, then mark the commit:

<pre id="cmdln-text">
$ npm test
# Tests pass
$ git bisect good
Bisecting: 3 revisions left to test after this (roughly 2 steps)
[d93e2a7b5c18f04e6a2d9c7b31f58e0a4c6d2b19] Refactor user authentication flow
</pre>

Continue testing and marking commits until Git identifies the problematic commit:

<pre id="cmdln-text">
$ npm test
# Tests fail
$ git bisect bad
Bisecting: 1 revision left to test after this (roughly 1 step)
[b4c5d6e8a1f23b907c4e5d6a8b2f19c03e7d4a56] Update session handling logic

$ npm test
# Tests fail
$ git bisect bad
Bisecting: 0 revisions left to test after this (roughly 0 steps)
[5a2c7f9d3e81b4c60a7f2e9d5b18c34a6e0f7d21] Add session timeout setting

$ npm test
# Tests pass
$ git bisect good
b4c5d6e8a1f23b907c4e5d6a8b2f19c03e7d4a56 is the first bad commit
commit b4c5d6e8a1f23b907c4e5d6a8b2f19c03e7d4a56
Author: Jane Developer &lt;jane.developer@goodcode.example&gt;
Date:   Mon Oct 14 10:15:30 2023 -0400

    Update session handling logic

 src/session.js | 12 ++++++------
 1 file changed, 6 insertions(+), 6 deletions(-)
</pre>

Bisect prints full 40-digit hashes; their first 7 digits are the abbreviated hashes you see elsewhere.

End the bisect session and return to your original branch:

<pre id="cmdln-text">
$ git bisect reset
</pre>

**Automated bisect testing** can run tests automatically at each step:

<pre id="cmdln-text">
$ git bisect run npm test
</pre>

Run `git bisect start`, `git bisect bad`, and `git bisect good` first, as above. Git then runs the test command at each step, marking the commit good if it exits with code 0 and bad if it exits with a code from 1 to 127 (except 125, which means "skip this commit"), until the problematic commit is found.

## Advanced Merging Techniques

While basic merging handles most scenarios automatically, complex projects often require more sophisticated merge strategies to handle conflicts, preserve history, or integrate changes according to specific project requirements.

**Merge strategies and strategy options** control how Git combines branches. The two are easy to confuse: a _strategy_ (`-s`) selects the merge algorithm, while a _strategy option_ (`-X`) fine-tunes the default algorithm:

<pre id="cmdln-text">
$ git merge feature/payment-system
$ git merge -X ours feature/payment-system
$ git merge -X theirs feature/payment-system
$ git merge feature/auth feature/payments feature/reporting
</pre>

* The first command uses the default two-branch strategy, `ort` (Git 2.34 and later; earlier versions use `recursive`).
* `-X ours` and `-X theirs` still merge every non-conflicting change from both branches. Only where the same lines conflict does Git automatically keep our side or their side, respectively.
* Merging more than two branches at once uses the `octopus` strategy automatically. It stops if any conflict needs manual resolution.

> <span id="warning-byline">Do not confuse `-X ours` with `-s ours` (`--strategy=ours`). The `ours` _strategy_ discards **everything** from the other branch and records a merge commit with your tree unchanged. Use it only to mark a branch as superseded (for example, `git merge -s ours legacy/old-api`), never to "prefer our side" when merging a branch whose changes you need, such as a security fix.</span>

**Three-way merge conflicts** are easier to resolve when you can also see the original common ancestor. By default, Git shows only the two sides. To include the ancestor, enable the `diff3` conflict style (or `zdiff3`, available since Git 2.35, which also trims lines common to both sides):

<pre id="cmdln-text">
$ git config --global merge.conflictStyle diff3
</pre>

A conflict then looks like this:

<pre id="cmdln-text">
$ git merge feature/api-refactor
Auto-merging src/api-client.js
CONFLICT (content): Merge conflict in src/api-client.js

$ cat src/api-client.js
function makeRequest(url, options) {
&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD
    return fetch(url, {
        ...options,
        signal: AbortSignal.timeout(5000)
    });
||||||| 2b7e0c4
    return fetch(url, options);
=======
    return fetch(url, options).then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response;
    });
&gt;&gt;&gt;&gt;&gt;&gt;&gt; feature/api-refactor
}
</pre>

The section between `<<<<<<< HEAD` and `|||||||` shows your current branch's version. The section between `|||||||` and `=======` shows the common ancestor (labelled with its abbreviated hash), and the section between `=======` and `>>>>>>>` shows the incoming changes. Comparing each side with the ancestor reveals what each branch intended: yours added a five-second timeout, and theirs added rejection of unsuccessful HTTP responses.

**Resolving complex conflicts** often requires keeping the intent of both sets of changes:

<pre id="cmdln-text">
function makeRequest(url, options) {
    return fetch(url, {
        ...options,
        signal: AbortSignal.timeout(5000)
    }).then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response;
    });
}
</pre>

After manually resolving the conflict by combining both improvements, mark the file as resolved:

<pre id="cmdln-text">
$ git add src/api-client.js
$ git commit
</pre>

**Merge conflict resolution tools** can simplify complex conflicts. Configure a visual merge tool:

<pre id="cmdln-text">
$ git config merge.tool vimdiff
$ git mergetool
</pre>

This opens a three-way diff view showing the base version, your changes, and the incoming changes, making it easier to understand and resolve conflicts.

**Aborting problematic merges** returns your repository to its pre-merge state:

<pre id="cmdln-text">
$ git merge --abort
</pre>

This is safer than trying to force through a complex merge that you don't fully understand.

**Fast-forward vs. true merges** control whether Git creates merge commits. Sometimes you want to preserve the branching structure:

<pre id="cmdln-text">
$ git merge --no-ff feature/user-dashboard
</pre>

The `--no-ff` flag forces creation of a merge commit even when a fast-forward merge would be possible, preserving the historical context that work was done on a separate branch.

## Collaborative Workflows

Professional Git usage involves coordinating with team members while maintaining repository quality. Advanced collaborative workflows leverage Git's distributed nature to enable effective teamwork without compromising project stability.

**Upstream repository management** becomes essential when contributing to open source projects or working with forked repositories:

<pre id="cmdln-text">
$ git remote add upstream https://git.goodcode.example/original/project.git
$ git remote -v
origin    https://git.goodcode.example/yourfork/project.git (fetch)
origin    https://git.goodcode.example/yourfork/project.git (push)
upstream  https://git.goodcode.example/original/project.git (fetch)
upstream  https://git.goodcode.example/original/project.git (push)
</pre>

Keep your fork synchronized with the upstream repository:

<pre id="cmdln-text">
$ git fetch upstream
$ git checkout main
$ git merge upstream/main
$ git push origin main
</pre>

**Rebase-based workflow** maintains linear history even in collaborative environments. Before pushing feature work, rebase onto the latest main branch:

<pre id="cmdln-text">
$ git checkout feature/user-notifications
$ git fetch origin
$ git rebase origin/main
</pre>

If there are conflicts during rebase, resolve them commit by commit:

<pre id="cmdln-text">
$ git status
rebase in progress; onto 72c4a0f
You are currently rebasing branch 'feature/user-notifications' on '72c4a0f'.
  (fix conflicts and then run "git rebase --continue")

Unmerged paths:
  both modified:   src/notifications.js

$ vim src/notifications.js  # resolve conflicts
$ git add src/notifications.js
$ git rebase --continue
</pre>

**Force pushing safely** requires understanding when history rewriting is appropriate. Never force push to shared branches like `main`, but a feature branch owned by a single developer can be force pushed after rebasing.

A plain `--force-with-lease` is safer than `--force`: it refuses the push if the remote branch no longer matches your _remote-tracking_ branch (`origin/feature/user-notifications`). However, that protection disappears as soon as you fetch. The `git fetch origin` above silently updates the remote-tracking branch, so if a teammate had pushed to your feature branch in the meantime, a plain `--force-with-lease` would overwrite their commits without complaint.

To make the lease reliable, record the remote commit you last saw _before_ fetching, and name it explicitly when pushing:

<pre id="cmdln-text">
$ expected=$(git rev-parse origin/feature/user-notifications)
$ git fetch origin
$ git rebase origin/main
$ git push --force-with-lease=feature/user-notifications:$expected origin feature/user-notifications
</pre>

If anyone has pushed to the branch since you recorded `$expected`, Git rejects the push with `(stale info)`, and you can fetch and integrate their work first. (Git 2.30 and later also offer `--force-if-includes`, which adds a similar check automatically.)

**Pull request preparation** involves cleaning up commits and ensuring clear commit messages:

<pre id="cmdln-text">
$ git log --oneline origin/main..feature/user-notifications
6c2e9a1 Add email notification templates
0b8f3d4 Implement notification delivery service
a95e7c2 Add user notification preferences
3d1b6f8 Create notification database schema
</pre>

This shows all commits that will be included in the pull request. Use interactive rebase to clean up the history if necessary.

**Handling feedback on pull requests** often requires amending commits or adding new ones. If you need to modify an existing commit after review:

<pre id="cmdln-text">
$ git add src/delivery-service.js
$ git commit --fixup 0b8f3d4
$ git rebase -i --autosquash origin/main
</pre>

The `--fixup` option creates a commit marked for squashing with an existing commit, and `--autosquash` automatically orders the interactive rebase to perform the fixup.

**Branch protection and review workflows** integrate with advanced Git techniques. Understanding how your team's branching strategy affects which Git commands you can use is crucial for effective collaboration.

## Conclusion

Each of these tools has a clear use. Interactive rebase prepares clean feature branches for integration. Cherry-picking applies specific fixes across branches. The stash handles context switches without premature commits. The reflog recovers work after a bad reset or rebase, and bisect finds the commit that introduced a bug. Merge strategy options and the `diff3` conflict style make complex integrations manageable.

Before running any history-rewriting command, ask whether the commits involved are local or already shared, and agree with your team on when rebasing and force pushing are acceptable. Practice these commands in a scratch repository first.

<hr>

_Copyright&copy; 2024, John Saysitall_
