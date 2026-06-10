# Shared Framework Scheme Guard

status: completed

## Context

The repository ships shared Xcode schemes for both the framework and the test
bundle. The static baseline already guards the test scheme because `build.sh`
uses it, but direct Xcode consumers also need the shared `NetworkState` scheme
to continue building `NetworkState.framework`.

## Objectives

- Require the shared `NetworkState.xcscheme` in the static baseline.
- Verify the shared framework scheme points at `NetworkState.framework`.
- Keep the shared scheme parseable as XML alongside the test scheme.
- Extend docs and baseline checks for the shared framework scheme guard.

## Verification

- `scripts/check-baseline.py`
- `make check`
- `git diff --check`
