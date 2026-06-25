# Changes

## 2026-06-25 14:54 PDT - P2 - Ignore local repository intelligence

### Summary

Kept maintainer-local `.explore/` notes out of source-control status and
accidental pull-request changes while requiring durable decisions to remain in
tracked repository documents.

### Work completed

- Added the active `.explore/` directory pattern to `.gitignore`.
- Extended the canonical ignore contract and made it reject commented-out
  patterns or leading-whitespace lookalikes rather than accepting normalized
  raw substrings, then added an effective Git check for ordered negations.
- Rejected force-added or historical tracked `.explore` files through a pinned
  `git ls-files` query.
- Documented the local-only intelligence boundary in contributor, setup,
  roadmap, and implementation-plan guidance.

### Threads

- Started: local repository intelligence ignore boundary.
- Continued: canonical baseline ownership of local and generated artifacts.
- Stopped: none.

### Files changed

- `.gitignore` — ignored repository-local `.explore/` files.
- `scripts/check-baseline.py` — enforced active, non-comment ignore entries.
- `tests/test_baseline_contracts.py` — covered comments, leading whitespace,
  later negation behavior, and force-added tracked files.
- `README.md` — distinguished local notes from source and durable evidence.
- `AGENTS.md` — added the maintenance rule.
- `VISION.md` — added the contribution guardrail.
- `docs/plans/2026-06-25-local-intelligence-ignore.md` — recorded evidence,
  decisions, verification, and risk.
- `CHANGES.md` — recorded this P2 cycle.

### Validation

- Red-first baseline — failed with `.gitignore must include .explore/` before
  the active ignore rule was added.
- Red-first unit regression — failed because the active-pattern parser helper
  did not yet exist.
- Commented-rule hostile mutation — failed with the intended missing-pattern
  error after the active rule was temporarily commented out.
- All six Make aliases passed from the repository root and an external working
  directory; each run included the baseline and 13 Python policy tests.
- Direct Python discovery, syntax parsing, `git check-ignore`, and
  `git diff --check` passed.
- First exact-head Codex review — found that trimming leading whitespace could
  accept ` .explore/` even though Git would not apply it to `.explore/foo`.
- Review fix — preserve pattern bytes, ignore only actual comment lines, and
  cover the malformed leading-space rule in the permanent unit regression.
- Second exact-head Codex review — clean on
  `fddb68246ed08e5f342aeca2bba8cedc40a08941` with no actionable findings.
- CodeQL Actions and Python passed on the corrected exact head.
- The first pull-request macOS runner exposed no installed iOS simulator and
  failed before compilation; the duplicate exact-head push job passed the full
  framework build and XCTest suite, confirming runner-image variance.
- The authoritative pull-request job was rerun unchanged and passed the full
  baseline, 13 Python tests, framework build, and XCTest suite in 2m23s.
- Third exact-head Codex review — found that a later `!.explore/` rule could
  disable Git's ignore behavior while leaving the textual contract satisfied.
- Review fix — require pinned `git check-ignore --no-index` success for both
  the directory and a representative file, covering positive, negated, and
  selective child re-inclusion behavior.
- Fourth exact-head Codex review — found that `--no-index` intentionally masks
  force-added or historical tracked `.explore` files.
- Review fix — query the index with pinned `git ls-files`, fail closed on query
  errors, and reject every tracked local-intelligence path.

### Bugs / findings

- P2: persistent local intelligence appeared as untracked source in every
  checkout and could be staged or published accidentally.
- P2: the prior raw-substring ignore checker would accept a commented-out rule.
- P2: the first active-pattern parser normalized leading whitespace and could
  accept a rule that Git would not apply.
- P2: the textual contract did not account for ordered negation rules that can
  disable an earlier `.explore/` pattern.
- P2: effective ignore checks alone did not reject already tracked `.explore`
  files because `--no-index` intentionally ignores index state.

### Blockers

- Local Linux cannot run Xcode; hosted macOS remains authoritative for the
  framework build and XCTest truth table.

### Next action

- Rerun exact-head review and hosted checks for this evidence-only update, then
  merge if they remain clean.

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
- First exact-head Codex review — clean on
  `148459249eebc876cb0af121d2ef2c1d2615fd0e` with no actionable findings.
- First hosted pull-request run — macOS baseline, framework build, XCTest,
  CodeQL Actions, and CodeQL Python passed. A duplicate push-triggered baseline
  for the same head was canceled after the pull-request run became authoritative.
- Final-review finding — Codex identified that the stale-tag regex missed
  multiline `:tag =>` declarations and modern `tag:` Ruby hash syntax.
- Review fix — parse Ruby code blocks into `NetworkState` pod declarations,
  normalize declaration whitespace, and reject both tag syntaxes. Focused
  modern-hash and multiline mutations now fail for the stale-tag contract.
- Second review finding — the required negative trunk sentence could coexist
  with a contradictory availability claim or bare trunk-only Podfile entry.
- Second review fix — reject `NetworkState` pod declarations without an
  explicit Git source and scan outside the exact disclaimer for install,
  availability, or publication claims. Contradictory-text and bare-install
  mutations now fail for their intended trunk contracts.
- Third review finding — the phrase-specific trunk scan still missed common
  `available in` and `install via` wording.
- Third review fix — remove the one exact negative disclaimer and reject every
  remaining `CocoaPods trunk` mention, avoiding language-specific false
  negatives. Both newly identified wording variants now fail.
- Local Xcode remained unavailable and skipped truthfully. Merge remains
  conditional on clean exact-head review and successful final hosted reruns.

### Bugs / findings

- P2: consumers could reasonably treat root podspec version `0.0.2` as evidence
  that the same-named immutable tag contained the current implementation.

### Blockers

- Local Linux cannot run Xcode or CocoaPods lint; hosted macOS remains
  authoritative for the existing framework build and XCTest truth table.

### Next action

- Merge only after clean exact-head review and final hosted baseline and CodeQL
  success.

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
