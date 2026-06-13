---
title: Document platform and network assumptions
status: planned
date: 2026-06-13
---

# Document Platform And Network Assumptions

## Goal

Make the supported platform, packaging, and reachability semantics explicit
without changing the public `NetworkState.isConnectedToNetwork()` boolean API.

## Decisions

- Describe the helper as a synchronous snapshot of
  `SCNetworkReachability` flags for the IPv4 default route.
- State that a `true` result does not prove internet access, DNS resolution,
  captive-portal completion, or availability of a specific service.
- Preserve the current iOS 8.0 deployment target and legacy Swift/Xcode
  compatibility boundary instead of claiming support for current toolchains.
- Document CocoaPods as the only declared package-manager integration; Swift
  Package Manager and Carthage remain unsupported unless added in a separate
  reviewed change.
- Keep reachability checks local to the device and free of telemetry, request
  logging, or remote probes.

## Implementation Units

### Consumer documentation

Files: `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`

- Add a concise support and semantics section to the README.
- Align security and vision language with the same local-only, no-probe
  boundary.
- Record the documentation contract in the changelog and mark the vision item
  complete.

### Regression contract

Files: `scripts/check-baseline.py`

- Require the README to retain the default-route snapshot limitation, the
  non-guarantees for internet/service availability, the iOS 8.0 legacy
  boundary, and CocoaPods-only package support.
- Require security and vision documentation to retain the local-only/no-remote-
  probe boundary.
- Require this plan to record completed status and actual verification before
  the full gate can pass.

## Verification

- Run `make lint`, `make test`, `make build`, and `make check`.
- Run the checker from an external working directory.
- Parse Python and workflow YAML, then run `git diff --check`.
- Exercise hostile mutations that remove or weaken each documented assumption
  and confirm the static gate rejects them.
- Scan the intended diff for credential material and generated artifacts.

## Risks

- Documentation can overstate compatibility if it treats a metadata target as
  proof of current Xcode support; wording must remain explicitly legacy-aware.
- `SCNetworkReachability` flags are not a substitute for request-level error
  handling, so the README must avoid presenting the helper as an internet
  availability oracle.
