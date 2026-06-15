# WWAN Reachability Flag Matrix

status: in progress

## Problem

The fixture matrix proves transient, local-address, and direct-route flags
cannot create connectivity, but it omits the iOS-specific
`kSCNetworkFlagsIsWWAN` bit. Cellular reachability commonly includes that flag,
so a predicate refactor could accidentally treat WWAN as sufficient or reject a
valid reachable cellular route without a focused regression.

## Scope

- Prove WWAN alone remains unreachable.
- Prove `Reachable | IsWWAN` remains reachable.
- Preserve the production predicate, public API, automatic-connection matrix,
  deployment target, framework metadata, and package support.
- Add mutation-sensitive static contracts and synchronized guidance.

## Implementation

1. Add a focused XCTest fixture for WWAN with and without `Reachable`.
2. Require both assertions and the iOS flag constant in the portable checker.
3. Record the cellular flag matrix in project maintenance documentation.

## Verification

- Run checker compilation and every Make gate from the repository plus the
  canonical gate from an external directory with explicit timeouts.
- Reject isolated mutations that remove the WWAN constant, remove either
  assertion, invert an assertion, remove guidance, or leave the plan incomplete.
- Audit the exact diff, generated artifacts, credential patterns, Xcode project
  integrity, conflict markers, binaries, large files, and intended paths.

## Risks

- Xcode and XCTest execution require a compatible macOS toolchain; Linux can
  validate only the dependency-free source contract.
- This remains a local SystemConfiguration flag snapshot, not proof of internet
  access or availability of any remote service.
- The stacked base pull request must remain available and merge first.
