# Network State Baseline Plan

status: completed

## Context

`NetworkState` is a small Swift framework that wraps SystemConfiguration
reachability as `NetworkState.isConnectedToNetwork()`.

## Risks

- The documented helper was not public even though the class was public.
- Reachability creation used a force unwrap, so an unexpected nil result could
  crash callers instead of reporting disconnected state.
- XCTest coverage still contained generated placeholder methods.
- `build.sh` hard-coded its Xcode destination and had no host-portable static
  verification path.
- CocoaPods metadata included a non-HTTPS social URL.

## Work Completed

- Made `isConnectedToNetwork()` public and guarded reachability creation.
- Replaced placeholder XCTest methods with a smoke test for the public API.
- Parameterized the Xcode build script through environment variables.
- Added `Makefile`, `scripts/check-baseline.py`, and Travis static-check coverage.
- Updated docs, local ignore rules, and podspec URL hygiene.

## Verification

- `make check`
- `git diff --check`

Xcode is not available on this Linux host, so `./build.sh` and
`pod spec lint NetworkState.podspec` still need to run on macOS with Xcode and
CocoaPods when release validation is required.
