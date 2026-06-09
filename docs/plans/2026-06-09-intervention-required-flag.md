# Intervention-Required Flag

status: completed

## Context

`NetworkState.isReachableWithFlags` already treats automatic connection flags as
reachable only when user intervention is not required. A flag set containing the
base reachable flag plus `kSCNetworkFlagsInterventionRequired` could still
report connectivity when no automatic-connection bit was present.

## Objectives

- Reject intervention-required reachability states before reporting connected.
- Preserve automatic connection behavior when no user intervention is required.
- Add deterministic fixture coverage for intervention-required flags.
- Extend the static baseline and docs for the intervention-required flag rule.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
