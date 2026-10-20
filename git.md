# Git: From Fundamentals to Advanced Workflows

A comprehensive, example-driven reference for learning Git, understanding its internals, and managing real software and data projects.

**Conventions:** Examples use a Unix-like terminal, Git 2.23+ for `switch`/`restore`, and `main` as the default branch. Substitute your own repository URL, email address, and branch names. Commands in an example assume the preceding commands have been run unless stated otherwise.

---

# Part I — Fundamentals

## 1. The Git Mental Model

### 1.1 What is Git?

Git is a **distributed version-control system**. Every full clone has its own local history; you can inspect, branch, and commit without contacting a server. GitHub, GitLab, and Bitbucket are hosting/collaboration services, not Git itself.

Git records **snapshots** of tracked files in commits. Internally it reuses unchanged content and compresses stored objects; it is not simply a folder of complete copies.

Core concepts:

| Concept | Meaning |
|---|---|
| Repository | Project history, objects, and references, usually under `.git/` |
| Working tree | The files you edit on disk |
| Index / staging area | The proposed file snapshot for the next commit |
| Commit | A snapshot plus metadata and parent commit ID(s) |
| Branch | A movable reference to a commit |
| `HEAD` | Usually a symbolic reference to the current branch; can directly identify a commit |
| Remote | A named URL/location of another Git repository |
| Remote-tracking ref | Local record such as `origin/main` of a remote branch's last fetched state |
| Tag | A named reference to a particular object, usually a release commit |

### 1.2 The three-tree model

```text
Working tree              Index (staging)               HEAD (last commit)
Files on disk    --add-->  Next proposed snapshot --commit--> Recorded history
       ^                        ^                                    |
       |                        |                                    |
   git restore           git restore --staged                  branch ref
```

What the comparison commands mean:

| Command | Comparison |
|---|---|
| `git diff` | Working tree vs index: **unstaged** changes |
| `git diff --staged` | Index vs `HEAD`: **staged** changes |
| `git diff HEAD` | Working tree vs `HEAD`: all tracked modifications (staged + unstaged) |
| `git status` | Summarizes staged, unstaged, and untracked states |

### 1.3 File lifecycle

```text
Untracked --git add--> Staged --git commit--> Tracked in HEAD
     |                       ^                      |
     |                       |                      v
     +---- ignored?          +-- git add -- Modified in working tree
```

`git add` snapshots the **current contents** into the index. If you edit the file again after staging, the newer changes remain unstaged until you add the file again.

### 1.4 Commit graph

```text
A---B---C  main
     \
      D---E  feature
```

A commit points to its parent(s); Git history is a **directed acyclic graph (DAG)**. Branch names are pointers, not containers of commits. A merge commit typically has two parents.

## 2. Installation and Configuration

### 2.1 Identify your setup

```bash
git --version
git help -a
git help status
git status --short
```

`git status` requires being inside a repository; the others do not. On Windows, Git Bash provides a Unix-like terminal.

### 2.2 Configure identity and defaults

```bash
git config --global user.name "Ada Developer"
git config --global user.email "ada@example.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
git config --global fetch.prune true
```

Scope hierarchy, from lower to higher precedence: system → global → local repository → worktree (when enabled) → command-line overrides. Environment variables can also affect behavior.

```bash
git config --list --show-origin
git config --show-origin --get user.email
git config --local user.email "ada@work.example"
git config --global --unset user.name
```

Configure the name again before committing if you have unset it.

Useful configuration:

| Setting | Typical value | Why |
|---|---|---|
| `init.defaultBranch` | `main` | Initial branch name |
| `pull.ff` | `only` | Refuse pulls requiring a non-fast-forward integration |
| `fetch.prune` | `true` | Prune deleted remote-tracking refs during fetch |
| `rebase.autoStash` | `true` | Temporarily stash local work during supported rebases; may still conflict |
| `rerere.enabled` | `true` | Remember successful conflict resolutions |
| `commit.gpgsign` | `true` | Sign commits once signing is configured |

```bash
git config --global pull.ff only
git config --global rerere.enabled true
```

**Identity is not authentication.** `user.name` and `user.email` are stored in commits; remote authentication normally uses SSH keys or HTTPS credentials/tokens managed by a credential helper.

## 3. Creating and Cloning Repositories

### 3.1 Start a local project

```bash
mkdir experiment-tracker
cd experiment-tracker
git init
git branch --show-current
printf '# Experiment Tracker\n' > README.md
git add README.md
git commit -m "docs: initialize project"
```

### 3.2 Clone an existing project

```bash
git clone https://github.com/example/repository.git
git clone https://github.com/example/repository.git my-folder
git clone --branch main https://github.com/example/repository.git
```

