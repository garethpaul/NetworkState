# Automatic Reachability Flags Plan

status: completed

## Context

`SCNetworkReachabilityFlags` can include `ConnectionRequired` together with `ConnectionOnDemand` or `ConnectionOnTraffic`. When no user intervention is required, those automatic connection paths should still be considered reachable.

## Objectives

- Treat automatic connection flags as reachable when intervention is not required.
- Keep intervention-required paths reported as not reachable.
- Cover the behavior with deterministic flag fixture tests.
- Extend the static baseline and docs to preserve automatic connection handling.

## Verification

- `make check`
- `git diff --check`
