---
title: Document CocoaPods source boundary
status: completed
date: 2026-06-25
---

# Document CocoaPods Source Boundary

## Goal

Prevent consumers from treating the historical `0.0.2` tag as the current
Swift implementation or assuming that the checked-in root podspec proves a
published CocoaPods trunk release.

## Evidence

- The root `NetworkState.podspec` still declares version `0.0.2` and a source
  tag derived from that version.
- The historical 0.0.2 tag points to commit
  `a310b6718f495f9d5ce835692533b6c8f073bdf9` from 2016.
- The current default branch includes public API, guarded reachability
  creation, a shared flag evaluator, exhaustive truth-table tests, and current
  hosted validation that are absent from that tag.
- No matching `NetworkState` spec was found in the CocoaPods Specs repository,
  so trunk availability must not be claimed.

## Decisions

- Document a Git Podfile example that resolves the current root podspec from
  `master` instead of recommending the stale historical tag.
- State that branch installs are mutable and production consumers should
  replace the branch with a reviewed commit.
- Keep release versioning and tag creation out of this documentation-only
  change; a future release requires a new immutable version and pod lint.
- Add exact positive and stale-tag contracts to the dependency-free checker.

## Verification

- Run the baseline checker before the README change and capture the expected
  missing-fragment failures.
- Run focused hostile mutations for the stale tag, trunk overclaim, and
  reviewed-commit guidance.
- Run all Make aliases, direct checker/tests, external-directory verification,
  Python compilation, and `git diff --check`.
- Require hosted Xcode tests and exact-head review before merge.

## Risks

- `master` is not immutable; the README must make reviewed commit pinning
  explicit.
- The root podspec and historical tag continue to share a version number. This
  change prevents unsafe guidance but does not create a package release.

## Verification Result

- The initial checker failed on the absent plan. After adding scope evidence,
  it reported all five missing README fragments and incomplete plan evidence.
- Three hostile mutations were rejected for recommending the historical 0.0.2
  tag, claiming CocoaPods trunk availability, and weakening the reviewed commit
  pinning guidance.
- The first pinning mutation command accidentally allowed shell backtick
  substitution and failed for the wrong reason; the safely quoted rerun was
  rejected for the intended missing guidance.
- Exact-head Codex review found that the first stale-tag regex only caught a
  single-line hash-rocket declaration. The corrected checker normalizes each
  `NetworkState` declaration and rejects both multiline `:tag => '0.0.2'` and
  modern `tag: '0.0.2'` syntax; focused hostile mutations cover both forms.
- Complete local, hosted, and review evidence is recorded in `CHANGES.md`.
