# GitFlow Workflow Guide

## Overview
This repository follows the GitFlow branching strategy for organized development and release management.

## Branch Structure

### Main Branches
- **`master`** - Production-ready code. Only contains stable, tested releases.
- **`develop`** - Integration branch where feature branches are merged. Contains the latest development changes.

### Supporting Branches
- **`feature/*`** - New features or enhancements
- **`release/*`** - Prepare for production releases
- **`hotfix/*`** - Emergency fixes for production issues

## Workflow Process

### 1. Feature Development
```bash
# Start a new feature from develop
git checkout develop
git pull origin develop
git checkout -b feature/feature-name

# Work on your feature...
# Commit changes regularly
git add .
git commit -m "feat: add new feature description"

# Push feature branch
git push -u origin feature/feature-name

# Create Pull Request: feature/feature-name → develop
```

### 2. Release Process
```bash
# Start a release from develop
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# Final testing and bug fixes...
git commit -m "fix: release preparation fixes"

# Push release branch
git push -u origin release/v1.0.0

# Create Pull Request: release/v1.0.0 → master
# After merge, also merge back to develop
```

### 3. Hotfix Process
```bash
# Start hotfix from master
git checkout master
git pull origin master
git checkout -b hotfix/critical-fix

# Apply the fix...
git commit -m "fix: critical production issue"

# Push hotfix branch
git push -u origin hotfix/critical-fix

# Create Pull Request: hotfix/critical-fix → master
# After merge, also merge back to develop
```

## Pull Request Rules

### Required for All Changes
- ✅ All changes must go through Pull Requests
- ✅ No direct pushes to `master` or `develop`
- ✅ Require at least 1 approval for merges
- ✅ All CI/CD checks must pass
- ✅ Branch must be up-to-date before merging

### PR Templates
- Use descriptive titles following conventional commits
- Include detailed description of changes
- Reference any related issues
- Add screenshots for UI changes
- List any breaking changes

## Commit Message Convention

Follow conventional commits format:
```
type(scope): description

feat: add new feature
fix: bug fix
docs: documentation changes
style: formatting changes
refactor: code refactoring
test: adding tests
chore: maintenance tasks
```

## Branch Protection Rules (To be set on GitHub)

### Master Branch
- Require pull request reviews before merging
- Dismiss stale PR approvals when new commits are pushed
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Include administrators in restrictions

### Develop Branch
- Require pull request reviews before merging
- Require status checks to pass before merging
- Require branches to be up to date before merging

## Quick Reference Commands

```bash
# Check current branch
git branch

# Switch to develop
git checkout develop

# Create feature branch
git checkout -b feature/my-feature

# Update local develop with remote changes
git checkout develop && git pull origin develop

# Delete feature branch after merge
git branch -d feature/my-feature
git push origin --delete feature/my-feature
```

## Emergency Procedures

### If direct push happens accidentally:
1. Immediately create a hotfix branch from the commit
2. Revert the direct push
3. Submit proper PR with the changes

### If develop gets out of sync with master:
```bash
git checkout develop
git pull origin master
git push origin develop
```

---

**Remember**: Never work directly on `master` or `develop`. Always use feature branches and Pull Requests!