# Framework Version Alignment

status: completed

## Context

`NetworkState.podspec` publishes version `0.0.2`, but the framework
`Info.plist` still reported `1.0` as its short version string. Consumers and
release tooling should not receive inconsistent package and bundle metadata.

## Objectives

- Keep `NetworkState/Info.plist` aligned with the podspec version.
- Preserve existing iOS 8.0 deployment target alignment.
- Extend the SDK-free static baseline and docs for framework version alignment.

## Verification

- `make check`
- `git diff --check`
