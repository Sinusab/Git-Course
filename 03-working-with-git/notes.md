# 🚀 Chapter 03: Working with Git

## 🎯 Key Concepts

- **Git Configuration**: Identity setup that permanently binds every commit to an author — the bedrock of audit trails and contribution graphs.
- **Repository Initialization**: `git init` creates the `.git/` database — idempotent, safe to re-run, and the birth of version history.
- **Tracking Lifecycle**: Untracked → Staged → Committed — the three states every file traverses under Git's supervision.
- **Workflow Discipline**: `Edit` → `git add` → `git commit` is not just a sequence; it is a contract for atomic, reviewable changes.
- **Commit Message Anatomy**: A structured artifact (summary + body) that serves humans, automation tools, and future-you — never an afterthought.

---

## 🔧 Commands Cheat Sheet

| Command                          | Purpose                                    | Example                                            |
| :------------------------------- | :----------------------------------------- | :------------------------------------------------- |
| `git config --global user.name`  | Set committer identity                     | `git config --global user.name "Your Name"`        |
| `git config --global user.email` | Bind email to commits                      | `git config --global user.email "you@example.com"` |
| `git config -l`                  | List all active configuration              | `git config -l`                                    |
| `git init`                       | Initialize repository in current directory | `git init`                                         |
| `ls -la .git/`                   | Inspect Git's internal database            | `ls -l .git/objects`                               |
| `git status`                     | Show working tree state                    | `git status -s`                                    |
| `git add <file>`                 | Stage file for next commit                 | `git add app.py`                                   |
| `git add .`                      | Stage all changes in working directory     | `git add .`                                        |
| `git commit`                     | Commit with editor-launched message        | `git commit`                                       |
| `git commit -m "msg"`            | Commit with inline message                 | `git commit -m "feat: add login"`                  |
| `git diff`                       | Show unstaged changes                      | `git diff README.md`                               |
| `git log`                        | Display commit history                     | `git log --oneline`                                |
| `cat .git/logs/HEAD`             | Raw reflog of HEAD movements               | `cat .git/logs/HEAD`                               |

---

## ⚙️ First Steps: Configuration & Initialization

Before writing a single line of code under Git's supervision, two foundational steps must be completed: **identity configuration** and **repository initialization**.

### 🆔 Git Configuration: Binding Identity to Every Commit

Git is not anonymous. Every commit records **who** made the change, **when**, and **what**. Without explicit configuration, Git either refuses to commit or attributes changes to a generic system user — breaking contribution graphs, audit trails, and team accountability.

#### 📝 Setting Global Identity

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

- `--global` writes to `~/.gitconfig` — applies across **all repositories** on the machine.
- Omit `--global` to set per-repository config (written directly to `.git/config`).
- Email serves as the primary key GitHub/GitLab use to link commits to your profile.

#### 🔍 Verifying Configuration

```bash
$ git config --global user.name
Your Name

$ git config --global user.email
you@example.com

$ git config -l                     # list ALL active config (global + local + system)
user.name=Your Name
user.email=you@example.com
init.defaultbranch=main
...
```

> ⚠️ **Critical Pitfall:** Forgetting `user.email` causes commits to appear as "unknown" on GitHub. The contribution graph (green squares) will never light up for those commits — even if you fix the config later. Historical commits retain their original author metadata permanently.

#### 🏛️ Configuration Scope Hierarchy

Git evaluates configuration from three distinct levels, with more specific scopes overriding broader ones:

| Scope      | File Location    | Use Case                                                     |
| :--------- | :--------------- | :----------------------------------------------------------- |
| **System** | `/etc/gitconfig` | Machine-wide defaults (rarely modified)                      |
| **Global** | `~/.gitconfig`   | User-level identity, editor, and aliases                     |
| **Local**  | `.git/config`    | Per-repo overrides (e.g., separate work vs. personal emails) |

```bash
# Check exactly where a specific value originates
git config --show-origin user.email
# file:/home/Your Name/.gitconfig    you@example.com
```

---

### 📦 Repository Initialization: Birth of the `.git/` Database

