# ✅ Chapter 04 Quiz: Advanced Git Interactions

Test your understanding of staging shortcuts, change inspection, file lifecycle management, and ignore mechanisms.

---

## Q1: Staging Bypass Limitation

You have three files in your repository:

- `config.yaml` (tracked, modified locally)
- `debug.log` (untracked, newly created)
- `schema.sql` (tracked, deleted locally)

You run `git commit -a -m "cleanup"`. Which files are included in the commit?

- A) All three files
- B) `config.yaml` and `schema.sql` only
- C) `config.yaml` only
- D) `debug.log` only

<details>
<summary>💡 Click to reveal answer</summary>

**B** — `git commit -a` auto-stages modifications and deletions to **tracked** files only. `config.yaml` (modified) and `schema.sql` (deleted) qualify. `debug.log` is untracked and completely ignored by `-a`. It requires explicit `git add debug.log` before it can be committed.

</details>

---

## Q2: Diff Layer Identification

After running `git add report.md`, you execute `git diff` and see no output. What does this indicate?

- A) No changes exist in the repository
- B) Changes were committed automatically
- C) Working directory matches the index; changes are now staged
- D) The file was reverted to its previous state

<details>
<summary>💡 Click to reveal answer</summary>

**C** — `git diff` compares Working Directory against Index. After `git add`, these two layers are identical, so diff is empty. The changes still exist — they moved to the staging area. Run `git diff --staged` to see them. Empty `git diff` never means "no changes"; it means "no unstaged changes".

</details>

---

## Q3: Interactive Staging Purpose

What is the primary professional benefit of `git add -p` over `git add <file>`?

- A) It runs faster on large repositories
- B) It enables splitting one file's changes across multiple atomic commits
- C) It automatically formats code before staging
- D) It bypasses pre-commit hooks for speed

<details>
<summary>💡 Click to reveal answer</summary>

**B** — Interactive staging presents changes hunk-by-hunk, letting you choose which portions belong in the current commit. This enables atomic commits: a bug fix and a feature addition in the same file become two separate, revertible, reviewable commits instead of one tangled snapshot. Speed, formatting, and hook bypass are unrelated to `-p`.

</details>

---

## Q4: File Deletion Semantics

What is the key difference between `rm file.txt` followed by `git add file.txt` versus `git rm file.txt`?

- A) `git rm` permanently erases the file from all history
- B) `rm` + `add` requires two commands; `git rm` stages deletion atomically in one step
- C) `git rm` only works on untracked files
- D) There is no difference; both produce identical staging state

<details>
<summary>💡 Click to reveal answer</summary>

**B** — Both approaches result in the same staged deletion and preserve the file in historical commits. The difference is operational: `rm` removes from filesystem only (Git detects it as unstaged deletion), requiring a second `git add` to stage. `git rm` combines filesystem removal and staging into one atomic command. Neither erases history.

</details>

---

## Q5: `.gitignore` Scope

You add `*.tmp` to `.gitignore`, but `git status` still shows `cache.tmp` as modified. Why?

- A) `.gitignore` syntax is invalid
- B) The file was already tracked before the ignore rule was added
- C) `.gitignore` only applies to directories, not files
- D) Wildcards require escaping in Git

<details>
<summary>💡 Click to reveal answer</summary>

**B** — `.gitignore` only affects **untracked** files. If `cache.tmp` was committed before the ignore rule existed, Git continues tracking it regardless of `.gitignore` content. To stop tracking while preserving the local file: `git rm --cached cache.tmp`, then commit. The ignore rule will prevent future re-tracking.

</details>

---

## Q6: HEAD Semantics

What does `HEAD~2` refer to in Git?

- A) The second branch in the repository
- B) The commit two generations before the current HEAD
- C) The second file in the staging area
- D) A tag named "2"

<details>
<summary>💡 Click to reveal answer</summary>

**B** — The `~n` suffix walks backward through commit ancestry. `HEAD~1` is the parent commit, `HEAD~2` is the grandparent, and so on. This notation enables precise historical navigation without memorizing hashes. It is essential for `git diff`, `git show`, and recovery operations.

</details>

---

## Q7: Documentation Access

Which command provides offline, version-matched documentation for `git diff`?

- A) `git diff --docs`
- B) `git help diff`
- C) `git diff --manual`
- D) `git docs diff`

<details>
<summary>💡 Click to reveal answer</summary>

**B** — `git help <command>` opens the built-in manual page in your pager. It works offline, loads instantly, and always matches your installed Git version. Alternatives `git <command> --help` and `man git-<command>` produce identical output. The other options are not valid Git flags.

</details>
