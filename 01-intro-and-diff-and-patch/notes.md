# Chapter 01: Intro, Diff & Patch

## 🎯 Key Concepts
- **Version Control**: Why it matters (traceability, collaboration, safety net)
- **Diff**: Comparing two versions of a file line-by-line
- **Patch**: A portable diff that can be applied to recreate changes

## 🔧 Commands Cheat Sheet
| Command | Purpose | Example |
|---------|---------|---------|
| `diff -u file1 file2` | Unified diff format | `diff -u old.txt new.txt` |
| `patch < change.patch` | Apply a patch to original | `patch -p1 < fix.patch` |
| `git diff` | Show unstaged changes | — |
| `kdiff3 file1 file2` | Visual side-by-side diff | `kdiff3 old.txt new.txt` |
| `kdiff3 -m a b c -o out` | 3-way merge with output | `kdiff3 -m base.txt mine.txt theirs.txt -o merged.txt` |

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