`git init` transforms an ordinary directory into a Git repository by creating the hidden `.git/` folder — Git's internal content-addressable database.

#### 🚀 Running `git init`

```bash
$ mkdir tmp && cd tmp
$ git init
hint: Using 'master' as the name for the initial branch...
hint:   git config --global init.defaultBranch <name>
Initialized empty Git repository in /home/user/project/.git/
```

#### 🗂️ What `git init` Actually Creates

```bash
$ ls -la
.  ..  .git

$ ls -l .git/
branches/  config  description  HEAD  hooks/  info/  objects/  refs/
```

| Directory / File | Architectural Purpose                                                              |
| :--------------- | :--------------------------------------------------------------------------------- |
| `objects/`       | Content-addressable store — stores blobs (files), trees (directories), and commits |
| `refs/`          | Pointers to commit hashes (branches, tags)                                         |
| `HEAD`           | Symbolic reference to the active branch (`ref: refs/heads/master`)                 |
| `config`         | Repository-specific local configuration                                            |
| `hooks/`         | Executable client-side lifecycle scripts                                           |
| `logs/`          | Reflog — chronological forensic record of HEAD and branch movements                |

> 💡 **Idempotency Guarantee:** Running `git init` multiple times in the same directory is **completely safe**. Git will not overwrite existing history or configurations. It simply ensures the directory structure exists, making it safe for automation scripts and CI pipelines.

#### 🏷️ The Default Branch Name Standard

Modern Git (≥2.28) issues a warning regarding legacy default branch nomenclature:

```text
hint: Using 'master' as the name for the initial branch. This default branch name
hint: is subject to change. To configure the initial branch name to use in all
hint: of your new repositories, call:
hint:   git config --global init.defaultBranch main
```

**Why this matters:** GitHub, GitLab, and modern CI/CD pipelines default to `main`. Aligning globally eliminates friction in automated workflows:

```bash
git config --global init.defaultBranch main
```

---

## 📌 Tracking Files: From Untracked to Staged

Git does not automatically monitor filesystem changes. You must explicitly register files through the **staging area** (also known as the index).

### 🔄 The Three File States in Action

#### 1️⃣ State: Untracked

```bash
$ echo "print('hi')" > test.py
$ python3 test.py
hi

$ git status
On branch master
No commits yet
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        test.py
nothing added to commit but untracked files present (use "git add" to track)
```

> Git sees `test.py` on disk but does not track its lifecycle.

#### 2️⃣ State: Staged

```bash
$ git add test.py
$ git status
On branch master
No commits yet
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   test.py
```

> File content is captured into `.git/objects/` and scheduled for the next commit snapshot.

#### 3️⃣ State: Committed

```bash
$ git commit -m "create my first file"
[master (root-commit) e4c08ea] create my first file
 1 file changed, 1 insertion(+)
 create mode 100644 test.py

$ git status
On branch master
nothing to commit, working tree clean
```

> Snapshot permanently recorded in repository history. Working directory is clean.

---

### ⚠️ Common Shell Mistake: `cat` vs `echo`

```bash
$ cat "print('hi')" > test.py
cat: 'print('\''hi'\'')': No such file or directory    # ❌ FAIL

$ echo "print('hi')" > test.py                        # ✅ SUCCESS
```

**Root Cause:** `cat` concatenates and reads **existing files**; it does not accept text literals as arguments. `echo` prints strings to standard output, which the shell redirection operator (`>`) pipes into a target file.

| Command                    | Primary Function                | Valid Syntax Example           |
| :------------------------- | :------------------------------ | :----------------------------- |
| `echo "text" > file`       | Write text string to a file     | `echo "print('hi')" > test.py` |
| `cat file`                 | Display file contents to stdout | `cat test.py`                  |
| `cat file1 file2 > merged` | Concatenate multiple files      | `cat a.txt b.txt > ab.txt`     |

> 💡 **Muscle Memory Rule:** Use `echo` to **create/write** strings to files. Use `cat` to **read/stream** file contents.

---

## 🔄 The Git Workflow in Action

