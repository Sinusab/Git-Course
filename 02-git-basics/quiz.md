---

## ✅ Concept Check: Chapter 02 Quiz

Test your understanding of the fundamentals before moving to hands-on commands in Chapter 03.

### Q1: Version Control vs Source Control

A teammate says "we need better source control for our design assets (Figma files, PDFs)". Is the term accurate?

- A) Yes, source control covers all file types
- B) No, "version control" is more accurate since "source" implies code
- C) Both terms are wrong — only Git works with binaries

<details>
<summary>💡 Answer</summary>

**B** — Historically "Source Control" meant source code specifically (Microsoft VSS/TFS era). For non-code assets, "Version Control" is the precise term. In practice though, most teams use them interchangeably.

</details>

### Q2: Git vs GitHub

Your internet is down. Which of these can you still do?

- A) `git commit -m "fix bug"`
- B) `git push origin main`
- C) `gh pr create`
- D) `git log --oneline`

<details>
<summary>💡 Answer</summary>

**A and D** — `git commit` and `git log` are local Git operations (engine). `git push` and `gh pr create` require GitHub (platform) and internet. This is the core distinction: Git works offline, GitHub doesn't.

</details>

### Q3: Three-State Model

You edited `app.py` but haven't run any Git command yet. What state is the file in?

- A) Committed
- B) Staged
- C) Modified
- D) Untracked

<details>
<summary>💡 Answer</summary>

**C (Modified)** — if the file was already tracked. **D (Untracked)** — if it's a brand new file Git has never seen. The Working Directory holds both modified and untracked files until you `git add` them.

</details>

### Q4: Automation Mindset

Why does Git provide `--porcelain` output format?

- A) To make output prettier for humans
- B) To guarantee stable, parseable output for scripts across Git versions
- C) To reduce output size for slow terminals
- D) To hide sensitive information from logs

<details>
<summary>💡 Answer</summary>

**B** — Porcelain output is a contract: its format won't change between Git versions. Default (human) output may change for readability. Automation relies on porcelain; humans use default.

</details>

### Q5: Distributed Architecture

In SVN, `svn log` fails without internet. In Git, `git log` works offline. Why?

- A) Git caches logs in RAM
- B) Every Git clone contains the full history locally in `.git/objects/`
- C) Git uses a faster network protocol
- D) SVN is deprecated and no longer maintained

<details>
<summary>💡 Answer</summary>

**B** — This is the fundamental architectural difference. Centralized VCS (SVN) keeps history on the server. Distributed VCS (Git) gives every clone a complete copy. No network = no problem for local operations.

</details>
