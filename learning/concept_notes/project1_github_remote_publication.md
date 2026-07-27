# GitHub Remotes and Public Portfolio Publication

## Core Idea

A Git commit records a snapshot in the local repository. A Git remote connects that local repository to another Git repository, such as one hosted on GitHub. Pushing sends local commits to that remote.

```text
working files -> staging area -> local commit -> push -> GitHub repository
```

Committing and pushing are separate operations. A commit can exist safely on one computer without appearing on GitHub.

## The Project Remote

This repository uses the remote name `origin` for:

```text
https://github.com/kpasichnuk/calgary-spatial-etl.git
```

The local `main` branch tracks `origin/main`. Inspect that relationship with:

```bash
git remote -v
git branch -vv
git status --short --branch
```

## Public Versus Private

A public repository can support a portfolio because employers can inspect:

- source code and architecture
- documentation and learning materials
- tests and verification practices
- commit history
- how the project changed over time

A private repository is appropriate when the content includes proprietary code, restricted data, confidential requirements, or material that is not ready to disclose.

Public visibility should be a deliberate decision, not a substitute for a security review.

## What Becomes Public

Publishing a repository exposes:

- every pushed commit and its files
- commit messages
- commit author names and email metadata
- branches and tags that are pushed
- any secrets preserved in pushed history

Deleting a credential in a later commit does not remove it from earlier commits. A leaked credential must be rotated or revoked, and repository history may need remediation.

## Safe Publication Checklist

Before the first push:

1. Inspect tracked and untracked files.
2. Review `.gitignore`.
3. Exclude generated data, logs, reports, caches, and local editor state.
4. Search candidate content for passwords, tokens, keys, and credential-bearing URLs.
5. Inspect the exact staged diff.
6. Run relevant tests.
7. Commit only the reviewed snapshot.
8. Verify the remote URL before pushing.

Never send passwords, access tokens, private keys, or SSH keys through documentation or chat. Authentication belongs in a credential manager, browser flow, or local SSH configuration.

## Creating the GitHub Repository

When a local repository already contains history, create an empty GitHub repository. Do not initialize it with another README, `.gitignore`, or license unless you intend to reconcile two histories.

Typical setup:

```bash
git remote add origin https://github.com/OWNER/REPOSITORY.git
git push -u origin main
```

The `-u` option establishes `origin/main` as the upstream branch. Later pushes can normally use:

```bash
git push
```

## Verification

A successful command is useful evidence, but comparing commit IDs is stronger:

```bash
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

The local and remote hashes should match after a successful push.

## Important Distinctions

- **Commit:** local immutable snapshot.
- **Remote:** named connection to another repository.
- **Push:** publishes local commits to a remote.
- **Upstream:** remote branch associated with a local branch.
- **Public repository:** visible to anyone.
- **Private repository:** visible only to authorized accounts.

## Related Resources

- [Module 2 Git reference](../reference/project1_module_2_git_reference.md)
- [Module 2 Git practice](../practice/project1_module_2_git_practice.ipynb)
