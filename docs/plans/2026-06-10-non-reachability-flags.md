# Non-Reachability Flag Guard

status: completed

## Problem

The reachability evaluator has deterministic coverage for connection-required,
automatic, combined, and intervention flags, but not for ancillary flags such
as transient connection, local address, and direct route. Those bits must not
create connectivity when the `Reachable` bit is absent.

## Scope

- Cover transient, local-address, and direct-route flags without `Reachable`.
- Confirm those ancillary flags do not suppress a valid reachable state.
- Keep production reachability derived from `kSCNetworkFlagsReachable`.
- Add static mutation guardrails without depending on live network state.
- Document the fixture coverage across project guidance.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- mutate reachable-bit evaluation and require the baseline to fail
- `git diff --check`

## Work Completed

- Added fixture coverage for transient, local-address, and direct-route flags.
- Verified ancillary flags remain false without `Reachable` and true when
  combined with a valid reachable state.
- Added a static assertion tying production evaluation to the actual
  `kSCNetworkFlagsReachable` bit.
- Documented the ancillary flag contract in project and security guidance.
