# 🚀 Chapter 05: Undoing Changes in Git

## 🎯 Key Concepts

- **Pre-Commit Recovery**: `git restore` and `git restore --staged` safely discard or unstage changes before they enter history.
- **Commit Amendment**: `git commit --amend` rewrites the most recent commit — powerful for local fixes, dangerous on shared branches.
- **Safe Rollback**: `git revert` creates a new commit that inverses a previous change, preserving full history for public/shared repositories.
- **SHA-1 Integrity**: Every Git object is identified by a cryptographic hash derived from its content, author, timestamp, and parent — any alteration produces a completely different hash.
- **Decision Framework**: Choosing between `restore`, `amend`, `reset`, and `revert` depends entirely on whether the change is staged, committed locally, or already pushed.

---

## 🔧 Commands Cheat Sheet

| Command                       | Purpose                                            | Safety Level                            |
| :---------------------------- | :------------------------------------------------- | :-------------------------------------- |
| `git restore <file>`          | Discard unstaged working directory changes         | ✅ Safe (matches last committed state)  |
| `git restore --staged <file>` | Unstage file without discarding changes            | ✅ Safe                                 |
| `git commit --amend`          | Rewrite the most recent commit (message + content) | ⚠️ Local only — never on pushed commits |
| `git commit --amend -m "msg"` | Amend with inline message (skip editor)            | ⚠️ Same as above                        |
| `git revert <commit>`         | Create inverse commit to undo a specific change    | ✅ Safe for shared/public branches      |
| `git show <ref>`              | Inspect commit metadata and diff                   | ✅ Read-only                            |
| `git log -p`                  | View full patch history                            | ✅ Read-only                            |
| `git stash`                   | Temporarily shelve uncommitted changes             | ✅ Safe                                 |

---

## 🔄 Pre-Commit Recovery: Fixing Mistakes Before They Stick

The safest time to fix a mistake is **before it enters Git history**. Git provides two dedicated commands for this phase.

### 🗑️ Discarding Unstaged Changes: `git restore <file>`

When you modify a tracked file but haven't staged it yet, `git restore` replaces the working copy with the last committed version:

```bash
# Accidental edits added to chapter1.txt
$ git status
Changes not staged for commit:
        modified:   chapter1.txt

$ git restore chapter1.txt
# File reverted to last committed state instantly
```

> 💡 **Modern Replacement:** `git restore` supersedes the legacy `git checkout -- <file>` syntax. While `checkout` still works, `restore` was introduced in Git 2.23 specifically to separate "undo working tree changes" from "switch branches" — eliminating a major source of confusion.

---

### 📦 Unstaging Without Losing Work: `git restore --staged <file>`

If you accidentally staged the wrong file or aren't ready to commit yet:

```bash
$ git add chapter1.txt          # Staged prematurely
$ git restore --staged chapter1.txt
$ git status
Changes not staged for commit:
        modified:   chapter1.txt    # Change preserved, just unstaged
```

This moves the file back from Index to Working Directory. **No data is lost.**

---

### 🏛️ Legacy Equivalent: `git reset <file>`

Before Git 2.23, unstaging required `git reset`:

```bash
git reset HEAD chapter1.txt     # Older equivalent of git restore --staged
```

Both achieve identical results. Prefer `git restore --staged` for clarity — its name explicitly communicates intent.

---

## ✏️ Commit Amendment: Rewriting the Latest Snapshot

`git commit --amend` replaces the most recent commit entirely. It can modify the commit message, add forgotten files, or remove accidentally included files.

### ⚙️ How Amend Works Internally

Amend does **not** edit an existing commit in place. It:

1. Creates a brand-new commit object with updated content/message.
2. Points the current branch tip to this new commit.
3. Leaves the old commit orphaned (eventually garbage-collected).

This means the commit hash **always changes**, even if only the message is corrected.

---

### 📝 Use Case 1: Fixing a Commit Message

```bash
$ git commit -m "wrong commit"
$ git commit --amend -m "feat: add chapter 1 content validation"
# New commit created with corrected message; old hash replaced
```

---

### 📂 Use Case 2: Adding Forgotten Files

```bash
$ git commit -m "add chapter 3,4"       # Forgot chapter4.txt!
$ git add chapter4.txt
$ git commit --amend --no-edit           # Keep same message, add staged file
# Result: single commit containing both chapter3.txt AND chapter4.txt
```

The `--no-edit` flag skips the editor when you only want to update content, not the message.

---

### ⚠️ Critical Safety Boundary

