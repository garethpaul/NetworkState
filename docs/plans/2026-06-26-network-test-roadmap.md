# Network Test Roadmap Reconciliation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Reconcile the network-test roadmap with deterministic snapshot coverage and the constrained-path API boundary.

**Architecture:** Preserve the legacy synchronous `SCNetworkReachability` implementation and iOS 8 compatibility surface. Enforce exact documentation stating that unavailable/reachable snapshots are covered and constrained-path state requires a separate Network framework migration.

**Tech Stack:** Swift/SystemConfiguration documentation, Python 3 static contracts, GNU Make, GitHub Actions

---

status: completed

### Task 1: Write The Failing Documentation Contract

**Files:**
- Modify: `scripts/check-baseline.py`

Require the exact snapshot-coverage and constrained-path boundary in maintained
guidance, require the stale roadmap item to be absent, and require this plan to
be completed.

Run `make check` and confirm it fails before documentation changes.

### Task 2: Reconcile Maintained Guidance

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `SECURITY.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`

Document completed unavailable/reachable snapshot coverage and the separate
Network framework compatibility decision needed for constrained-path testing.

### Task 3: Complete Evidence

**Files:**
- Modify: `docs/plans/2026-06-26-network-test-roadmap.md`

Record red-first evidence, mutation results, root/external Make results, hosted
boundaries, and completion status.

### Task 4: Validate And Review

Run focused hostile mutations, all Make aliases from repository and external
working directories, syntax/diff/secret audits, Codex review, and hosted checks.
Merge only the exact unchanged green head.

## Verification Completed

- Red-first `make check` failed on the pending plan, missing exact guidance in
  five maintained documents, and stale combined roadmap item.
- The maintained guidance now distinguishes deterministic unavailable/reachable
  snapshots from constrained-path state in Network framework.
- Root and external-directory `make check` plus all six documented Make aliases
  passed, each including the baseline and 19 Python policy tests.
- Isolated mutations cover stale roadmap restoration, missing constrained-path
  guidance, missing snapshot guidance, and incomplete-plan evidence.
- Hosted macOS remains authoritative for Xcode project compilation and XCTest.