A standard clone usually configures remote `origin` and creates a local branch tracking the selected remote branch. `origin` is only the conventional remote name.

### 3.3 Repository structure

```text
project/
├── .git/
├── .gitignore
├── README.md
├── pyproject.toml
├── src/
└── tests/
```

`.git/` holds the repository's object database, index, references, and configuration. Do not hand-edit it unless you know exactly why.

## 4. The Daily Editing and Commit Cycle

### 4.1 Inspect changes

```bash
git status
git status --short
git diff
git diff --stat
git diff -- README.md
git diff --check
```

Short-status example:

```text
 M README.md
M  pyproject.toml
?? notebooks/
```

The first column describes index status; the second describes working-tree status. `??` means untracked.

### 4.2 Stage deliberately

```bash
git add README.md
git add src/ tests/
git add -u
git add -A
git add -p
git diff --staged
```

| Command | Meaning |
|---|---|
| `git add file` | Stage that path's current contents |
| `git add -u` | Stage tracked-file modifications/deletions, not untracked files |
| `git add -A` | Stage tracked changes and new untracked files throughout the repo |
| `git add -p` | Interactively stage selected hunks |
| `git restore --staged file` | Remove a file's staged changes; retain the working-tree contents |

`git add -p` is valuable when you made multiple independent edits in one file: stage and commit one logical change at a time.

### 4.3 Commit

```bash
git commit -m "feat: add dataset loader"
git commit -m "fix: handle missing labels" -m "Treat absent label columns as optional for unsupervised datasets."
git commit --amend
```

`--amend` creates a new commit and replaces the current branch tip. It can change content, message, or both. Avoid amending a commit other people have based work on unless coordination is explicit.

Commit-message guidance:

```text
feat: support stratified train-test splits
fix: prevent division by zero in metric calculation
refactor: isolate input data normalization
test: cover empty prediction arrays
docs: clarify installation instructions
```

Conventional Commit prefixes are a team convention, not a Git requirement. Prefer a concise imperative subject describing the change.

### 4.4 Rename or remove tracked files

```bash
git mv old_name.py new_name.py
git rm obsolete.py
git rm --cached local_config.json
```

`git mv` is a convenient move-plus-stage operation; Git recognizes renames by comparing content when it displays diffs. `git rm --cached` stops tracking a file **without deleting the working copy**. Add an appropriate ignore rule to keep it untracked.

## 5. Reading History and Comparing Versions

### 5.1 Logs

```bash
git log
git log --oneline
git log --oneline --graph --decorate --all
git log -5
git log --since="2 weeks ago" --author="Ada"
git log --grep="dataset"
git log -- path/to/file.py
git log -p -- src/
```

### 5.2 Examine commits

```bash
git show HEAD
git show HEAD:README.md
git show --stat HEAD~2
git show --name-status HEAD
```

`HEAD:path` reads a file **from a commit**, rather than your working-tree file.

### 5.3 Revision notation

| Syntax | Meaning |
|---|---|
| `HEAD` | Current commit |
| `HEAD~1` | First parent of `HEAD` |
| `HEAD~3` | First-parent ancestor three steps back |
| `HEAD^1` | First parent; same as `HEAD^` |
| `HEAD^2` | Second parent, meaningful for merge commits |
| `abc1234` | Abbreviated commit object ID, if unambiguous |
| `main~2` | Two first-parent steps behind `main` |
| `A..B` | Commits reachable from `B`, excluding those reachable from `A` |
| `A...B` in `git log` | Symmetric difference of commit sets |

```bash
git log main..feature
git log --left-right main...feature
git diff main feature
git diff main...feature
```

**Important distinction:** `git diff A B` compares the two endpoint trees, whereas `git diff A...B` compares the merge-base tree of `A` and `B` with `B` (under the usual single merge-base case). The `...` notation has different semantics in `git log` and `git diff`.

### 5.4 Find the merge base

```bash
git merge-base main feature
git branch --contains HEAD~2
git branch -r --contains HEAD~2
```

`merge-base` finds a best common ancestor, useful for code-review-style diffs and analyzing divergent histories.

---

# Part II — Branching and Collaboration

## 6. Branches, HEAD, and Detached HEAD

### 6.1 Create, switch, list, and delete

```bash
git branch
git branch -a
git branch -vv
git switch -c feat/metrics
git switch main
git branch feat/experiment
git branch -d feat/experiment
```

`-d` protects against deleting a branch that Git considers not fully merged; `-D` forces deletion and can leave commits reachable only through reflogs. Treat it as an intentional recovery-risk action.

### 6.2 Rename a branch