| Scenario                             | Safe to Amend? | Reason                                                                    |
| :----------------------------------- | :------------- | :------------------------------------------------------------------------ |
| **Local commit, never pushed**       | ✅ Yes         | No one else references this hash                                          |
| **Pushed to remote**                 | ❌ Never       | Collaborators' clones reference the old hash; force-push required to sync |
| **Shared branch (`main`/`develop`)** | ❌ Never       | History rewriting breaks everyone's local copies                          |
| **Feature branch, solo developer**   | ✅ Yes         | Only your own work is affected                                            |

> 💡 **Golden Rule:** Treat `--amend` as a **local-only tool**. Once a commit exists on any remote, use `git revert` instead. When a hash changes, anyone who pulled the original hash will experience divergent history.

---

## ↩️ Safe Rollback: `git revert` for Public History

Unlike `amend` and `reset`, `git revert` **never rewrites history**. It creates a new commit that applies the exact inverse of a specified commit.

### 🛠️ How Revert Works

```bash
$ git revert HEAD
# Creates new commit: "Revert 'feat: add broken feature'"
# Original commit remains in history untouched
```

The resulting commit contains:

- An auto-generated message referencing the reverted commit hash.
- A diff that precisely undoes every line added/removed in the target commit.
- Full traceability: future readers see both the original change and its reversal.

---

### 🎯 Reverting Non-HEAD Commits

You can revert any commit in history by specifying its hash:

```bash
$ git revert 6ab7907
# Creates inverse commit for target snapshot
# Deletes files/lines added in 6ab7907 without wiping history
```

This is essential for fixing bugs introduced several commits ago without disturbing intermediate work.

---

### ⚖️ Revert vs. Reset: When to Use Which

| Dimension                     | `git revert`                                 | `git reset`                               |
| :---------------------------- | :------------------------------------------- | :---------------------------------------- |
| **History**                   | Preserved (new commit added)                 | Rewritten (commits removed/altered)       |
| **Safety on shared branches** | ✅ Safe                                      | ❌ Dangerous                              |
| **Visibility of mistakes**    | Transparent — mistake and fix both visible   | Hidden — history appears clean            |
| **Collaboration impact**      | None                                         | Requires force-push and team coordination |
| **Best for**                  | Production bugs, public repos, team branches | Local cleanup, pre-push corrections       |

> 💡 **Professional Standard:** In any collaborative environment, `git revert` is the default undo mechanism. `reset` is reserved for local-only recovery scenarios where no one else has pulled the affected commits.

---

## 🔐 SHA-1: The Cryptographic Backbone

Every Git object (blob, tree, commit, tag) is identified by a 40-character SHA-1 hash. This is not arbitrary naming — it is fundamental to Git's integrity model.

### 🧩 What Determines a Commit Hash?

A commit's SHA-1 is computed from:

- Tree hash (snapshot of all files at that point)
- Parent commit hash(es)
- Author name and email
- Committer name and email
- Timestamps (author date + committer date)
- Commit message

**Any change to any of these inputs produces a completely different hash.** This is why `--amend` always changes the hash even for message-only edits.

---

### 🛡️ Two Core Functions

1. **Integrity Verification**: If file content changes, its blob hash changes. If any blob hash changes, the tree hash changes. If the tree hash changes, the commit hash changes. Tampering at any level is immediately detectable.
2. **Content Addressing**: Objects are stored and retrieved by their hash, not by filename or path. Identical content across commits shares the same blob object — enabling deduplication and instant branching.

---

### 💡 Practical Implications

- Short hashes (`6ab7907`) work because collisions are astronomically unlikely in typical repositories.
- `git show <hash>` retrieves objects directly from `.git/objects/` using the hash as a filesystem path.
- Force-pushing rewritten history breaks collaborators because their local refs point to hashes that no longer exist upstream.

> 💡 **Algorithm Migration:** SHA-1 was chosen in 2005 for speed and adequate collision resistance. Git is migrating toward SHA-256 (experimental since Git 2.29) due to theoretical collision attacks, but understanding SHA-1 semantics transfers directly to SHA-256.

---

## 🗺️ Decision Framework: Which Undo Tool Do I Need?

```text
Is the change already committed?
├── NO → Is it staged?
│        ├── YES → git restore --staged <file>
│        └── NO  → git restore <file>
│
└── YES → Has it been pushed to a remote?
          ├── NO → Is it the MOST RECENT commit?
          │        ├── YES → git commit --amend
          │        └── NO  → git reset --soft/mixed <target>
          │                  (local history rewrite, safe)
          │
          └── YES → git revert <commit-hash>
                    (safe for shared/public branches)
```

---

### 📊 Quick Reference Table

