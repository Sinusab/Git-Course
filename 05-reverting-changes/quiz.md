# ✅ Chapter 05 Quiz: Undoing Changes in Git

Test your understanding of pre-commit recovery, commit amendment, safe rollback, and SHA-1 integrity.

---

## Q1: Safe Undo on Shared Branches

You discover a bug in the latest commit on `main`, which has already been pushed and pulled by three teammates. Which command should you use?

- A) `git commit --amend`
- B) `git reset --hard HEAD~1`
- C) `git revert HEAD`
- D) `git restore <file>`

<details>
<summary>💡 Click to reveal answer</summary>

**C** — `git revert` creates a new inverse commit without rewriting history. Since the commit is already on a shared branch, `amend` and `reset --hard` would require force-push and break teammates' local copies. `git restore` only works for uncommitted changes. Revert is the only safe option for public/shared history.

</details>

---

## Q2: Amend Behavior

After running `git commit --amend -m "fixed message"`, what happens to the original commit?

- A) It is edited in place with the new message
- B) It is deleted permanently and unrecoverably
- C) A new commit is created with a new hash; the old commit becomes orphaned
- D) Both old and new commits coexist on the branch

<details>
<summary>💡 Click to reveal answer</summary>

**C** — Amend never modifies existing objects in place. It creates a brand-new commit with updated metadata/content and points the branch tip to it. The old commit loses all direct references and is eventually garbage-collected after ~30 days. The hash always changes because the commit object's content (including the message) determines its SHA-1.

</details>

---

## Q3: Pre-Commit Staging Mistake

You ran `git add large-dataset.csv` by accident. The file is 2GB and should never be committed. You have NOT committed yet. What is the correct recovery?

- A) `git restore large-dataset.csv`
- B) `git restore --staged large-dataset.csv`
- C) `git commit --amend`
- D) `git revert HEAD`

<details>
<summary>💡 Click to reveal answer</summary>

**B** — `git restore --staged` removes the file from the index without deleting it from disk or losing any local changes. Option A would discard working directory modifications. Options C and D operate on existing commits, but no commit has been made yet.

</details>

---

## Q4: SHA-1 Determinism

Two developers independently create identical commits (same tree content, same message, same author, same parent, same timestamp). Will their commit hashes match?

- A) No, hashes are random UUIDs
- B) Yes, because SHA-1 is deterministic for identical inputs
- C) Only if they are on the same physical machine
- D) Only if they use the identical Git binary version

<details>
<summary>💡 Click to reveal answer</summary>

**B** — SHA-1 is a deterministic cryptographic hash function: identical inputs always produce identical outputs. Since commit hashes are derived from tree hash + parent hash + author/committer identity + timestamps + message, identical inputs yield identical hashes across machines.

</details>

---

## Q5: Revert Scope

You need to undo a commit that is 5 commits behind HEAD on a shared branch. What is the correct approach?

- A) Run `git revert HEAD` five times
- B) Run `git reset --hard HEAD~5`
- C) Run `git revert <specific-commit-hash>`
- D) Run `git commit --amend` on the target commit

<details>
<summary>💡 Click to reveal answer</summary>

**C** — `git revert` accepts any commit hash, not just HEAD. Specify the exact commit to invert. Option A would revert the wrong commits. Option B rewrites shared history (destructive). Option D cannot target non-HEAD commits and rewrites history. Reverting by explicit hash is precise, safe, and preserves all intermediate work.

</details>

---

## Q6: Amend Safety Check

Which scenario makes `git commit --amend` unsafe?

- A) The commit is the latest on a local feature branch
- B) The commit has been pushed to a remote repository
- C) The commit message contains a typo
- D) A file was forgotten in the commit

<details>
<summary>💡 Click to reveal answer</summary>

**B** — Once pushed, other developers may have based work on that commit hash. Amending replaces the hash, causing divergence that requires a force-push to resolve. Scenarios A, C, and D are all valid, safe uses of amend. The safety boundary is exclusively about remote visibility.

</details>

---

## Q7: Restore vs Checkout

What is the primary architectural advantage of `git restore <file>` over `git checkout -- <file>`?

- A) It executes faster on large codebases
- B) It separates "undo file changes" from "switch branches" into distinct commands
- C) It automatically tracks previously untracked files
- D) It automatically stages the restored file into the index

<details>
<summary>💡 Click to reveal answer</summary>

**B** — Before Git 2.23, `git checkout` served dual purposes: switching branches AND restoring files. This ambiguity caused accidental branch switches. `git restore` and `git switch` were introduced to give each operation a dedicated, unambiguous interface.

</details>
