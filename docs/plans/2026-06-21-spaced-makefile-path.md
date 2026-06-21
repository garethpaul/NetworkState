# Spaced Absolute Makefile Path Verification

status: completed

## Context

GNU Make list functions split a loaded absolute Makefile path at spaces. A
checkout path containing spaces, brackets, and an apostrophe therefore sent
the SDK-free verifier to a fabricated caller path.

## Scope

1. Derive the checkout root from the complete `MAKEFILE_LIST` value.
2. Preserve the authoritative root against command-line and environment input.
3. Reject command-line or environment-preferred `MAKEFILE_LIST` overrides.
4. Exercise all six Make aliases from an external working directory.
5. Pin checked-in Make alias execution to `/bin/sh` and `/usr/bin/python3`.
6. Document that additional `-f` Makefiles are caller-supplied Make programs
   outside the local Make trust boundary, and that the hosted direct workflow
   remains authoritative.

## Verification

- Root and external hostile-path gates passed on Python 3.12 and 3.14.
- All six Make aliases retained the checkout with no override and with
  command-line or environment `ROOT` input.
- Both tested `MAKEFILE_LIST` override paths failed closed.
- Fake `python3` on `PATH` plus command-line and `MAKEFLAGS` `SHELL` controls
  were rejected across all six checked-in Make aliases.
- Static reachability, Xcode project, scheme, podspec, and workflow contracts
  remained green; no Apple build ran locally.

## Risk And Rollback

This changes SDK-free verification root discovery only. It does not alter the
Swift framework, reachability truth table, Xcode project, or build script.
