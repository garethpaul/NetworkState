# Automatic Intervention Matrix

status: completed

## Context

The reachability predicate rejects user-intervention-required states, including
automatic connection modes. Existing XCTest coverage protects on-demand plus
intervention, but not on-traffic or the combined automatic flags. A future
condition refactor could therefore make one automatic mode report connectivity
while still requiring user action.

## Priorities

1. Cover on-demand, on-traffic, and combined automatic modes with intervention.
2. Require reachable and connection-required flags in each fixture.
3. Preserve the production predicate and public API unchanged.
4. Enforce the matrix through the portable static checker.

## Implementation Units

### XCTest Matrix

File: `NetworkStateTests/NetworkStateTests.swift`

Add a focused test asserting all three automatic-mode combinations remain
unreachable when `kSCNetworkFlagsInterventionRequired` is present.

### Static Contract And Documentation

Files:

- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-12-automatic-intervention-matrix.md`

Require the three fixtures, completed evidence, and synchronized reachability
documentation.

## Verification

Completed locally on 2026-06-12:

- `python3 -m py_compile scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- hostile mutations removing on-traffic or combined intervention coverage were
  each rejected by the static contract
- `git diff --check`

`xcodebuild` is unavailable on this Linux host, so XCTest was not executed
locally.

Completed on hosted macOS for implementation head
`70801c49325700194ab14fa3ea44a22c7747fc80`:

- push run `27397655613`: success
- pull-request run `27397656753`: success

## Boundaries

- Do not make live network requests or collect telemetry.
- Do not change the public API or production flag predicate.
- Do not claim XCTest execution without a compatible Xcode test environment.
