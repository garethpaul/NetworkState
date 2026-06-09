# Combined Automatic Connection Flags

status: completed

## Context

The reachability evaluator accepts `ConnectionOnDemand` and
`ConnectionOnTraffic` when the base reachable flag is present, connection is
required, and no user intervention is required. Existing fixture tests covered
each automatic flag independently but not the combined state.

## Objectives

- Add deterministic XCTest coverage for reachable on-demand plus on-traffic
  flags together.
- Preserve the existing automatic-connection and intervention-required behavior.
- Extend the SDK-free static baseline and docs so the combined automatic state
  stays covered.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
