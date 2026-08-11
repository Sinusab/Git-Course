# Chapter 01: Intro, Diff & Patch

## 🎯 Key Concepts

- **Version Control**: Why it matters (traceability, collaboration, safety net)
- **Diff**: Comparing two versions of a file line-by-line
- **Patch**: A portable diff that can be applied to recreate changes

## 🔧 Commands Cheat Sheet

| Command                  | Purpose                   | Example                                                |
| ------------------------ | ------------------------- | ------------------------------------------------------ |
| `diff -u file1 file2`    | Unified diff format       | `diff -u old.txt new.txt`                              |
| `patch < change.patch`   | Apply a patch to original | `patch -p1 < fix.patch`                                |
| `git diff`               | Show unstaged changes     | —                                                      |
| `kdiff3 file1 file2`     | Visual side-by-side diff  | `kdiff3 old.txt new.txt`                               |
| `kdiff3 -m a b c -o out` | 3-way merge with output   | `kdiff3 -m base.txt mine.txt theirs.txt -o merged.txt` |

## 🖥️ Visual Tool: KDiff3

KDiff3 is a free, cross-platform GUI for comparing and merging files/directories.  
It shines when you need to **see** differences instead of reading raw `+/-` lines.

### Features at a glance

- Side-by-side or 3-pane comparison
- Line-level and character-level highlighting
- Built-in merge editor with conflict resolution
- Directory comparison (recursive)
- Integrates with Git as `mergetool` / `difftool`

### Example: 3-way merge view

![KDiff3 3-way merge interface](./assets/kdiff3-merge-view.png)

> **Pane A** = Base (common ancestor)  
> **Pane B** = Local (your changes)  
> **Pane C** = Remote (incoming changes)  
> **Bottom** = Merged output — edit directly here to resolve conflicts

### Quick start

```bash
# Install (Debian/Ubuntu)
sudo apt install kdiff3

# Compare two files visually
kdiff3 original.txt modified.txt

# Use as Git mergetool
git config --global merge.tool kdiff3
git mergetool
```

## 💡 Key Takeaways

> **Diff is the language of code review.**  
> Understanding it manually makes Git diffs intuitive later.

> **Patches predate GitHub PRs.**  
> They were the original open-source contribution mechanism and remain useful for email-based workflows.

> **Visual tools bridge the learning gap.**  
> KDiff3 turns abstract `+/-` symbols into something visual — great for learning, but in real teams VS Code's built-in diff or GitHub's web UI are more common.

## 🛠️ Practice: WSL Path Converter

A small script to convert Windows paths to WSL-compatible paths.  
Demonstrates iterative improvement — a core concept in version control.

### Version 1: Basic Windows → WSL conversion

[`exercises/wsl-path-converter-base.py`](./exercises/wsl-path-converter-base.py)

- Handles `C:\Users\...` → `/mnt/c/Users/...`
- ❌ Missing: UNC paths (`//wsl.localhost/...`)

### Version 2: Added UNC path support

[`exercises/wsl-path-converter-fixed.py`](./exercises/wsl-path-converter-fixed.py)

- ✅ Handles both drive letters AND UNC paths
- ✅ Uses regex groups for clean extraction
- 💡 Key learning: Always consider edge cases before declaring "done"

### What changed between v1 (base) and v2 (fixed)?

Generated with:

```bash
diff -u exercises/wsl-path-converter-base.py exercises/wsl-path-converter-fixed.py > exercises/results/wsl-path-diff.diff
```

Full diff saved in [`exercises/results/wsl-path-diff.diff`](./exercises/results/wsl-path-diff.diff)

```diff
--- exercises/wsl-path-converter-base.py        2026-08-11 19:42:13.644187242 +0330
+++ exercises/wsl-path-converter-fixed.py       2026-08-11 19:42:27.319481882 +0330
@@ -3,8 +3,14 @@

 dir_add = input("Enter directory path: ").strip("'\"")

-# Convert Windows path to WSL path
-if re.match(r"^[a-zA-Z]:[/\\]", dir_add):
+# Convert //wsl.localhost/<distro>/... → /...
+unc_match = re.match(r"^//wsl\.localhost/[^/]+(/.*)", dir_add, re.IGNORECASE)
+if unc_match:
+    dir_add = unc_match.group(1)
+    print(f"Converted UNC to: {dir_add}")
+
+# Convert Windows drive paths C:\... → /mnt/c/...
+elif re.match(r"^[a-zA-Z]:[/\\]", dir_add):
     drive = dir_add[0].lower()
     rest = dir_add[2:].replace("\\", "/")
     dir_add = f"/mnt/{drive}{rest}"
```

**💡 Notice how the original `if` became `elif` — this is exactly the kind of detail Git tracks in every commit.**

Now that we've seen the diff, let's understand how it becomes a portable, applicable unit of change.

### 📄 `.diff` vs `.patch`: What's the Difference?

**Short answer:** Technically identical format. The difference is **convention, intent, and one Git-specific edge case**.

| Aspect            | `.diff`                     | `.patch`                       |
| ----------------- | --------------------------- | ------------------------------ |
| Content format    | Unified diff                | Unified diff                   |
| Typical use       | Viewing / reviewing changes | Applying changes to files      |
| Common tool       | `diff -u`, GitHub UI, IDEs  | `patch`, `git apply`, `git am` |
| Naming convention | Describes _what changed_    | Describes _a change to apply_  |
| Example name      | `wsl-path-diff.diff`        | `wsl-path-converter.patch`     |

#### ⚠️ One Git-Specific Nuance

While the core content is identical, there is one technical edge case worth keeping in mind:

- **`git diff`** outputs usually **lack commit metadata** (author, date, commit message). This aligns perfectly with the `.diff` convention — pure differences for review.
- **`git format-patch`** outputs automatically **include email-style headers** (`From:`, `Date:`, `Subject:`) so that `git am` can reconstruct the exact commit history. This aligns perfectly with the `.patch` convention — a self-contained, applicable unit of change.

> 💡 **Same format, different purpose.**  
> A `.diff` says "look at these differences."  
> A `.patch` says "apply these differences to reconstruct a new version."  
> Git doesn't care about the extension — it reads the content. But humans (and `git am`) do.

In practice:

- Save as `.diff` when documenting or reviewing (like our [wsl-path-diff.diff](./results/wsl-path-diff.diff))
- Save as `.patch` when intending to apply it later (like our [wsl-path-converter.patch](./exercises/results/wsl-path-converter.patch))

### 🩹 Applying the Patch

Now let's use the same diff as a **patch** to reconstruct `fixed.py` from `base.py` — without ever touching the fixed file directly.

#### Step 1: Generate the patch

```bash
diff -u exercises/wsl-path-converter-base.py exercises/wsl-path-converter-fixed.py > exercises/results/wsl-path-converter.patch
```

#### Step 2: Apply it to a fresh copy

```bash
cp exercises/wsl-path-converter-base.py exercises/test-reconstructed.py
patch exercises/test-reconstructed.py < exercises/results/wsl-path-converter.patch
# Output: patching file exercises/test-reconstructed.py
```

#### Step 3: Verify the result

```bash
diff exercises/test-reconstructed.py exercises/wsl-path-converter-fixed.py
# No output = files are identical ✅

rm exercises/test-reconstructed.py
```

> 💡 **This is the core idea behind Git:** every commit stores a patch, not a full copy.  
> When you `git checkout`, Git applies patches sequentially to reconstruct any version.  
> Manual `patch` = what Git does internally thousands of times per second.
