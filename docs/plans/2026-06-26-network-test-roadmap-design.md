# Network Test Roadmap Reconciliation Design

## Context

The roadmap still asks for offline, online, and constrained-network tests. The
merged deterministic snapshot seam now covers unavailable (`nil` and empty
flags) and reachable flag snapshots without depending on the host network.

Apple documents `SCNetworkReachabilityFlags` as route-reachability,
connection-establishment, intervention, local/direct, and WWAN flags. It does
not expose Low Data Mode or a constrained-path property. Apple exposes that
property through Network framework path APIs instead:

- <https://developer.apple.com/documentation/systemconfiguration/scnetworkreachabilityflags>
- <https://developer.apple.com/documentation/network/3131049-nw_path_is_constrained>

## Options Considered

1. Keep the stale roadmap item. This understates completed deterministic
   coverage and suggests a constrained flag can be added to the current API.
2. Add Network framework monitoring now. This expands the public and lifecycle
   surface, conflicts with the iOS 8 compatibility boundary, and is not needed
   to validate the current synchronous Boolean helper.
3. Reconcile documentation and contracts. Mark offline/online snapshot coverage
   complete, document that constrained paths require a separately reviewed
   Network framework migration, and preserve current behavior.

## Decision

Use option 3. Do not change Swift code, public API, deployment targets, or
package metadata. Add an exact documentation contract across contributor,
README, security, roadmap, history, and a completed implementation plan.

## Verification

- Add the static contract first and observe it fail against stale guidance.
- Update the required documents and mark the implementation plan completed.
- Mutate the roadmap retirement, constrained-framework boundary, and completed
  plan in isolated copies; each mutation must fail.
- Run every Make alias from repository and external directories, plus hosted
  Xcode and CodeQL on the exact PR head.
