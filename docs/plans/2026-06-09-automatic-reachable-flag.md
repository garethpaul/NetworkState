# Automatic Reachable Flag Plan

status: completed

## Context

Automatic connection flags such as connection-on-demand can make a reachable
route usable without manual intervention. They should not, however, turn an
otherwise unreachable flag set into a connected state.

## Objectives

- Preserve the rule that automatic connection handling still requires the
  reachable flag.
- Add XCTest fixture coverage for connection-on-demand and connection-on-traffic
  combinations without the reachable flag.
- Extend static checks and docs so the reachability rule remains visible.

## Verification

- `make check`
- `git diff --check`
