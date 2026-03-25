# Code Review Process

## Purpose
Ensure all code changes meet quality, security, and maintainability standards before merging to production branches.

## Requirements
- All code changes require at least 1 approval before merge
- Changes to critical systems (auth, payments, data pipeline) require 2 approvals
- Self-merging is not allowed for production branches
- Reviews should be completed within 1 business day

## Reviewer Checklist
1. **Correctness**: Does the code do what the PR description claims?
2. **Testing**: Are there adequate tests? Do edge cases have coverage?
3. **Security**: No hardcoded secrets, SQL injection, XSS, or auth bypass
4. **Performance**: No N+1 queries, unnecessary loops, or memory leaks
5. **Readability**: Clear naming, appropriate comments, consistent style
6. **Architecture**: Follows established patterns, no unnecessary complexity

## PR Standards
- Title: Clear, concise description of the change
- Description: What changed, why, how to test, any migration steps
- Size: Aim for <400 lines changed. Split larger changes into stacked PRs
- Linked ticket: Every PR references the task/issue it addresses

## Merge Policy
- Squash merge for feature branches
- Merge commit for release branches
- All CI checks must pass before merge
- Branch protection enabled on main and release branches