```bash
git branch -m feat/metrics feat/evaluation-metrics
```

If already published, updating the remote involves publishing the new branch, adjusting upstream configuration, and deleting the old remote name when appropriate.

### 6.3 `HEAD` versus branch reference

```text
HEAD -> refs/heads/main -> C
A --- B --- C
```

Ordinarily `HEAD` symbolically points to a branch; that branch points to the tip commit. Switching branches changes `HEAD` and updates index/working tree as allowed by your current edits.

### 6.4 Detached HEAD

```bash
git switch --detach HEAD~2
git log -1 --oneline
git switch -c research/older-state
git switch main
```

Detached `HEAD` means you are examining a specific commit rather than being on a local branch. You **can** commit in detached mode; create a branch to retain those commits before moving away.

## 7. Remotes, Fetch, Pull, and Push

### 7.1 Remotes are named locations

```bash
git remote -v
git remote add origin git@github.com:example/project.git
git remote get-url origin
git remote set-url origin git@github.com:example/new-project.git
git remote show origin
```

Choose HTTPS or SSH based on your credentials and organizational policy.

### 7.2 Fetch does not merge

```bash
git fetch origin
git fetch --all --prune
git log --oneline main..origin/main
git diff main..origin/main
```

`fetch` downloads objects and updates remote-tracking refs (for example `origin/main`) according to configured refspecs. It does **not** move your checked-out local `main` branch or automatically change tracked working-tree files.

### 7.3 Pull = fetch + integration

```bash
git switch main
git pull --ff-only origin main
```

`--ff-only` updates only when your branch can advance without creating a merge commit or replaying local commits. When local and remote branches diverge, choose consciously:

```bash
git pull --rebase origin main
git pull --no-rebase origin main
```

The first replays local commits on top of fetched updates; the second allows merge-based integration. Teams should establish a consistent policy.

### 7.4 Publish and track a branch

```bash
git push -u origin feat/metrics
git push
git branch -vv
git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
```

`-u` sets an upstream tracking relationship, enabling argument-free `git push` and `git pull` in common configurations.

### 7.5 Delete remote branches and understand pruning

```bash
git push origin --delete feat/old-branch
git fetch --prune origin
```

Deleting `origin/feat/old-branch` locally with pruning does not delete a server branch; it clears stale local remote-tracking references after fetching.

### 7.6 Force pushing safely

```bash
git push --force-with-lease origin feat/metrics
```

Use only when deliberately replacing published history and collaborators understand. `--force-with-lease` checks that the remote ref still matches the value you expect, reducing accidental overwrites relative to plain `--force`. It is not an absolute concurrency guarantee; understand what your local remote-tracking ref represents.

## 8. Merging and Resolving Conflicts

### 8.1 Fast-forward merge

```text
Before: A---B (main)---C---D (feature)
After:  A---B---C---D (main, feature)
```

```bash
git switch main
git merge --ff-only feature
```

If `main` is an ancestor of `feature`, Git can move the branch pointer forward without creating a merge commit.

### 8.2 Three-way merge

```text
A---B---C---M  main
     \     /
      D---E    feature
```

```bash
git switch main
git merge --no-ff feature
```

A merge commit typically records two parents. `--no-ff` requests a merge commit even when a fast-forward could suffice (unless other conditions prevent merging).

### 8.3 Resolve a conflict

```bash
git status
git diff --name-only --diff-filter=U
git diff
```

A conflicted file can contain markers:

```text
<<<<<<< HEAD
value = 10
=======
value = 20
>>>>>>> feature
```

Edit the file to the intended combined result, remove markers, then:

```bash
git add src/config.py
git merge --continue
```

If you choose not to continue:

```bash
git merge --abort
```

During an ordinary merge, `--ours` denotes the version from the checked-out side and `--theirs` denotes the incoming side:

```bash
git restore --ours -- src/config.py
git restore --theirs -- src/config.py
git add src/config.py
```

**Caution:** During a rebase, the conceptual roles of `ours` and `theirs` are often counterintuitive: `ours` corresponds to the history you are rebasing **onto**; `theirs` corresponds to the replayed commit side. Verify before using either wholesale.

### 8.4 Conflict-resolution tools

```bash
git mergetool
git diff --check
git status
```

Use editor merge views when conflict markers are complex. Never resolve a conflict by deleting lines without understanding the combined behavior.

## 9. Rebasing and Interactive History Editing

### 9.1 Merge vs rebase

```text
Before:
A---B---C    main
     \
      D---E  feature

After merge:
A---B---C---M main
     \     /
      D---E

After rebase feature onto main:
A---B---C       main
         \
          D'---E' feature
```