| Situation                                 | Recommended Command                              | Why                                     |
| :---------------------------------------- | :----------------------------------------------- | :-------------------------------------- |
| **Typo in working file, not staged**      | `git restore <file>`                             | Instant discard, zero risk              |
| **Staged too early, not ready to commit** | `git restore --staged <file>`                    | Preserves work, removes from index      |
| **Wrong message on latest local commit**  | `git commit --amend -m "..."`                    | Cleanest fix before pushing             |
| **Forgot file in latest local commit**    | `git add <file> && git commit --amend --no-edit` | Atomic correction                       |
| **Bug found in pushed commit**            | `git revert <hash>`                              | Safe, traceable, collaboration-friendly |
| **Multiple bad commits on shared branch** | `git revert <oldest>..<newest>`                  | Sequential inverse commits              |
| **Want to temporarily set aside WIP**     | `git stash` / `git stash pop`                    | Non-destructive shelving                |

---

## 🛠️ Hands-On Lab: Recovery Scenarios

Execute these sequences to internalize the concepts above.

### 📋 Lab 1: Pre-Commit Recovery

```bash
mkdir lab-ch05 && cd lab-ch05 && git init
echo "correct content" > file.txt && git add file.txt && git commit -m "feat: initial commit"

# Scenario A: Accidental modification (unstaged)
echo "garbage data" >> file.txt
git restore file.txt                     # Verify: content restored
cat file.txt                             # Should show "correct content"

# Scenario B: Premature staging
echo "new feature" >> file.txt
git add file.txt
git restore --staged file.txt            # Unstage without losing change
git status                               # Should show modified, not staged
git restore file.txt                     # Now discard the change entirely
```

---

### 📋 Lab 2: Commit Amendment

```bash
echo "chapter content" > chapter.txt && git add chapter.txt
git commit -m "wip message"              # Intentionally poor message

# Fix message only
git commit --amend -m "docs: add chapter draft with outline"
git log --oneline -1                     # Verify new message and changed hash

# Add forgotten file
touch appendix.txt && git add appendix.txt
git commit --amend --no-edit             # Append to existing commit
git show --stat HEAD                     # Verify both files present
```

---

### 📋 Lab 3: Safe Revert on Simulated Shared Branch

```bash
echo "feature v1" > feature.txt && git add feature.txt && git commit -m "feat: add feature v1"
FEATURE_HASH=$(git rev-parse HEAD)       # Capture hash for later revert

echo "feature v2" > feature.txt && git add feature.txt && git commit -m "feat: upgrade to v2"
echo "buggy code" > bug.txt && git add bug.txt && git commit -m "fix: resolve edge case"

# Discover v1 was actually correct; revert the upgrade
git revert $FEATURE_HASH                 # Accept default message or customize
git log --oneline                        # Original commit preserved; revert commit added
git show HEAD                            # Verify inverse diff
```

---

### 📋 Lab 4: Hash Observation

```bash
echo "test" > hash_demo.txt && git add hash_demo.txt
git commit -m "demo: hash observation"
HASH_BEFORE=$(git rev-parse HEAD)

git commit --amend -m "demo: hash observation (amended)"
HASH_AFTER=$(git rev-parse HEAD)

echo "Before: $HASH_BEFORE"
echo "After:  $HASH_AFTER"
# Hashes differ despite identical content — proves amend creates new object
```

---

### 🎯 Verification Checklist

- [ ] Restored unstaged changes and confirmed file content matches last commit.
- [ ] Unstaged a file without losing modifications, then discarded separately.
- [ ] Amended commit message and verified hash changed.
- [ ] Added forgotten file via amend and confirmed both files in `git show --stat`.
- [ ] Reverted a non-HEAD commit and verified original commit remains in history.
- [ ] Observed hash change after amend with identical content.
- [ ] Articulated why `revert` is preferred over `reset` on shared branches.

---

## 💡 Key Takeaways

> **Fix early, fix cheaply.** Pre-commit recovery (`restore`) is lossless and instantaneous. Always validate changes before staging and committing.

> **Amend is local-only.** The hash change caused by `--amend` makes it incompatible with any commit that exists on a remote. Use it freely during local development; never after push.

> **Revert preserves truth.** On shared branches, mistakes should be visible and reversible, not erased. `git revert` maintains complete audit trails while correcting errors.

> **Hashes guarantee integrity.** SHA-1 binds content, identity, time, and lineage into a single fingerprint. Any tampering or amendment produces a new identity — making unauthorized modifications cryptographically evident.

> **Choose by context, not preference.** The decision between `restore`/`amend`/`reset`/`revert` depends entirely on the change's lifecycle stage and visibility to others. Memorize the decision framework, not individual commands.
