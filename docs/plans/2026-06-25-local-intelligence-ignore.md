---
title: Ignore local repository intelligence
status: completed
date: 2026-06-25
---

# Ignore Local Repository Intelligence

## Goal

Keep maintainer-local `.explore/` notes out of source-control status, package
input, and accidental pull-request changes while preserving durable decisions
in reviewed repository documents.

## Evidence

- The repository already persists local exploration notes under `.explore/`.
- `.gitignore` did not match that directory, so a freshly synchronized checkout
  reported every local intelligence file as untracked.
- The canonical checker enforced generated, signing, credential, and local
  configuration exclusions but did not enforce the intelligence boundary.
- A raw substring check would accept a commented-out ignore rule even though
  Git would not apply it.

## Decisions

- Add the exact active `.explore/` directory pattern to `.gitignore`.
- Parse active ignore entries in the baseline checker so comments cannot satisfy
  required ignore contracts.
- Document that local notes are not product source or durable review evidence.
- Keep the change repository-local; do not delete or publish existing local
  intelligence files.

## Verification

- Add the checker expectation before the ignore rule and capture the intended
  `.gitignore must include .explore/` failure.
- Run the canonical baseline and all Python policy tests.
- Verify `git check-ignore` accepts a representative `.explore/` file.
- Temporarily comment out the rule and prove the strengthened checker rejects
  it, then restore the active rule.
- Run every Make alias from the root and an external working directory.
- Require exact-head Codex review and hosted Xcode/CodeQL success before merge.

## Risks

- Ignored local notes are not shared through Git. Any durable technical decision
  must therefore be copied into tracked plans, changes, policies, or source.
- This change does not alter reachability behavior, public API, package version,
  Xcode settings, or hosted tool authority.