Rebase **replays** commits as new commits with new IDs. It is useful for maintaining a linear story before merging an unpublished branch.

```bash
git switch feature
git fetch origin
git rebase origin/main
```

On conflicts:

```bash
git status
git add path/to/resolved.py
git rebase --continue
```

Recovery and alternatives:

```bash
git rebase --abort
git rebase --skip
```

`--skip` drops the current commit's patch from the replay; use it only after deciding the change is redundant or intentionally unwanted.

### 9.2 Interactive rebase

```bash
git rebase -i HEAD~4
```

The editor's todo list supports:

| Instruction | Purpose |
|---|---|
| `pick` | Apply the commit |
| `reword` | Edit message |
| `edit` | Stop to modify the commit |
| `squash` | Combine with preceding commit, edit message |
| `fixup` | Combine with preceding commit, usually discard this commit's message |
| `drop` | Remove commit |
| `exec` | Run a command at this point in replay |

You may reorder commits, but dependencies can cause conflicts or failed builds. Rebased commits receive new object IDs.

### 9.3 Autosquash

```bash
git commit --fixup=HEAD~1
git rebase -i --autosquash HEAD~3
```

`--fixup` creates a commit marked for folding into a target commit. Autosquash rearranges/rewrites the todo list accordingly.

### 9.4 Rebase starting from an earlier fork point

```bash
git rebase --onto main old-base feature
```

Interpretation: take commits reachable from `feature` but not from `old-base`, and replay them onto `main`; update the `feature` branch when the operation finishes. This can transplant a subset of a branch's work.

### 9.5 Rewrite policy

Safe defaults:

- Rebase and squash **your own local, unpublished** feature work.
- Avoid rebasing a shared branch that collaborators already use.
- If you must replace published feature history, coordinate and consider `--force-with-lease`.
- Keep merge commits when they convey useful integration history.

## 10. Undoing Changes: Restore, Reset, Revert

### 10.1 Choose based on what you want to change

| Goal | Preferred command | Main effect |
|---|---|---|
| Discard unstaged edits to tracked file | `git restore file` | Working tree overwritten from index |
| Unstage changes while keeping file edits | `git restore --staged file` | Index reset from `HEAD` |
| Restore tracked file in both index and worktree | `git restore --staged --worktree file` | Both match `HEAD` |
| Move branch back one commit, keep changes staged | `git reset --soft HEAD~1` | Ref moves; index/worktree retained |
| Move branch back one commit, keep edits unstaged | `git reset --mixed HEAD~1` | Ref and index move; worktree retained |
| Discard tracked changes and reset branch | `git reset --hard HEAD~1` | Ref, index, worktree reset |
| Undo a published commit without rewriting history | `git revert <commit>` | New inverse commit |

### 10.2 Restore examples

```bash
git restore README.md
git restore --staged README.md
git restore --source=HEAD~1 -- README.md
git restore --source=HEAD --staged --worktree -- README.md
```

`git restore` may delete tracked paths that do not exist in the chosen source. Review changes before destructive use.

### 10.3 Reset, explained in three modes

```bash
git reset --soft HEAD~1
git reset --mixed HEAD~1
git reset --hard HEAD~1
```

These are **alternatives**, not steps to run sequentially. By default, `git reset <commit>` means `--mixed`.

```text
Mode      Move branch/HEAD?   Replace index?   Replace tracked worktree?
soft      yes                 no               no
mixed     yes                 yes              no
hard      yes                 yes              yes
```

`--hard` can irreversibly discard uncommitted tracked edits and may remove obstructing untracked files; inspect status and make a backup before running it. It does **not** mean “delete every untracked file.”

### 10.4 Revert public history

```bash
git revert HEAD
git revert --no-commit HEAD~2..HEAD
```

The range example stages the cumulative reversals for the commits selected by that revision range; inspect and commit the result. Reverting a merge requires choosing a mainline parent:

```bash
git revert -m 1 <merge-commit>
```

Mainline selection has subtle future-merge implications; investigate the graph and desired semantics first.

### 10.5 Clean untracked files

```bash
git clean -nd
git clean -nfd
```

`-n` previews; `-f` actually removes eligible untracked files and `-d` includes directories. `-x` additionally includes ignored files; take extreme care with caches, datasets, and virtual environments.

## 11. Stashing Unfinished Work

### 11.1 Save temporary changes

```bash
git stash push -m "WIP: metric validation"
git stash push -u -m "WIP: include untracked tests"
git stash list
git stash show -p stash@{0}
```

By default, stash records tracked changes (staged/unstaged), not arbitrary untracked files. `-u` includes untracked files, but not ignored files.

### 11.2 Apply, pop, or branch

