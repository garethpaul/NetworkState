# Unsigned Build Default

status: completed

## Context

`build.sh` is the maintained Xcode verification path, but it only passes the
project, scheme, destination, and SDK values to `xcodebuild`. Simulator
validation should not depend on a developer's local signing identity or
provisioning profile state.

## Completed Scope

- Added a `CODE_SIGNING_ALLOWED` environment override that defaults to `NO`.
- Passed the signing setting through the build/test invocation.
- Extended static checks and documentation so the unsigned simulator build
  contract stays visible.

## Verification

- `make check`
- `git diff --check`

Xcode validation still requires macOS with a compatible simulator.
