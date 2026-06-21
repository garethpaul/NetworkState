# NetworkState Contributor Guide

## Scope

This repository maintains a small Swift wrapper around legacy
`SCNetworkReachability` flag snapshots.

## Verification

- Run `make check` for dependency-free repository contracts.
- Run `./build.sh` on macOS to compile and execute the XCTest truth table.
- Override `DESTINATION`, `SWIFT_VERSION`, or `IPHONEOS_DEPLOYMENT_TARGET` when
  validating with a different installed Xcode toolchain.
- Treat Make aliases as convenience wrappers. The hosted direct chain remains
  the pull-request authority, and local Make must fail closed for fake
  `python3`, caller `SHELL`, and additional `-f` Makefile controls.

## Reachability Rules

- Require the `Reachable` flag for every positive result.
- Treat `ConnectionRequired` as unavailable unless on-demand or on-traffic can
  establish the connection without user intervention.
- Do not let transient, local, direct, or WWAN flags create reachability alone.
- Guard WWAN-only constants to iOS-family builds.
- Describe results as local route reachability, never proof of internet or
  service availability.

## Maintenance

- Preserve the public Boolean API and fixture evaluator unless a reviewed
  compatibility change explicitly replaces them.
- Keep checkout credentials disabled and the single hosted workflow intact.
- Record skipped device, carrier, captive-portal, and live-service validation.