```bash
git stash apply stash@{0}
git stash pop stash@{0}
git stash branch recover/stashed-work stash@{0}
git stash drop stash@{0}
```

`apply` keeps the stash entry; `pop` attempts to apply and remove it (on conflict, Git generally retains it). `stash branch` can help when reapplication to your current branch produces conflicts.

### 11.3 Stash only selected changes

```bash
git stash push -p
git stash push -- src/metrics.py tests/test_metrics.py
```

Use a worktree (Section 16) instead of stashing if you need to keep two branches actively checked out for longer work.

## 12. Team Collaboration and Pull Requests

### 12.1 Typical feature-branch cycle

```bash
git switch main
git pull --ff-only
git switch -c feat/new-evaluation
```

Make changes, run tests, inspect staged files, and commit:

```bash
git status
git diff --check
git add -p
git commit -m "feat: implement evaluation summary"
git push -u origin feat/new-evaluation
```

Then open a pull/merge request on your hosting platform and request review. Review requests, required checks, branch protection, and merge options are hosting-service features rather than core Git commands.

### 12.2 Update after review

```bash
git add src/evaluation.py tests/test_evaluation.py
git commit -m "fix: address evaluation edge cases"
git push
```

Squashing on the server may produce a new merge commit or squash commit depending on settings; the local feature commits may not appear individually on `main`.

### 12.3 Fork-based collaboration

```bash
git remote add upstream https://github.com/original/project.git
git fetch upstream
git switch main
git merge --ff-only upstream/main
git push origin main
```

Convention: `origin` is your fork and `upstream` is the canonical project. This is a convention, not a Git rule.

### 12.4 Strategy trade-offs

| Approach | History | Trade-off |
|---|---|---|
| Merge commit | Preserves topology and original commit IDs | More branch structure |
| Squash merge | One combined commit on target | Loses individual feature commits on target |
| Rebase and merge | Linear target history with rewritten commits | Rewritten IDs; original merge context may be lost |
| Trunk-based development | Short-lived branches, frequent integration | Needs strong tests/feature flags |

## 13. Tags and Releases

### 13.1 Lightweight vs annotated tags

```bash
git tag v1.0.0
git tag -a v1.1.0 -m "Release 1.1.0"
git tag --list
git show v1.1.0
```

Lightweight tags are direct refs. Annotated tags are separate tag objects with metadata and an annotation; generally appropriate for published releases.

### 13.2 Publish tags

```bash
git push origin v1.1.0
git push origin --tags
```

A normal `git push` does not necessarily push every tag. Avoid moving an already published release tag because downstream automation may depend on it.

---

# Part III — Advanced Techniques

## 14. Cherry-pick, Reflog, and Recovery

### 14.1 Cherry-pick a commit

```bash
git switch release/1.x
git cherry-pick <commit-id>
```

Cherry-picking applies a commit's change as a **new commit on the current branch**. The new commit usually has a different ID.

```bash
git cherry-pick --no-commit <commit-id>
git cherry-pick --continue
git cherry-pick --abort
```

The continuation commands are relevant after conflicts; `--no-commit` applies a change without automatically committing.

### 14.2 Reflog tracks movements of references

```bash
git reflog
git reflog show main
git show HEAD@{1}
git switch -c recover/lost-work <commit-id>
```

Reflog can recover a commit after an accidental reset, branch deletion, or rebase **while the object is still reachable through reflog entries and has not been pruned**. Reflogs are local and expire; they are not guaranteed permanent backups.

### 14.3 Recovery scenario

Suppose you accidentally reset to an earlier commit:

```bash
git reflog -5
git switch -c rescue/previous-tip <previous-tip-id>
```

Inspect the rescued branch and then choose whether to merge, cherry-pick, or reset back. Creating a rescue branch before experimenting preserves a named reference to the discovered commit.

## 15. Debugging History: Blame, Bisect, Search

### 15.1 Blame and file history

```bash
git blame src/model.py
git blame -L 15,35 src/model.py
git log --follow --oneline -- src/model.py
git log -p -- src/model.py
```

`blame` attributes lines to commits; this is a debugging tool, not proof of personal responsibility for a defect. `--follow` helps inspect a single file through renames but has limitations.

### 15.2 Search tracked content and history

```bash
git grep -n "TODO"
git grep -n "predict" -- '*.py'
git log -S 'threshold = 0.5' --oneline -- src/
git log -G 'threshold\s*=' --oneline -- src/
```

`-S` finds commits where the **number of occurrences** of a given string changes; `-G` searches diff lines matching a regex. Neither is identical to ordinary text search.

### 15.3 Binary search for a regression

```bash
git bisect start
git bisect bad
git bisect good <known-good-commit>
```

