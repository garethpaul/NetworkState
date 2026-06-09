# Make Gate Aliases

status: completed

## Context

The repository had a working `make check` static baseline, but the shared
maintenance workflow also runs `make lint`, `make test`, and `make build` before
pushes. Those commands should reach the same SDK-free verifier on hosts without
Xcode.

## Completed Scope

- Added `lint`, `test`, `build`, and `verify` Make targets that delegate to the
  static baseline.
- Extended `scripts/check-baseline.py` so the gate aliases remain present.
- Updated README, VISION, SECURITY, and CHANGES with the standard local gate
  contract.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
