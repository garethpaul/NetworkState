## Network State Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

Network State is a small iOS library that exposes a simple connectivity check
through `NetworkState.isConnectedToNetwork()`.

The repository is useful as a compact CocoaPod-style Swift utility with a
podspec, tests, and a build script. Usage details live in [`README.md`](README.md).

The goal is to keep the connectivity helper tiny, predictable, and easy to
consume.

The current focus is:

Priority:

- Preserve the public boolean connectivity API
- Keep podspec, Xcode project, and README usage aligned
- Maintain test coverage for the helper behavior
- Keep reachability flag evaluation covered by deterministic tests
- Keep snapshot acquisition failure covered without a live network dependency
- Keep automatic connection reachability flags covered without live network state
- Keep automatic connection behavior constrained so it requires the reachable flag
- Keep combined automatic connection flags covered in fixture tests
- Keep intervention-required handling scoped to connections that must first be
  established
- Keep the automatic intervention matrix across every automatic connection mode
- Keep the non-reachability flag guard around ancillary route flags
- Keep the WWAN reachability flag matrix around cellular routes
- Keep the reachability decision truth table exhaustive across decision flags
- Avoid growing the library beyond focused reachability utilities
- Keep `SystemConfiguration` checks local to the device
- Keep simulator verification independent of local signing identities by
  default
- Keep Xcode deployment targets aligned with the podspec's iOS 8.0 support
- Keep framework version alignment between the Info.plist and podspec metadata
- Keep the shared framework scheme available for the `NetworkState.framework`
  target
- Keep `make lint`, `make test`, `make build`, and `make check` wired to the
  SDK-free static baseline
- Keep hosted macOS project parsing pinned, read-only, and separate from the
  legacy simulator build
- Keep hosted source retrieval credential-free after checkout
- Keep the platform contract explicit: iOS 8.0 is a legacy package boundary,
  not a current-Xcode compatibility claim
- Keep reachability documented as a synchronous IPv4 default-route flag
  snapshot with no callback scheduling or observer lifecycle, rather than proof
  of internet or service availability
- Keep CocoaPods as the only declared package-manager integration until another
  manager is added and verified in a focused change
- Keep the historical 0.0.2 tag distinct from the current root podspec and
  default-branch source until a new immutable package release is prepared
- Keep connectivity evaluation local to the device with no remote probes,
  telemetry, or endpoint checks

Next priorities:

- Modernize Swift/project settings in a dedicated pass
- Add tests for offline, online, and constrained network cases where practical
- Run `pod spec lint NetworkState.podspec` on macOS before any package release

Contribution rules:

- One PR = one focused API, test, package, or documentation change.
- Keep the library lightweight.
- Run `make lint`, `make test`, `make build`, `make check`, and the build
  script or Xcode tests before pushing behavior changes.
- Preserve API compatibility for consumers where possible.
- Preserve reachability flag evaluation coverage when changing SystemConfiguration logic.
- Preserve automatic connection handling when changing reachability flags.
- Preserve the reachable flag requirement for automatic connection cases.
- Preserve combined automatic connection flags coverage when changing flag logic.
- Preserve intervention-required flag handling when changing reachability logic.
- Preserve the non-reachability flag guard when changing ancillary flag logic.
- Preserve the WWAN reachability flag matrix when changing cellular flag logic.
- Preserve deployment target alignment when changing package metadata.
- Preserve framework version alignment when changing release metadata.
- Preserve the shared framework scheme when changing Xcode project metadata.
- Preserve the `.explore/` local-intelligence ignore boundary and record
  durable maintenance decisions in tracked repository documents.

## Security

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Connectivity checks should not collect browsing or network traffic data. Future
changes should avoid telemetry and keep behavior local to the device.

## What We Will Not Merge (For Now)

- Network telemetry or analytics
- Broad networking frameworks unrelated to connectivity state
- API-breaking changes without migration notes
- Package metadata changes without verification

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
