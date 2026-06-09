# Reachability Flag Evaluation

status: completed

## Context

`NetworkState.isConnectedToNetwork()` obtains SystemConfiguration reachability
flags and then decides whether the default route is usable. The public smoke
test only confirmed that the method returned a Boolean, so the flag evaluation
rules were not captured by fixture-style tests.

## Objectives

- Preserve the existing `isConnectedToNetwork()` public API.
- Extract the reachability flag decision into a small public helper.
- Cover reachable, connection-required, and unreachable flag combinations.
- Extend `make check` so future Swift changes preserve the helper and tests.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`

Xcode validation still requires macOS with a compatible simulator.
