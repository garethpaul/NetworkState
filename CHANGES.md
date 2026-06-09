# Changes

## 2026-06-08

- Defaulted the Xcode build script to unsigned simulator validation through
  `CODE_SIGNING_ALLOWED=NO`.
- Added `make check` static verification for the legacy Swift framework baseline.
- Made the documented `NetworkState.isConnectedToNetwork()` helper public for framework consumers.
- Guarded reachability creation so an unexpected `SCNetworkReachabilityCreateWithAddress` failure returns `false` instead of crashing.
- Replaced placeholder XCTest methods with a smoke test for the public connectivity API.
- Parameterized `build.sh` with `PROJECT`, `SCHEME`, `DESTINATION`, and `SDK` environment overrides.
- Updated CocoaPods metadata URLs to HTTPS and documented `pod spec lint` verification.
- Added local secret/config ignore rules for Xcode and environment files.