The standard Git development loop follows an immutable cycle: **Edit → Stage → Commit → Repeat**.

### 🛠️ Step 1: Modify Existing File + Create New File

```bash
$ echo "print('hi')." > test.py          # modify tracked file
$ echo "print('goodbye')." > nothi.py    # create new file

$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   test.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        nothi.py

no changes added to commit (use "git add" and/or "git commit -a")
```

**Key Distinction:**

- **`modified`**: Tracked file with unstaged changes (`test.py`).
- **`untracked`**: New file completely unknown to Git (`nothi.py`).

### 📦 Step 2: Stage Both Modifications

```bash
$ git add nothi.py test.py
$ git status
On branch master
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   nothi.py
        modified:   test.py
```

> Both changes are assembled into the staging index for an atomic commit.

### 💾 Step 3: Commit

#### Option A: Editor-Launched Commit (Comprehensive)

```bash
$ git commit
# Opens configured text editor (nano/vim) with commit template:
#   Please enter the commit message for your changes...
#   # On branch master
#   # Changes to be committed:
#   #       new file:   nothi.py
#   #       modified:   test.py
```

Save (`Ctrl+O` → Enter) and exit (`Ctrl+X`) in nano.

#### Option B: Inline Message with `-m`

```bash
$ git commit -m "the change that git status understand"
[master b698c68] the change that git status understand
 2 files changed, 2 insertions(+), 1 deletion(-)
 create mode 100644 nothi.py
```

### ✅ Step 4: Verify Clean State

```bash
$ git status
On branch master
nothing to commit, working tree clean
```

---

## ✍️ Anatomy of a Professional Commit Message

A commit message is a **permanent engineering record**, not a temporary scratchpad.

### ❌ Anti-Pattern: Unstructured Commit

```bash
$ git commit -m "create my first file - this is not the best comment, we explain the good commit messages then."
```

**Core Issues:**

- ❌ Exceeds standard line length (95 characters).
- ❌ Blends subject and conversational meta-commentary into a single line.
- ❌ Lacks imperative mood and structured context.
- ❌ Fails to explain _why_ the modification exists.

---

### 📐 Standard Commit Architecture

```text
<type>(<optional scope>): <imperative summary max 50 chars>

[Optional body explaining the 'WHY' behind the change, wrapped at 72 chars]

[Optional footer: issue trackers, breaking changes, references]
```

#### 1️⃣ Summary Line Rules

- **Max 50 characters** — keeps `git log --oneline` readable.
- **Imperative mood** — "Add feature", not "Added feature" or "Adds feature".
- **Capitalized first letter**, no trailing period.
- Completes the sentence: _"If applied, this commit will..."_

#### 2️⃣ Body Rules

- Separated from summary by **exactly one blank line**.
- **Max 72 characters per line** to prevent terminal wrapping.
- Focuses on the **motivation and architectural reasoning**, not line-by-line diffs.

---

### 🔄 Refactoring Example: Before vs. After

#### ❌ Before

```text
create my first file - this is not the best comment, we explain the good commit messages then.
```

#### ✅ After

```text
feat: initialize project with hello world script

Add test.py as the first tracked file to establish
the repository baseline. Subsequent commits will
demonstrate proper workflow and message hygiene.

Refs: ch03-working-with-git practice session
```

---

### 🏷️ Conventional Commits Reference

| Type       | Semantic Intent                             | Production Example                               |
| :--------- | :------------------------------------------ | :----------------------------------------------- |
| `feat`     | Introduces a new feature                    | `feat(auth): add OAuth2 login flow`              |
| `fix`      | Resolves a software defect                  | `fix(api): handle null response payload`         |
| `docs`     | Documentation updates only                  | `docs(readme): update installation instructions` |
| `refactor` | Code restructuring without behavior changes | `refactor(db): extract connection pool logic`    |
| `test`     | Adding or correcting test suites            | `test(utils): cover boundary edge cases`         |
| `chore`    | Maintenance, dependencies, build configs    | `chore(ci): upgrade node runtime to 20`          |