At each proposed revision, test the behavior and mark:

```bash
git bisect good
git bisect bad
git bisect skip
```

Finish with:

```bash
git bisect reset
```

For deterministic test commands, Git can automate the search:

```bash
git bisect start HEAD <known-good-commit>
git bisect run python -m pytest tests/test_regression.py -q
git bisect reset
```

For `bisect run`, exit code **0** = good, **1–127 except 125** = bad, **125** = skip; special handling applies to other codes. Use a test that reliably distinguishes good from bad revisions.

## 16. Multiple Worktrees and Sparse Checkout

### 16.1 Worktrees: several branches, separate folders

```bash
git worktree add ../project-hotfix -b fix/urgent main
git worktree list
git worktree remove ../project-hotfix
```

A linked worktree has its own working files, index, and `HEAD`, but shares most repository objects and refs. Git ordinarily prevents checking out the same branch in multiple worktrees simultaneously.

Worktrees are useful when you are running a long experiment on one branch while testing a hotfix on another.

### 16.2 Sparse checkout

```bash
git sparse-checkout init --cone
git sparse-checkout set src tests
git sparse-checkout list
git sparse-checkout disable
```

Sparse checkout limits which tracked paths populate the working tree; it does not by itself imply that the complete history was avoided during clone. Cone mode is optimized for directory-oriented rules.

### 16.3 Partial / shallow clones

```bash
git clone --depth 1 https://github.com/example/repository.git
git clone --filter=blob:none https://github.com/example/repository.git
```

Shallow clone restricts available history. Partial clone can defer download of some objects if the remote supports it. Some history-oriented operations may require fetching additional data.

## 17. Submodules, Git LFS, and Large Repositories

### 17.1 Submodules

```bash
git submodule add https://github.com/example/library.git external/library
git clone --recurse-submodules https://github.com/example/project.git
git submodule update --init --recursive
```

A superproject records a submodule commit ID (a *gitlink*) and configuration in `.gitmodules`. A submodule is a distinct repository; simply updating its remote branch does not automatically update the superproject's recorded pointer.

### 17.2 Git LFS

Git LFS is an **additional tool**, not built into every Git installation. It stores pointer files in ordinary Git objects and manages binary content separately.

```bash
git lfs install
git lfs track '*.parquet'
git add .gitattributes
git add data/sample.parquet
git commit -m "data: track sample with LFS"
```

Before adopting LFS, consider cost/storage quotas, remote support, dataset licenses, and whether a data/versioning tool is more suitable. Tracking a pattern with LFS does not automatically migrate existing Git history.

### 17.3 Repository strategies for data science

- Track source code, tests, configuration templates, and environment specifications.
- Ignore reproducible caches, local virtual environments, and machine-specific files.
- Treat raw datasets, checkpoints, models, and notebooks case-by-case: size, reproducibility, privacy, licensing, and reviewability matter.
- Avoid committing secrets, tokens, credentials, proprietary data, or huge generated outputs.

## 18. Ignore Rules, Attributes, and Hooks

### 18.1 `.gitignore`

Example Python/data project:

```gitignore
__pycache__/
*.py[cod]
.venv/
.pytest_cache/
.ipynb_checkpoints/
.env
.env.*
!.env.example
data/raw/
models/checkpoints/
dist/
*.egg-info/
```

Pattern basics:

| Pattern | Meaning |
|---|---|
| `*.log` | Matching log filenames at relevant levels |
| `build/` | Directories named `build` |
| `/output/` | `output` directory at the level of this `.gitignore` |
| `!important.log` | Negation of a previous ignore rule, subject to parent-directory rules |
| `**/cache/` | Matching cache directories at multiple levels |

```bash
git check-ignore -v data/raw/input.csv
git ls-files
git rm --cached .env
```

`.gitignore` does **not** stop tracking files already in the index. Removing a tracked secret and committing that removal does **not** remove the secret from existing history.

### 18.2 `.gitattributes`

```gitattributes
*.sh text eol=lf
*.bat text eol=crlf
*.png binary
*.ipynb linguist-generated=false
```

The first three lines are Git attributes for text/line endings and binary treatment. `linguist-generated` is interpreted by some hosting tooling, not Git's core merge engine.

Use `.gitattributes` when consistent line endings, diff behavior, filters, or merge strategies are needed across operating systems. Changing EOL normalization may create a one-time large diff; coordinate repository-wide changes.

### 18.3 Hooks

Git hooks are executable scripts located in the configured hooks directory (often `.git/hooks/`). Common names:

