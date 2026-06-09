# Changes

## 2026-06-09

- Added `make lint`, `make test`, and `make build` aliases so standard local
  gates run the same SDK-free static baseline as `make check`.
- Aligned the framework Info.plist version with the podspec's `0.0.2` release
  metadata.
- Added combined automatic connection flags coverage so reachable on-demand and
  on-traffic states stay accepted together.

## 2026-06-08

- Defaulted the Xcode build script to unsigned simulator validation through
  `CODE_SIGNING_ALLOWED=NO`.
- Added `make check` static verification for the legacy Swift framework baseline.
- Made the documented `NetworkState.isConnectedToNetwork()` helper public for framework consumers.
- Guarded reachability creation so an unexpected `SCNetworkReachabilityCreateWithAddress` failure returns `false` instead of crashing.
- Added deterministic reachability flag evaluation coverage for reachable, connection-required, and unreachable states.
- Treated automatic connection reachability flags as reachable when no user intervention is required.
- Covered automatic connection flag combinations that still require the reachable flag.
- Rejected intervention-required flag combinations so user-action states do not
  report connectivity.
- Aligned Xcode deployment targets with the podspec's iOS 8.0 support claim.
- Replaced placeholder XCTest methods with a smoke test for the public connectivity API.
- Parameterized `build.sh` with `PROJECT`, `SCHEME`, `DESTINATION`, and `SDK` environment overrides.
- Updated CocoaPods metadata URLs to HTTPS and documented `pod spec lint` verification.
- Added local secret/config ignore rules for Xcode and environment files.
