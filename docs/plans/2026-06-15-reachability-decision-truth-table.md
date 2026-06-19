# Reachability Decision Truth Table

Status: completed

## Problem

`NetworkState.isReachableWithFlags(_:)` derives its result from four decision
bits: `Reachable`, `ConnectionRequired`, either automatic-connection flag, and
`InterventionRequired`. Existing fixtures cover important examples, but they do
not prove every boolean combination. A future predicate change could preserve
the named examples while regressing an uncovered combination.

## Scope

- Add an XCTest truth table covering all 16 combinations of the four decision
  dimensions.
- Derive concrete `SCNetworkReachabilityFlags` inputs for each row while using a
  stable representative automatic flag.
- Assert the production decision rule: connectivity requires `Reachable`, must
  not require intervention, and when a connection is required it must be able
  to connect automatically.
- Keep the current production predicate, public API, deployment targets,
  dependencies, project structure, and existing focused fixtures unchanged.
- Add mutation-sensitive portable contracts and synchronized guidance.

## Files

- `NetworkStateTests/NetworkStateTests.swift`
- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-15-reachability-decision-truth-table.md`

## Verification

- Run the portable static iOS baseline through all standard Make aliases and
  from an external directory.
- On this Linux host, truthfully report Xcode/XCTest availability rather than
  claiming runtime execution.
- Reject isolated mutations for incomplete row coverage, incorrect expected
  logic, missing decision inputs, missing guidance, and stale plan status.
- Audit the exact diff, project/dependency drift, generated artifacts,
  credentials, conflicts, binaries, large files, modes, and whitespace.

## Risks

- Linux cannot execute the XCTest target; hosted macOS remains the runtime
  validation boundary.
- The truth table characterizes the existing synchronous default-route
  predicate and does not claim internet or service availability.
- This change must remain stacked on PR #10; neither pull request may be merged
  or closed without explicit owner authorization.

## Success Criteria

- Every combination of the four decision dimensions is represented exactly
  once and checked against the documented boolean rule.
- Existing focused flag fixtures remain intact and continue to pass the portable
  checker.
- No production, dependency, project, or workflow file changes are introduced.

## Work Completed

- Added a nested four-dimension XCTest matrix that constructs concrete
  reachability flags and checks all 16 combinations against the documented
  decision rule.
- Retained every existing focused fixture and left production code unchanged.
- Added mutation-sensitive portable contracts and synchronized guidance.

## Verification Completed

- All four Make gates passed from the repository and `make check` passed from
  an external directory.
- Seven isolated hostile mutations were rejected for incomplete dimensions,
  missing flag inputs, incorrect expected logic, weakened row count, missing
  guidance, and stale plan status.
- The exact seven-file implementation diff passed project/dependency,
  generated-artifact, credential, conflict, binary, large-file, mode,
  whitespace, and intended-path audits.
- `xcodebuild` and XCTest were unavailable on Linux; the portable static iOS
  baseline passed and no local runtime claim was made.
