# Deterministic Reachability Snapshot Provider Implementation Plan

Status: Completed

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Replace the vacuous live-network Boolean test with deterministic coverage for unavailable and supplied reachability flag snapshots.

**Architecture:** Keep `isConnectedToNetwork()` as the unchanged public entry point and leave SystemConfiguration acquisition there. Add one internal closure-based overload that accepts an optional flag snapshot and delegates non-nil values to the existing public flag evaluator, allowing XCTest to cover acquisition failure and success without live network state.

**Tech Stack:** Swift, SystemConfiguration, XCTest, Python static contracts, Xcode hosted tests.

---

### Task 1: Add RED snapshot contracts

**Files:**
- Modify: `NetworkStateTests/NetworkStateTests.swift`
- Modify: `scripts/check-baseline.py`
- Modify: `tests/test_baseline_contracts.py`

Add XCTest for a nil provider returning false and supplied flags matching `isReachableWithFlags`. Reject the old `result || !result` tautology. Add hostile source mutations that bypass nil handling or the shared evaluator.

Run `python3 scripts/check-baseline.py`; expect failure because the internal provider overload does not exist.

### Task 2: Extract the minimal seam

**Files:**
- Modify: `NetworkState/NetworkState.swift`

Make the public method acquire an optional snapshot and pass it to an internal closure-based overload. Return false for nil and delegate non-nil flags to `isReachableWithFlags`.

Run the focused Python tests and baseline; expect green.

### Task 3: Reconcile maintenance documentation

**Files:**
- Modify: `README.md`
- Modify: `SECURITY.md`
- Modify: `VISION.md`
- Modify: `AGENTS.md`
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-26-deterministic-snapshot-provider.md`

Record the deterministic boundary, RED/GREEN evidence, lack of public API change, runtime limitations, and next live-network validation step.

### Task 4: Verify and ship

Run root and external-directory `make check`, Python tests, `git diff --check`, hosted Xcode, CodeQL, and exact-head Codex review. Merge only the exact green head.

## Result

The public API now supplies an optional SystemConfiguration flag snapshot to an
internal evaluator. Nil snapshots fail closed and supplied snapshots delegate
to `isReachableWithFlags(_:)`. The former tautological live-network XCTest was
replaced with deterministic nil and supplied-snapshot coverage; final local and
hosted evidence is recorded in `CHANGES.md` before merge. Root and
external-directory `make check`, all 19 Python policy tests, Python compilation,
and `git diff --check` pass locally; native XCTest remains a hosted gate.
