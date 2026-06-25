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
- Trimming leading whitespace would also turn a malformed nonmatching rule into
  the required canonical pattern inside the checker.
- A later `!.explore/` negation can disable the directory rule even when the
  canonical text remains present.

## Decisions

- Add the exact active `.explore/` directory pattern to `.gitignore`.
- Parse active ignore entries without trimming their pattern bytes so comments
  and malformed leading whitespace cannot satisfy required ignore contracts.
- Verify both the directory and a representative file with pinned
  `git check-ignore --no-index` so ordered negations, selective child
  re-inclusion, and Git's real pattern semantics remain authoritative.
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
- Prove a leading-space rule remains distinct from the required canonical rule.
- Prove a later negation disables the effective ignore check.
- Run every Make alias from the root and an external working directory.
- Require exact-head Codex review and hosted Xcode/CodeQL success before merge.

## Risks

- Ignored local notes are not shared through Git. Any durable technical decision
  must therefore be copied into tracked plans, changes, policies, or source.
- This change does not alter reachability behavior, public API, package version,
  Xcode settings, or hosted tool authority.

## Verification Result

- The red-first baseline rejected the absent `.explore/` rule.
- The red-first unit regression rejected the missing active-pattern helper.
- Commented and leading-space lookalikes were rejected for the intended
  canonical-pattern boundary.
- All six Make aliases passed from root and an external directory with 13
  Python policy tests per invocation.
- Codex found and prompted the leading-whitespace correction; the corrected
  exact head received a clean follow-up review. A later review found the
  negation bypass, which is now covered through effective Git behavior.
- CodeQL Actions/Python and both exact-head macOS jobs passed. One initial PR
  runner lacked an installed simulator; an unchanged rerun passed the complete
  framework build and XCTest suite, confirming transient runner variance.