| Hook | Typical use |
|---|---|
| `pre-commit` | Formatting, quick tests, secret checks |
| `commit-msg` | Commit-message validation |
| `pre-push` | Test/lint checks |
| `post-checkout` | Local environment setup |

Ordinary local hooks are **not automatically shared by cloning** a repository. Teams often use hook-management tools or CI to enforce consistent checks.

## 19. Git Internals and Plumbing

### 19.1 Four core object types

| Object | Stores |
|---|---|
| Blob | Raw file contents |
| Tree | Directory entries mapping names/modes to object IDs |
| Commit | Tree ID, parent ID(s), author/committer metadata, message |
| Annotated tag | Named annotated target object and metadata |

Object IDs identify content. Git repositories typically use SHA-1 format, while SHA-256 repositories exist; do not assume a fixed 40-character ID in generic tooling.

### 19.2 Inspect raw objects

```bash
git rev-parse HEAD
git cat-file -t HEAD
git cat-file -p HEAD
git ls-tree HEAD
git ls-tree -r HEAD
```

Read-only examples are safe for exploration. The tree associated with a commit represents its snapshot; parent links create history.

### 19.3 Refs, `HEAD`, and the index

```bash
git symbolic-ref HEAD
git show-ref
git for-each-ref --format='%(refname:short) %(objectname:short)'
git ls-files --stage
```

- Branch refs live conceptually under `refs/heads/`.
- Remote-tracking refs live under `refs/remotes/`.
- Tags live under `refs/tags/`.
- Refs may be stored in loose files or other ref backends; don't assume filesystem layout in tooling.
- Index entries refer to staged objects and file modes; unresolved merges may have multiple index stages.

### 19.4 Content-addressed storage and packfiles

Git hashes objects; unchanged contents can share underlying objects. Loose objects may be consolidated into packfiles and delta-compressed for efficiency. Reachability from refs and reflogs influences when unreachable objects can be pruned.

```bash
git count-objects -v
git fsck --full
git gc
```

`git fsck` verifies connectivity/integrity to the extent supported by the options; `git gc` performs maintenance. Running them normally is not necessary for routine development.

### 19.5 Plumbing vs porcelain

- **Porcelain:** Human-facing commands such as `status`, `commit`, `switch`, `log`.
- **Plumbing:** Lower-level interfaces such as `cat-file`, `rev-parse`, `update-ref`, `ls-files`.

Scripts often benefit from stable machine-readable options, for example:

```bash
git status --porcelain=v1 -z
git ls-files -z
git rev-parse --show-toplevel
```

The `-z` format emits NUL delimiters, which safely represent filenames containing spaces or newlines.

## 20. Advanced Configuration, Security, and Maintenance

### 20.1 Rerere: reuse conflict resolutions

```bash
git config --global rerere.enabled true
git rerere status
git rerere diff
```

When repeated rebases/merges produce a familiar conflict, rerere may reapply a previously recorded resolution. Always inspect the result and run tests.

### 20.2 Useful comparison and maintenance tools

```bash
git range-diff main...feature@{1} main...feature
git diff --word-diff
git diff --name-only main...feature
git maintenance run
git branch --merged main
```

`range-diff` compares two sequences of commits, useful after rewriting a PR branch. `git maintenance run` performs repository maintenance tasks supported/configured by your Git version.

### 20.3 Signing and authentication

- Configure SSH authentication for hosting separately from your commit identity.
- Keep tokens in an OS-supported credential manager, not shell scripts or committed files.
- Commit signing (SSH/GPG) attests to a signing identity when properly verified; it does not validate code quality.
- Review `.git/config` and hosting permissions before automating pushes or allowing untrusted hooks.

### 20.4 Sensitive data already committed

1. **Revoke/rotate the credential immediately.**
2. Remove it from current files, environment/configuration, and CI variables as appropriate.
3. Assess whether full history rewriting is needed; use a purpose-built tool such as `git filter-repo` and coordinate with all downstream clones/remotes.
4. Treat history rewriting as a disruptive maintenance operation; old clones, forks, and caches may retain the data.

Never treat `.gitignore` or a normal deletion commit as secret remediation by itself.

---

# Part IV — Applying Git in Real Projects

## 21. Practical Project Workflows

### 21.1 New Python/data-science repository

```bash
mkdir model-evaluation
cd model-evaluation
git init
printf '# Model Evaluation\n' > README.md
printf '.venv/\n__pycache__/\n.pytest_cache/\n.env\n' > .gitignore
mkdir -p src tests notebooks
git add README.md .gitignore
git commit -m "chore: initialize repository"
```

Create small commits for independently understandable work: source-code change, test addition, documentation update, then follow-up fixes.

### 21.2 Safely update a feature branch from upstream main

