# Intervention-Required Scope

Status: planned

## Problem

`NetworkState.isReachableWithFlags(_:)` currently treats
`InterventionRequired` as a global connectivity veto. Apple documents that flag
as describing manual action needed to establish a connection, alongside
`ConnectionRequired`. A route that is already reachable without establishing a
connection should therefore remain reachable even if a synthetic flag fixture
also contains `InterventionRequired`.

The exhaustive truth table currently repeats the production mistake in its
expected-value expression, so it cannot detect this boundary error.

## Scope

- Apply `InterventionRequired` only while evaluating an automatically
  established connection that is actually required.
- Correct the 16-row truth-table oracle independently of the production
  expression.
- Add a focused fixture for `Reachable | InterventionRequired` without
  `ConnectionRequired`.
- Strengthen the portable checker and synchronize user and maintainer guidance.
- Keep the public API, deployment targets, dependencies, project structure, and
  workflows unchanged.

## Files

- `NetworkState/NetworkState.swift`
- `NetworkStateTests/NetworkStateTests.swift`
- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-15-intervention-required-scope.md`

## Verification

- Run every standard Make alias and invoke the absolute Makefile from an
  external directory.
- On Linux, report Xcode/XCTest unavailability rather than claiming runtime
  execution.
- Reject isolated mutations that restore the global intervention veto, weaken
  the focused fixture or truth-table oracle, remove guidance, or reopen the
  completed plan.
- Audit the exact diff, generated artifacts, credentials, conflicts, binaries,
  large files, modes, whitespace, and project/dependency drift.

## Risks

- Linux cannot execute XCTest; hosted macOS remains the runtime validation
  boundary.
- The corrected case is an unusual synthetic flag combination, but accepting it
  follows the documented relationship between connection-required and
  intervention-required state.
- This change must remain stacked on PR #11, and no pull request may be merged
  or closed without explicit owner authorization.

## Success Criteria

- `Reachable | InterventionRequired` remains reachable when no connection must
  first be established.
- A required connection remains unreachable when manual intervention is needed.
- The exhaustive truth table and focused fixtures independently enforce both
  sides of that boundary.
