# Project 1 Module 2: Git Reference

## Purpose

This reference teaches the version-control concepts behind [Module 2 Git practice](../practice/project1_module_2_git_practice.ipynb).

## 1. What Git Tracks

Git records saved file content and history. It cannot see an unsaved editor buffer.

Distinguish four states:

1. **Editor buffer:** current content in the editor, possibly unsaved.
2. **Working tree:** saved files on disk.
3. **Staging area:** proposed contents of the next commit.
4. **Commit:** an immutable snapshot in repository history.

## 2. Inspect Before Changing

Start a work session with read-only commands:

```bash
git status
git branch --show-current
git log -1 --oneline
git remote -v
```

These identify the branch, baseline, saved modifications, untracked files, and configured remotes.

## 3. Diff and Staging

Inspect unstaged saved changes:

```bash
git diff
```

Stage specific files:

```bash
git add path/to/file
```

Inspect exactly what the next commit would contain:

```bash
git diff --cached
```

The staging area supports selective commits. Avoid staging everything without reviewing it.

## 4. Commits

A commit should represent one coherent, completed change.

```bash
git commit -m "Add QA quality gate"
```

A useful message describes the result, not the typing activity. Test and review before committing.

## 5. Ignore Rules

`.gitignore` tells Git which untracked paths should normally remain outside version control.

This project ignores generated data, logs, QA reports, caches, local editor settings, and secrets.

Important rule: `.gitignore` does not untrack a file already committed. That requires an explicit index change, and sensitive data may also require history remediation.

## 6. Tracked Source Versus Generated Artifacts

Track definitions needed to reproduce the system:

- source code
- tests
- SQL
- environment definitions
- documentation
- nonsecret examples

Do not normally track reproducible outputs:

- raw downloads
- processed GeoJSON
- logs
- QA reports
- caches
- local environments
- credentials

## 7. Branches

A branch is a movable name pointing to a sequence of commits.

```bash
git switch -c feature/qa-report
```

Branches isolate work while preserving a common history. They do not automatically publish anything to GitHub.

## 8. Remotes and GitHub

A remote is a named connection to another repository.

```bash
git remote add origin <repository-url>
git remote -v
git push -u origin main
```

Fetching downloads remote history. Pulling fetches and integrates it. Pushing publishes local commits.

Use browser authentication, a credential manager, or SSH. Never place a token in a remote URL committed to documentation or notebook output.

## 9. Pull Requests

A pull request is a collaboration and review workflow around commits on a branch. It is not a Git object stored in the local repository.

A good pull request includes:

- focused commits
- clear purpose
- test evidence
- known limitations
- no unrelated generated files or secrets

## 10. Merge Conflicts

A conflict means Git cannot automatically combine competing changes.

Safe process:

1. Read both sides and surrounding context.
2. Understand the intended combined result.
3. Edit the file deliberately.
4. Remove conflict markers.
5. Test the result.
6. Stage the resolved file.
7. Continue the merge or rebase.

Do not resolve conflicts by automatically discarding another person's work.

Notebook conflicts are difficult because `.ipynb` files are JSON. Keep notebook edits focused, avoid unnecessary output churn, and coordinate concurrent changes.

## 11. Restore and Recovery

Inspect before restoring anything.

```bash
git diff path/to/file
git diff --cached path/to/file
```

Restoring a working-tree file can discard saved, uncommitted work. Unstaging and restoring are separate actions.

Commits make recovery easier because prior snapshots remain addressable.

## 12. Secrets

If a real credential is committed:

1. Treat it as exposed.
2. Rotate or revoke it.
3. Remove it from current files.
4. Remediate repository history when required.
5. prevent recurrence with secret management and ignore rules.

Deleting the secret in a later commit does not remove it from earlier history.

## 13. Daily Workflow

```bash
git status
git diff
# edit and test
git add <specific-files>
git diff --cached
git commit -m "Describe the completed change"
git pull --rebase
git push
```

Use `pull --rebase` only when it matches the team's workflow and you understand the branch state.

## 14. Rename Behavior

Before staging, a rename may appear as one deleted path and one untracked path. After staging, Git compares content and often reports the pair as a rename.

Git does not store a special rename operation; rename detection is based primarily on content similarity.

## Common Misconceptions

- Git tracks unsaved editor changes. It does not.
- Staging saves a backup. It prepares a commit snapshot.
- `.gitignore` removes tracked history. It does not.
- A branch is a copy of the entire repository. It is a reference into commit history.
- Pushing and committing are the same. Commit is local; push publishes commits.
- Deleting a leaked secret fixes exposure. Rotation is still required.

## Review Checklist

You should be able to explain:

- editor buffer, working tree, staging area, and commit
- tracked, untracked, ignored, and staged files
- branches, remotes, fetch, pull, and push
- selective staging and staged review
- conflict resolution
- safe secret response
- why generated ETL artifacts remain outside history

## Companion Resources

- [Module 2 Git practice](../practice/project1_module_2_git_practice.ipynb)
- [Project 1 learning index](../README.md)
- [Project 1 study guide](../guides/project1_study_guide.md)