```bash
git status
git fetch origin
git switch feat/metrics
git rebase origin/main
git diff --check
git push --force-with-lease
```

Run this sequence **only if** you intentionally use a rebase workflow, have a clean or appropriately stashed worktree, and are authorized to rewrite that feature branch's published commits. Otherwise choose `merge` or new commits.

### 21.3 Undo an accidental commit on a published branch

```bash
git log -3 --oneline
git revert <bad-commit-id>
git push
```

This is typically safer than resetting and force-pushing a shared branch.

### 21.4 Separate unrelated edits into coherent commits

```bash
git diff
git add -p
git diff --staged
git commit -m "refactor: extract data transformer"
git add -A
git diff --staged
git commit -m "test: cover transformer edge cases"
```

Review the selected hunks carefully; later unstaged hunks may depend on changes already committed.

### 21.5 Investigate a broken CI build

```bash
git log --oneline -10
git show --stat HEAD
git diff HEAD~1 HEAD -- tests/
git blame src/pipeline.py
git bisect start HEAD <known-good-commit>
git bisect run python -m pytest tests/test_pipeline.py -q
git bisect reset
```

A passing bisect test must be reproducible across the candidate revisions; environment/API drift can create false conclusions.

## 22. Command Reference and Decision Tables

### 22.1 High-frequency commands

| Command | Purpose |
|---|---|
| `git init` | Initialize local repository |
| `git clone URL` | Clone repository |
| `git status -sb` | Compact branch/status view |
| `git add -p` | Stage selected hunks |
| `git diff` | Inspect unstaged changes |
| `git diff --staged` | Inspect staged changes |
| `git commit -m "..."` | Create commit |
| `git log --oneline --graph --all` | Visualize history |
| `git switch -c branch` | Create and switch branch |
| `git fetch --prune` | Update remote-tracking refs |
| `git pull --ff-only` | Pull only when fast-forward possible |
| `git push -u origin branch` | Publish branch and set upstream |
| `git merge branch` | Integrate branch via merge |
| `git rebase main` | Replay commits onto another base |
| `git stash push -u` | Store work including untracked files |
| `git restore file` | Discard unstaged tracked edits |
| `git restore --staged file` | Unstage changes |
| `git revert commit` | Create inverse commit |
| `git reflog` | Inspect local ref movements |
| `git worktree add path branch` | Make another checkout |

### 22.2 Decision guide

| You want to... | Usually use... | Important warning |
|---|---|---|
| See what's changed | `status`, `diff` | Distinguish staged from unstaged |
| Keep edits but undo staging | `restore --staged` | Does not discard disk contents |
| Discard tracked local edits | `restore` | Destructive to those edits |
| Undo an unpushed commit | `reset --soft` or `--mixed` | Rewrites local history |
| Undo a pushed bad commit | `revert` | Adds an inverse commit |
| Integrate remote work | `fetch` then `merge`/`rebase` | Choose explicit strategy |
| Backport a particular fix | `cherry-pick` | New commit, possible conflicts |
| Recover lost commit | `reflog`, rescue branch | Subject to expiry/pruning |
| Pause current work | `stash` | Not a permanent versioned feature branch |
| Work on two branches at once | `worktree` | Shared object store, distinct worktrees |

### 22.3 Frequent misconceptions

| Misconception | Reality |
|---|---|
| `git add` means permanently save | It only stages a snapshot for a future commit |
| `git commit` uploads to GitHub | Commits are local until pushed |
| `git fetch` changes my current code | It normally updates remote-tracking refs, not your checked-out tracked files |
| A branch is a separate folder of commits | It is a movable ref to a commit |
| Rebase keeps the same commit IDs | Replay ordinarily creates new commits |
| `.gitignore` removes already tracked files | It applies to untracked candidates, not already indexed paths |
| `git reset --hard` is always recoverable | Uncommitted edits may be lost permanently |
| A shallow clone has all history | It deliberately omits some ancestry |

## 24. Official References

- [Git documentation index](https://git-scm.com/docs)
- [Pro Git book — free online](https://git-scm.com/book/en/v2)
- [Git branches in a nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [Git rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)
- [Reset demystified: the three trees](https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified)
- [git-restore manual](https://git-scm.com/docs/git-restore)
- [git-rebase manual](https://git-scm.com/docs/git-rebase)
- [git-worktree manual](https://git-scm.com/docs/git-worktree)
- [git-revisions manual](https://git-scm.com/docs/gitrevisions)

**Suggested progression:** Master sections 1–7, then practice 8–12 using a throwaway repository. Study section 10 before using destructive commands. Sections 14–20 become substantially easier once the three-tree model and commit graph are intuitive.
