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
- Keep automatic connection reachability flags covered without live network state
- Avoid growing the library beyond focused reachability utilities
- Keep `SystemConfiguration` checks local to the device
- Keep simulator verification independent of local signing identities by
  default

Next priorities:

- Document platform and network-framework assumptions
- Modernize Swift/project settings in a dedicated pass
- Add tests for offline, online, and constrained network cases where practical
- Clarify package-manager support if revived
- Run `pod spec lint NetworkState.podspec` on macOS before any package release

Contribution rules:

- One PR = one focused API, test, package, or documentation change.
- Keep the library lightweight.
- Run `make check` and the build script or Xcode tests before pushing behavior changes.
- Preserve API compatibility for consumers where possible.
- Preserve reachability flag evaluation coverage when changing SystemConfiguration logic.
- Preserve automatic connection handling when changing reachability flags.

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
