# Podspec Deployment Target Alignment

status: completed

## Context

`NetworkState.podspec` declares iOS 8.0 support, while the checked-in Xcode
project used newer iOS deployment targets in project and test settings. That
can mislead CocoaPods consumers and make local project validation diverge from
the package metadata.

## Objectives

- Keep the podspec's iOS 8.0 support claim unchanged.
- Align Xcode project deployment target settings with the podspec.
- Extend static checks so future project edits do not reintroduce stale iOS 9.x
  deployment targets.
- Document the package metadata alignment rule for maintainers.

## Verification

- `make check`
- `git diff --check`

Xcode and CocoaPods are not installed on this Linux host, so `./build.sh` and
`pod spec lint NetworkState.podspec` still need macOS verification before a
package release.