> 💡 **Headline Rule:** The first line functions as an article title. Treat it like a newspaper headline: punchy, unambiguous, and immediately informative.

---

## 🔍 Inspecting History: `git log` & Internal Logs

### 📜 `git log`: Structured Narrative

```bash
$ git log
commit b698c6804618f6bc40f4517b0af9fc91d6485a31 (HEAD -> master)
Author: Your Name <you@example.com>
Date:   Wed Aug 13 20:15:51 2026 +0000

    the change that git status understand

commit e4c08eaff4d760c6a405645f2374ecf296ac0624
Author: Your Name <you@example.com>
Date:   Wed Aug 13 20:07:17 2026 +0000

    create my first file - this is not the best comment...
```

#### ⚡ Essential Navigation Flags

```bash
git log --oneline              # Compact: 7-char hash + summary line
git log --graph --oneline      # ASCII branch visualization
git log --stat                  # Shows modified file lists and insertion/deletion counts
git log -p                     # Generates full patch (diff) per commit
git log --author="Your Name"   # Filter commits by author
git log --since="2 weeks ago"  # Filter by relative timeframe
```

---

### 🧬 Low-Level Forensics: `.git/logs/` (The Reflog)

Git preserves every branch tip modification in chronological flat-text log files:

```bash
$ cat .git/logs/HEAD
0000000000000000000000000000000000000000 e4c08ea... Your Name <you@example.com> 1786717237 +0330	commit (initial): create my first file...
e4c08ea... b698c68... Your Name <you@example.com> 1786717751 +0330	commit: the change that git status understand
```

#### 🔍 Log Line Structure

```text
<old-sha> <new-sha> <committer-identity> <unix-timestamp> <timezone> <action-type>: <message>
```

> 💡 **The Safety Guarantee:** The reflog records every movement of `HEAD`. Even if commits become detached or branches are deleted via `git reset --hard`, commit objects remain accessible via reflog hashes for 30–90 days before garbage collection runs.

---

## 🛠️ Hands-On Lab: Terminal Reproduction

Recreate the complete workflow to establish muscle memory for states and transitions.

### 📋 Terminal Execution Sequence

```bash
# 1. Environment Initialization
mkdir ch03-practice && cd ch03-practice
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git init

# 2. File Creation & Execution Check
cat "print('hi')" > test.py                    # Observe expected error
echo "print('hi')" > test.py                   # Correct approach
python3 test.py                                # Verify output: hi

# 3. Track, Inspect, and Commit
git status                                     # State: Untracked
git add test.py
git status                                     # State: Staged
git commit -m "feat: add hello world script"   # State: Committed

# 4. Multi-File Lifecycle Transitions
echo "print('hi')." > test.py                  # State: Modified
echo "print('goodbye')." > nothi.py            # State: Untracked
git status

# 5. Staging & Atomic Commit
git add nothi.py test.py
git status                                     # Both changes staged
git commit -m "feat: add goodbye script and update greeting"

# 6. Historical Inspection
git log --oneline
cat .git/logs/HEAD                             # Inspect low-level reflog
git show HEAD                                  # Inspect patch of latest commit
```

### 🎯 Verification Checklist

- [ ] Captured `git status` displaying both `modified` and `untracked` files simultaneously.
- [ ] Confirmed sequential entries logged inside `cat .git/logs/HEAD`.
- [ ] Articulated why Git enforces explicit staging via `git add` instead of automatic tracking.

---

## 💡 Key Takeaways

> **Configuration is Identity.** `user.name` and `user.email` are the immutable cryptographic bindings between author and commit. Set them globally from day one.

> **`git init` is Idempotent.** Running `git init` inside an existing repository is completely safe and non-destructive.

> **Staging is Intentional Architecture.** Unlike legacy systems with blind commits, Git's staging area gives you total control to craft clean, atomic snapshots.

> **Commit Messages are Infrastructure.** High-quality summaries and bodies drive automated semantic releases, changelogs, and rapid debugging.

> **The Reflog Never Forgets.** While `git log` displays your curated repository tree, `.git/logs/HEAD` stores the raw operational truth for forensic recovery.
