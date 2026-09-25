# Complete Git & GitHub Master Cheat Sheet

A comprehensive, battle-tested reference guide based on [tiimgreen/github-cheat-sheet](https://github.com/tiimgreen/github-cheat-sheet) combined with modern Git & GitHub best practices.

---

## 1. Configured Git Aliases (Active on your system)

The following shortcuts have been globally configured in your `.gitconfig`:

| Command | Full Git Action | Description |
| :--- | :--- | :--- |
| `git lg` | `git log --graph --pretty=format:'...'` | Beautiful tree graph showing commits, branches, author, and relative time |
| `git st` | `git status -sb` | Concise status view showing current branch and tracking status |
| `git sw <branch>` | `git switch <branch>` | Switch branches quickly |
| `git prev` | `git checkout -` | Jump back to the previously active branch |
| `git last` | `git log -1 HEAD --stat` | View full details of the latest commit including changed files |
| `git unstage <file>` | `git restore --staged <file>` | Remove file from staging area without losing changes |
| `git amend` | `git commit --amend --no-edit` | Add staged changes directly into the most recent commit |
| `git empty -m "msg"` | `git commit --allow-empty -m "msg"` | Create a zero-change commit (useful for triggering CI/CD) |
| `git undo` | `git reset --soft HEAD~1` | Undo the last commit while preserving all changes staged |
| `git br` | `git branch` | Branch list |
| `git co` | `git checkout` | Checkout alias |
| `git ci` | `git commit` | Commit alias |

---

## 2. GitHub Web UI & URL Magic

### URL Query Modifiers
* **Hide Whitespace in Diffs:** Append `?w=1` to any PR or commit diff URL:
  ```text
  https://github.com/owner/repo/pull/42/files?w=1
  ```
* **Adjust Tab Width:** Change indentation tab-stops to 2 or 4 spaces:
  ```text
  https://github.com/owner/repo/blob/main/index.js?ts=2
  ```
* **Get Raw Diff or Patch:** Append `.diff` or `.patch` to any commit or PR URL to view plain patch text or pipe into unix commands:
  ```text
  https://github.com/owner/repo/pull/42.diff
  https://github.com/owner/repo/commit/abc1234.patch
  ```
* **Author Filter:** Filter commit history to a single author:
  ```text
  https://github.com/owner/repo/commits/main?author=username
  ```

### Browser Keyboard Shortcuts (Press `?` anywhere on GitHub)
| Key | Action |
| :--- | :--- |
| <kbd>t</kbd> | Activate fuzzy file finder in any repository |
| <kbd>s</kbd> or <kbd>/</kbd> | Focus search bar |
| <kbd>y</kbd> | Transform URL into a canonical permalink (pins specific commit SHA) |
| <kbd>b</kbd> | View Git blame for the current file |
| <kbd>l</kbd> | Jump to line number in file view |
| <kbd>w</kbd> | Open branch/tag switcher popup |
| <kbd>r</kbd> | Quote selected text in a PR or issue reply |

### Issues & Pull Requests
* **Auto-Close Issues via Commits:** Include keywords followed by issue ID in commit messages:
  `Fixes #12`, `Closes #12`, `Resolves #12`.
* **Markdown Task Lists:**
  ```markdown
  - [x] Finished feature
  - [ ] Pending unit test
  ```
* **Cross-Repository References:**
  Reference issues/PRs in other repos using `owner/repo#number` (e.g. `torvalds/linux#1024`).

---

## 3. Advanced Git CLI Operations

### Branching & Navigation
* **Switch to previous branch:**
  ```bash
  git switch -
  # or
  git checkout -
  ```
* **List merged branches (safe to delete):**
  ```bash
  git branch --merged
  ```
* **Delete all local branches already merged into `main`:**
  ```bash
  git branch --merged main | grep -v '^\*' | grep -v 'main' | xargs -n 1 git branch -d
  ```

### Code Archeology & Investigation (Pickaxe & Grep)
* **Search commit history for exact code added/removed (`-S`):**
  ```bash
  git log -S "function calculateTax" --source --all
  ```
* **Search commit history using Regex (`-G`):**
  ```bash
  git log -G "api_key\s*=" -p
  ```
* **Grep repository without git indexing lag:**
  ```bash
  git grep -n "searchTerm"
  ```
* **View commit history for a specific function:**
  ```bash
  git log -L :calculateTax:src/billing.js
  ```

### Fixing Commits & Clean History
* **Autosquash workflow:**
  ```bash
  # 1. Stage fixes for a prior commit
  git add .
  # 2. Mark commit as a fixup targeting an older commit SHA
  git commit --fixup <older-commit-sha>
  # 3. Automatically squash fixups into their target commits
  git rebase -i --autosquash <base-branch>
  ```
* **Interactive staging (Hunk selection):**
  ```bash
  git add -p
  ```
* **Interactive stashing (Stash part of your changes):**
  ```bash
  git stash -p
  ```

### Disaster Recovery
* **Recover deleted branches or lost commits (`reflog`):**
  ```bash
  git reflog
  # Find the HEAD@{n} point before mistake, then:
  git checkout -b recovered-branch HEAD@{1}
  ```
* **Undo a commit cleanly with a new inverse commit:**
  ```bash
  git revert <commit-sha>
  ```

---

## 4. PR Checkout & Collaboration Tricks

* **Check out a PR branch locally directly from GitHub:**
  ```bash
  # Fetch the PR into a local branch called pr-42
  git fetch origin pull/42/head:pr-42
  git switch pr-42
  ```
* **Compare two commits / branches with statistics:**
  ```bash
  git diff --stat main..feature-branch
  ```
* **Run built-in web viewer:**
  ```bash
  git instaweb
  ```

---
*Created and installed in workspace: `e:/anti`.*
