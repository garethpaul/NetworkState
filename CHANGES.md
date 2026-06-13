# Changes

## 2026-06-13

- Made every SDK-free Make alias resolve the static checker from the checkout
  when the Makefile is invoked by absolute path.
- Documented the synchronous IPv4 default-route reachability semantics, the
  request-level failures callers must still handle, the legacy iOS 8.0
  compatibility boundary, and CocoaPods-only package support.
- Enforced the local-only, no-remote-probe documentation contract in the static
  baseline.

## 2026-06-12

- Disabled persisted checkout credentials and enforced the sole pinned
  credential-free workflow boundary.

## 2026-06-10

- Added an automatic intervention matrix covering on-demand, on-traffic, and
  combined automatic connection flags while user action is required.
- Added a non-reachability flag guard covering transient, local-address, and
  direct-route bits with and without the `Reachable` flag.
- Added pinned, read-only macOS hosted validation for the SDK-free baseline and
  `NetworkState.xcodeproj` parsing.
- Added a shared framework scheme guard so the static baseline catches Xcode
  project changes that stop exposing `NetworkState.framework` directly.

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
