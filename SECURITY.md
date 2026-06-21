# Security Policy

## Supported Versions

The supported security scope for `NetworkState` is the current default branch, `master`. Older commits, tags, branches, forks, demos, and generated artifacts are not actively supported unless the repository explicitly marks them as maintained.

Project summary: SDK for Reachability

## Reporting a Vulnerability

Please report suspected vulnerabilities through GitHub's private vulnerability reporting or by opening a draft GitHub Security Advisory for `garethpaul/NetworkState` when that option is available. If GitHub does not show a private reporting option for this repository, contact the repository owner through GitHub and avoid posting exploit details publicly until the issue can be assessed.

Do not open a public issue that includes exploit code, secrets, personal data, or detailed reproduction steps for an unpatched vulnerability.

## What to Include

Helpful reports include:

- the affected file, endpoint, permission, dependency, or workflow
- a concise impact statement explaining what an attacker could do
- reproduction steps using test data and accounts you control
- the branch, commit SHA, platform version, device, runtime, or dependency versions used
- logs, screenshots, or proof-of-concept snippets that demonstrate impact without exposing private data

## Project Security Posture

- This repository appears to be an Apple platform application or Swift sample. The active security scope is the code and documentation on the default branch.
- The core code uses `SystemConfiguration` reachability. Connectivity checks should remain local to the device and should not collect telemetry, browsing data, endpoint history, or packet contents.
- Reachability must remain a local flag snapshot with no remote probes. A
  positive result must not be documented as proof of internet access, DNS,
  captive-portal completion, or availability of a specific service.
- The helper installs no reachability callback and owns no callback queue,
  observer, or teardown lifecycle; callers must request a fresh snapshot when
  their own application lifecycle requires one.
- Reachability flag evaluation should remain deterministic and covered without live network telemetry.
- Automatic connection reachability flags should be evaluated locally and covered without live network telemetry.
- Automatic connection handling should still require the reachable flag before reporting connectivity.
- Combined automatic connection flags should stay covered so on-demand and
  on-traffic states remain accepted together when reachable.
- The intervention-required flag should prevent connectivity from being
  reported only when a required connection still needs user action; it should
  not override an already established reachable route.
- The automatic intervention matrix should cover on-demand, on-traffic, and
  combined automatic modes with user intervention required.
- The non-reachability flag guard should ensure ancillary route flags cannot
  report connectivity without the `Reachable` bit.
- The WWAN reachability flag matrix should keep the cellular bit dependent on
  `Reachable` without rejecting valid reachable cellular routes.
- The reachability decision truth table should cover every boolean combination
  that controls the public flag evaluator.
- Review found network clients, sockets, web APIs, or service endpoints; changes in those areas should receive security-focused review before merge.
- Review found file, document, data, or media parsing flows; changes in those areas should receive security-focused review before merge.
- CocoaPods metadata lives in `NetworkState.podspec`. Run `make lint`,
  `make test`, `make build`, `make check`, and
  `pod spec lint NetworkState.podspec` before publishing package metadata
  changes.
- CocoaPods is the only declared package-manager integration. Swift Package
  Manager and Carthage support require separate metadata and verification
  before being advertised.
- The pinned macOS workflow runs static checks and project parsing without
  simulator execution, signing, pod publishing, or runtime connectivity checks.
- The Xcode project and podspec should stay aligned on iOS 8.0 support so consumers do not receive inconsistent package metadata.
- Framework version alignment should keep `NetworkState/Info.plist` and
  `NetworkState.podspec` on the same public version before package release.
- The shared framework scheme should keep the `NetworkState.framework` target
  available for direct Xcode builds alongside the test scheme.

## Mobile Privacy Notes

If this project requests device permissions such as location, camera, microphone, contacts, Bluetooth, health data, or local storage access, reports should describe the permission involved and whether sensitive data can be accessed, persisted, or transmitted unexpectedly. Please avoid testing against real third-party user data or accounts you do not control.

## Dependency and Supply Chain Security

Dependency updates should come from trusted package managers and should keep lockfiles in sync when lockfiles exist. Do not commit credentials, private keys, tokens, generated secrets, or machine-local configuration. If a vulnerability depends on a compromised package, typosquatting risk, insecure transitive dependency, or unsafe build step, include the package name, affected version, and the path through which it is used.

For this repository, keep signing identities, local xcconfig files, `.env`
files, and generated build products out of git. Preserve the shared framework
scheme when changing project metadata so package verification remains
repeatable.

The hosted gate uses a credential-free checkout so its read-only token is not
retained in the runner's Git configuration.

The hosted `baseline` job runs repository policy, Python tests, and the Xcode
project check directly before entering any mutable Make target. This prevents
duplicate `ROOT` assignments, recipe replacement, or caller shell settings from
claiming successful policy validation. Local Make aliases remain convenience
commands for the checked-in Makefile, not authority over arbitrary
caller-supplied Make programs. They pin `/bin/sh` and `/usr/bin/python3`, and
they fail closed for the reviewed fake `python3`, command-line and `MAKEFLAGS`
`SHELL`, `ROOT`, and `MAKEFILE_LIST` controls. Additional `-f` Makefiles are
caller-supplied Make programs outside the local Make trust boundary; the hosted
direct workflow remains authoritative for pull-request validation.

The workflow contract permits only the pinned checkout and exact validation
step, with no job/step environment, custom shell, extra step, or command
addition. Hosted Python, shell, and `xcodebuild` entrypoints use absolute system
paths so checked-in or `PATH`-injected replacements cannot claim success.

The workflow itself is pull-request editable. Branch protection must require
the GitHub Actions `baseline` context, and workflow changes require review as
changes to verification authority. Repository code cannot independently
guarantee those provider-side settings.

## Safe Research Guidelines

Good-faith research is welcome when it stays within these boundaries:

- use only accounts, devices, data, and infrastructure that you own or have explicit permission to test
- avoid destructive actions, persistence, spam, phishing, social engineering, or denial-of-service testing
- minimize access to personal data and stop testing immediately if private data is exposed
- do not exfiltrate secrets or third-party data; report the minimum evidence needed to verify impact
- keep vulnerability details confidential until the maintainer has assessed the report

## Maintainer Response

The maintainer will review complete reports as availability allows, prioritize issues by exploitability and impact, and coordinate a fix or mitigation when the affected code is still maintained. For sample, archived, or educational repositories, the likely remediation may be documentation, dependency updates, or clearly marking unsupported code rather than a production-style patch release.
