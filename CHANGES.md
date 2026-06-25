# Changes

## 2026-06-25 12:12 PDT - P2 - Clarify current CocoaPods source

### Summary

Documented that the checked-in root podspec describes current default-branch
source while the historical `0.0.2` tag still resolves the original 2016 Swift
implementation.

### Work completed

- Added a current-branch Git Podfile example without claiming CocoaPods trunk
  publication.
- Added reviewed-commit pinning guidance for reproducible builds.
- Added exact positive and stale-tag regression contracts plus maintenance and
  roadmap boundaries.

### Threads

- Started: none; the package-source documentation gap was completed directly.
- Continued: none.
- Stopped: none.

### Files changed

- `README.md` — added current source, stale-tag, trunk, and pinning guidance.
- `scripts/check-baseline.py` — enforced the exact package-source boundary.
- `AGENTS.md` — recorded the historical-tag maintenance rule.
- `VISION.md` — recorded the package release boundary.
- `docs/plans/2026-06-25-cocoapods-source-boundary.md` — recorded evidence,
  scope, and verification.

### Validation

- Initial baseline check — failed on the missing plan.
- Second red baseline check — after adding scope evidence, reported five missing
  README fragments plus incomplete verification evidence.
- First green attempt — exposed an overbroad stale-tag check that also rejected
  explanatory prose; narrowed it to actual `pod 'NetworkState'` tag syntax.
- Three hostile mutations — stale tag, CocoaPods trunk overclaim, and weakened
  reviewed-commit guidance were rejected for the intended contract failures.
- The first pinning mutation command allowed shell backtick substitution and
  failed for the wrong reason; the safely quoted rerun passed the intended
  rejection assertion.
- All six Make aliases passed from the repository root and an external working
  directory; each run included the baseline and all 12 Python policy tests.
- Python bytecode compilation and `git diff --check` passed. Validation-created
  bytecode plus the empty file produced by the misquoted mutation command were
  removed before review.
- Local Xcode remained unavailable and skipped truthfully. Hosted Xcode tests
  and exact-head review remain pending.

### Bugs / findings

- P2: consumers could reasonably treat root podspec version `0.0.2` as evidence
  that the same-named immutable tag contained the current implementation.

### Blockers

- Local Linux cannot run Xcode or CocoaPods lint; hosted macOS remains
  authoritative for the existing framework build and XCTest truth table.

### Next action

- Open the pull request, run exact-head review, and require hosted baseline and
  Xcode success before merge.

## 2026-06-21

- Preserved the complete checkout root for absolute Makefile paths containing
  spaces, brackets, or apostrophes, and rejected `MAKEFILE_LIST` overrides.
- Hardened every checked-in public Make alias with `/bin/sh` and
  `/usr/bin/python3`, while documenting that additional `-f` Makefiles are
  caller-supplied Make programs outside the local Make trust boundary.
- Added three SDK-free regression tests across all six Make aliases.
- Moved the hosted policy, Python test, and Xcode project bootstrap outside
  mutable Make target, `ROOT`, and shell authority, with hostile hosted-equivalent
  regression coverage and an explicit required-context trust boundary.
- Required the exact hosted workflow and absolute Python, shell, and Xcode tool
  paths, rejecting environment, step, shell, command, and fake-tool shadowing.
- Isolated local and hosted Python from `PYTHONPATH`, user-site startup code,
  and bytecode writes so injected startup modules cannot claim successful gates.

## 2026-06-19

- Made the reachability truth table executable on current Xcode while retaining
  the legacy Boolean API and iOS 8 package declaration.
- Expanded automatic-mode coverage to distinguish on-demand, on-traffic, and
  combined flags across all 32 core decision rows.
- Added repository ownership guidance and a credential-free hosted native gate.

## 2026-06-15

- Added a WWAN reachability flag matrix covering the cellular bit with and
  without the required `Reachable` flag.
- Added a reachability decision truth table for the flags that control the
  public evaluator.
- Scoped intervention-required handling to connections that must first be
  established, preserving already reachable routes that need no connection.

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
