# Location-Independent NetworkState Verification

status: completed

## Context

The SDK-free Make aliases invoke `scripts/check-baseline.py` relative to the
caller's working directory. An absolute Makefile invocation from elsewhere can
therefore fail or inspect the wrong tree instead of this checkout.

## Objectives

- Resolve every Make alias from the checkout containing the loaded Makefile.
- Preserve the existing SDK-free target graph.
- Enforce the exact rooted recipe, operator guidance, completed status, and
  verification evidence in the active baseline checker.
- Prove root and external-directory behavior with mutation-sensitive checks.

## Implementation Units

### Make Contract

Files: `Makefile` and `scripts/check-baseline.py`.

Derive one absolute root from the loaded Makefile and invoke the checker by
absolute path. Require the complete small Makefile so aliases and path
resolution cannot drift independently.

### Documentation And Evidence

Files: `README.md`, `CHANGES.md`, and this plan.

Document absolute Makefile invocation and record bounded local and hostile
mutation verification after it completes.

## Boundaries

- Do not change Swift, Xcode project files, CocoaPods metadata, tests,
  workflows, or deployment targets.
- Do not run dependency installation, builds, signing, simulators, remote
  probes, or application execution.
- Preserve the existing stacked PR chain and exact-head evidence.

## Work Completed

- Rooted every SDK-free Make alias at the checkout containing the loaded
  Makefile while preserving the existing target graph.
- Added exact Makefile, README invocation, completed status, and verification
  evidence contracts to `scripts/check-baseline.py`.
- Documented absolute Makefile invocation without changing Swift, Xcode, or
  workflow behavior.

## Verification Completed

- Root and external-directory `lint`, `test`, `build`, `verify`, and `check`
  gates passed through the checkout's absolute Makefile path.
- `python3 -m py_compile scripts/check-baseline.py` and `git diff --check`
  passed.
- Five isolated hostile mutations covering root derivation, checker resolution,
  alias delegation, completed plan evidence, and README invocation guidance
  were rejected by the intended contracts.
- Intended-path, secret-pattern, conflict-marker, generated-artifact, Swift,
  Xcode project, CocoaPods, test, workflow, and credential-boundary audits
  passed.
