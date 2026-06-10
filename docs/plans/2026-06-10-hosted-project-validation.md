# Hosted Project Validation

status: completed

## Context

The repository separates an SDK-free baseline from a legacy iPhone 5 simulator
build script. It has shared framework and test schemes, but no hosted validation
of the static contract or Xcode project parsing.

## Priorities

1. Run the canonical static gate on pinned macOS CI.
2. Parse `NetworkState.xcodeproj` and its shared schemes when Xcode is available.
3. Enforce a read-only, bounded workflow from the baseline checker.
4. Keep simulator execution, signing, CocoaPods publishing, and runtime network
   state outside hosted structural validation.

## Implementation Units

Files:

- `.github/workflows/check.yml`
- `scripts/check-baseline.py`
- `README.md`
- `VISION.md`
- `SECURITY.md`
- `CHANGES.md`

Add push, pull-request, and manual triggers; read-only permissions; concurrency
cancellation; a bounded `macos-15` job; commit-pinned checkout; and `make check`.
Require that contract and run `xcodebuild -list -project
NetworkState.xcodeproj` when Xcode exists.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- workflow YAML parse
- `git diff --check`
- successful hosted macOS `Check` workflow for the pushed commit

## Boundaries

- Do not run the obsolete iPhone 5 simulator build in hosted validation.
- Do not sign, publish a pod, or claim runtime connectivity coverage.
