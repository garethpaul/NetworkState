# AGENTS.md

## Repository purpose

`garethpaul/NetworkState` is a small Swift framework that wraps SystemConfiguration reachability as `NetworkState.isConnectedToNetwork()`.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `NetworkState.xcodeproj` - Xcode project
- `NetworkState` - repository source or sample assets
- `NetworkStateTests` - repository source or sample assets

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Local Apple development: `open NetworkState.xcodeproj`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Swift (2), C/C++ headers (1), shell (1).
- Preserve legacy Xcode project settings and signing assumptions unless the change is explicitly about modernization.

## Testing guidance

- Test-related files detected: `docs/plans/2026-06-09-podspec-deployment-target-alignment.md`, `NetworkState.podspec`, `NetworkState.xcodeproj/xcshareddata/xcschemes/NetworkStateTests.xcscheme`, `NetworkStateTests/NetworkStateTests.swift`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- No required secret or credential file was identified in the repository scan.
- Keep signing identities, local xcconfig files, environment files, and generated build output out of git.
- The library uses `SystemConfiguration` reachability and should keep checks local to the device.
- Reachability flag evaluation should remain covered by fixture-style tests rather than relying only on live network state.
- Automatic connection reachability flags should stay covered so connection-on-demand paths do not report false negatives.
- Automatic connection behavior should keep the rule that it requires the reachable flag.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
