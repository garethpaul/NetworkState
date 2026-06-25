#!/usr/bin/env python3
"""Static baseline checks for the legacy NetworkState Swift framework."""

from pathlib import Path
import os
import plistlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MAKEFILE = """override SHELL := /bin/sh
override .SHELLFLAGS := -eu -c
override HASH := \\#

ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override MAKEFILE_PATH := $(shell path='$(subst ','"'"',$(MAKEFILE_LIST))'; first=$${path%"$${path$(HASH)?}"}; if [ "$$first" = " " ]; then path=$${path$(HASH)?}; fi; if [ -f "$$path" ]; then printf '%s\\n' "$$path"; fi)
ifeq ($(MAKEFILE_PATH),)
$(error this Makefile must be invoked directly as the checked-in Makefile)
endif
override ROOT := $(shell path='$(subst ','"'"',$(MAKEFILE_PATH))'; root=$${path%/*}; if [ "$$root" = "$$path" ]; then root=.; fi; if [ -z "$$root" ]; then root=/; fi; printf '%s\\n' "$$root")

.PHONY: build check lint static-check test verify

check: verify

lint test build verify: static-check

static-check:
\t/usr/bin/python3 -I -B "$(ROOT)/scripts/check-baseline.py"
\t/usr/bin/python3 -I -B -m unittest discover -s "$(ROOT)/tests" -p 'test_*.py'
"""
EXPECTED_WORKFLOW = """name: Check
on:
  pull_request:
  push:
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: check-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  baseline:
    runs-on: macos-15
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10
        with:
          persist-credentials: false
      - run: |
          /usr/bin/python3 -I -B scripts/check-baseline.py
          /usr/bin/python3 -I -B -m unittest discover -s tests -p 'test_*.py'
          /bin/sh ./build.sh
"""
REQUIRED = [
    ".gitignore",
    ".github/CODEOWNERS",
    ".github/workflows/check.yml",
    ".travis.yml",
    "AGENTS.md",
    "CHANGES.md",
    "Makefile",
    "NetworkState.podspec",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    "build.sh",
    "NetworkState/NetworkState.swift",
    "NetworkState/Info.plist",
    "NetworkStateTests/NetworkStateTests.swift",
    "NetworkStateTests/Info.plist",
    "NetworkState.xcodeproj/project.pbxproj",
    "NetworkState.xcodeproj/xcshareddata/xcschemes/NetworkState.xcscheme",
    "NetworkState.xcodeproj/xcshareddata/xcschemes/NetworkStateTests.xcscheme",
    "docs/plans/2026-06-08-network-state-baseline.md",
    "docs/plans/2026-06-09-unsigned-build-default.md",
    "docs/plans/2026-06-09-reachability-flag-evaluation.md",
    "docs/plans/2026-06-09-automatic-reachability-flags.md",
    "docs/plans/2026-06-09-automatic-reachable-flag.md",
    "docs/plans/2026-06-09-podspec-deployment-target-alignment.md",
    "docs/plans/2026-06-09-intervention-required-flag.md",
    "docs/plans/2026-06-09-make-gate-aliases.md",
    "docs/plans/2026-06-09-framework-version-alignment.md",
    "docs/plans/2026-06-09-combined-automatic-flags.md",
    "docs/plans/2026-06-10-shared-framework-scheme-guard.md",
    "docs/plans/2026-06-10-non-reachability-flags.md",
    "docs/plans/2026-06-10-hosted-project-validation.md",
    "docs/plans/2026-06-12-automatic-intervention-matrix.md",
    "docs/plans/2026-06-12-checkout-credential-boundary.md",
    "docs/plans/2026-06-13-platform-network-assumptions.md",
    "docs/plans/2026-06-13-location-independent-make.md",
    "docs/plans/2026-06-15-reachability-decision-truth-table.md",
    "docs/plans/2026-06-15-wwan-reachability-flag-matrix.md",
    "docs/plans/2026-06-21-spaced-makefile-path.md",
    "docs/plans/2026-06-25-cocoapods-source-boundary.md",
    "docs/plans/2026-06-25-local-intelligence-ignore.md",
    "docs/readme-overview.svg",
    "tests/test_baseline_contracts.py",
    "tests/test_makefile_root.py",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def active_gitignore_patterns(source: str) -> set[str]:
    return {
        line
        for line in source.splitlines()
        if line and not line.startswith("#")
    }


def git_ignores(root: Path, path: str) -> bool:
    result = subprocess.run(
        ["/usr/bin/git", "check-ignore", "--quiet", "--no-index", path],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    failures = []
    for path in REQUIRED:
        if not (ROOT / path).is_file():
            failures.append(f"required file missing: {path}")

    swift = read("NetworkState/NetworkState.swift")
    if "public class func isConnectedToNetwork() -> Bool" not in swift:
        failures.append("isConnectedToNetwork must be public for framework consumers")
    if "guard let reachability = defaultRouteReachability" not in swift:
        failures.append("reachability creation must be guarded")
    if "defaultRouteReachability!" in swift:
        failures.append("reachability must not be force-unwrapped")
    if "public class func isReachableWithFlags(_ flags: SCNetworkReachabilityFlags) -> Bool" not in swift:
        failures.append("reachability flag evaluation must be exposed for fixture tests")
    if "return isReachableWithFlags(flags)" not in swift:
        failures.append("isConnectedToNetwork must use the shared flag evaluator")
    for phrase in [
        "canConnectAutomatically",
        "flags.contains(.connectionOnDemand)",
        "flags.contains(.connectionOnTraffic)",
        "flags.contains(.interventionRequired)",
    ]:
        if phrase not in swift:
            failures.append(f"reachability flag evaluation must handle {phrase}")
    if "return isReachable &&" not in swift:
        failures.append("automatic reachability handling must still require the reachable flag")
    if "return isReachable && (!needsConnection || canConnectWithoutUserInteraction)" not in swift:
        failures.append("reachability evaluation must scope intervention to required connections")
    if "return isReachable && !interventionRequired" in swift:
        failures.append("reachability evaluation must not apply intervention as a global veto")
    if "flags.contains(.reachable)" not in swift:
        failures.append("reachability evaluation must derive connectivity from the Reachable flag")

    tests = read("NetworkStateTests/NetworkStateTests.swift")
    if "import NetworkState" not in tests:
        failures.append("tests must import the framework module")
    if "NetworkState.isConnectedToNetwork()" not in tests:
        failures.append("tests must exercise the public connectivity API")
    if "testReachabilityFlagEvaluation" not in tests or "isReachableWithFlags" not in tests:
        failures.append("tests must cover reachability flag evaluation")
    if "testReachabilityFlagEvaluationAllowsAutomaticConnection" not in tests:
        failures.append("tests must cover automatic reachability connection flags")
    if "testAutomaticConnectionStillRequiresReachableFlag" not in tests:
        failures.append("tests must cover automatic connection flags without the reachable flag")
    if "testCombinedAutomaticConnectionFlagsAreReachable" not in tests:
        failures.append("tests must cover combined automatic connection reachability flags")
    established_intervention_test = tests.split("func testInterventionRequiredDoesNotBlockEstablishedReachability()", 1)[-1].split("\n    func ", 1)[0]
    if (
        "func testInterventionRequiredDoesNotBlockEstablishedReachability()" not in tests
        or "reachable | interventionRequired" not in established_intervention_test
        or established_intervention_test.count("XCTAssertTrue") != 1
        or "XCTAssertFalse" in established_intervention_test
    ):
        failures.append("tests must keep established reachability independent of intervention state")
    automatic_intervention_test = tests.split("func testAutomaticConnectionModesRequireNoUserIntervention()", 1)[-1].split("func testNonReachabilityFlagsDoNotCreateConnectivity()", 1)[0]
    if (
        "func testAutomaticConnectionModesRequireNoUserIntervention()" not in tests
        or "requiredFlags | connectionOnDemand" not in automatic_intervention_test
        or "requiredFlags | connectionOnTraffic" not in automatic_intervention_test
        or "requiredFlags | connectionOnDemand | connectionOnTraffic" not in automatic_intervention_test
        or automatic_intervention_test.count("XCTAssertFalse") != 3
    ):
        failures.append("tests must cover intervention across every automatic connection mode")
    if (
        "testNonReachabilityFlagsDoNotCreateConnectivity" not in tests
        or "SCNetworkReachabilityFlags.transientConnection.rawValue" not in tests
        or "SCNetworkReachabilityFlags.isLocalAddress.rawValue" not in tests
        or "SCNetworkReachabilityFlags.isDirect.rawValue" not in tests
    ):
        failures.append("tests must cover ancillary flags with and without the Reachable flag")
    wwan_test = tests.split("func testWWANFlagRequiresReachableBaseFlag()", 1)[-1].split("\n    func ", 1)[0]
    if (
        "func testWWANFlagRequiresReachableBaseFlag()" not in tests
        or "#if os(iOS)" not in wwan_test
        or "SCNetworkReachabilityFlags.isWWAN.rawValue" not in wwan_test
        or "XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: wwan)))" not in wwan_test
        or "XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | wwan)))" not in wwan_test
        or wwan_test.count("XCTAssertFalse") != 1
        or wwan_test.count("XCTAssertTrue") != 1
    ):
        failures.append("tests must cover WWAN reachability with and without the Reachable flag")
    truth_table_test = tests.split("func testReachabilityDecisionTruthTable()", 1)[-1].split("\n    func ", 1)[0]
    if (
        "func testReachabilityDecisionTruthTable()" not in tests
        or "let booleanValues = [false, true]" not in truth_table_test
        or truth_table_test.count("for ") != 5
        or "for isReachable in booleanValues" not in truth_table_test
        or "for connectionRequired in booleanValues" not in truth_table_test
        or "for connectionOnDemand in booleanValues" not in truth_table_test
        or "for connectionOnTraffic in booleanValues" not in truth_table_test
        or "for interventionRequired in booleanValues" not in truth_table_test
        or "SCNetworkReachabilityFlags.reachable.rawValue" not in truth_table_test
        or "SCNetworkReachabilityFlags.connectionRequired.rawValue" not in truth_table_test
        or "SCNetworkReachabilityFlags.connectionOnDemand.rawValue" not in truth_table_test
        or "SCNetworkReachabilityFlags.connectionOnTraffic.rawValue" not in truth_table_test
        or "SCNetworkReachabilityFlags.interventionRequired.rawValue" not in truth_table_test
        or "let canConnectAutomatically = connectionOnDemand || connectionOnTraffic" not in truth_table_test
        or "let expected = isReachable &&" not in truth_table_test
        or "(!connectionRequired || (canConnectAutomatically && !interventionRequired))" not in truth_table_test
        or "XCTAssertEqual(coveredRows, 32)" not in truth_table_test
    ):
        failures.append("tests must cover the complete reachability decision truth table")
    if "testExample" in tests or "testPerformanceExample" in tests:
        failures.append("placeholder XCTest methods must be replaced")

    build = read("build.sh")
    for phrase in ["PROJECT=${PROJECT:-NetworkState.xcodeproj}", "SCHEME=${SCHEME:-NetworkStateTests}", "DESTINATION=${DESTINATION:-", "SWIFT_VERSION=${SWIFT_VERSION:-5.0}", "IPHONEOS_DEPLOYMENT_TARGET=${IPHONEOS_DEPLOYMENT_TARGET:-12.0}", "CODE_SIGNING_ALLOWED=${CODE_SIGNING_ALLOWED:-NO}", "XCODEBUILD=/usr/bin/xcodebuild", '[ ! -x "$XCODEBUILD" ]', 'SWIFT_VERSION="${SWIFT_VERSION}"', 'IPHONEOS_DEPLOYMENT_TARGET="${IPHONEOS_DEPLOYMENT_TARGET}"', 'CODE_SIGNING_ALLOWED="${CODE_SIGNING_ALLOWED}"']:
        if phrase not in build:
            failures.append(f"build.sh must include {phrase}")
    if "function " in build:
        failures.append("build.sh must use POSIX shell function syntax or no shell functions")

    makefile = read("Makefile")
    if makefile != EXPECTED_MAKEFILE:
        failures.append("Makefile must exactly preserve rooted SDK-free aliases")

    podspec = read("NetworkState.podspec")
    podspec_version_match = re.search(r's\.version\s*=\s*"([^"]+)"', podspec)
    podspec_version = podspec_version_match.group(1) if podspec_version_match else None
    if podspec_version is None:
        failures.append("podspec must keep the current published version visible")
    for phrase in ['s.framework  = "SystemConfiguration"', 's.source_files = "NetworkState/*.{swift}"', 's.social_media_url   = "https://twitter.com/gpj"']:
        if phrase not in podspec:
            failures.append(f"podspec must include {phrase}")
    if 's.platform     = :ios, "8.0"' not in podspec:
        failures.append("podspec must declare the maintained iOS 8.0 deployment target")
    if "http://twitter.com" in podspec or "http://docs.cocoapods.org" in podspec:
        failures.append("podspec metadata should use HTTPS URLs")

    project = read("NetworkState.xcodeproj/project.pbxproj")
    if project.count("IPHONEOS_DEPLOYMENT_TARGET = 8.0;") < 4:
        failures.append("Xcode project deployment targets must align with the podspec's iOS 8.0 support")
    for stale_target in ["IPHONEOS_DEPLOYMENT_TARGET = 9.2;", "IPHONEOS_DEPLOYMENT_TARGET = 9.3;"]:
        if stale_target in project:
            failures.append(f"Xcode project must not retain stale deployment target {stale_target}")

    travis = read(".travis.yml")
    if "- make check" not in travis or "- ./build.sh" not in travis:
        failures.append(".travis.yml must run static checks before the Xcode build")

    framework_scheme = read("NetworkState.xcodeproj/xcshareddata/xcschemes/NetworkState.xcscheme")
    if (
        'BuildableName = "NetworkState.framework"' not in framework_scheme
        or 'BlueprintName = "NetworkState"' not in framework_scheme
        or 'buildForArchiving = "YES"' not in framework_scheme
    ):
        failures.append("shared framework scheme must build the NetworkState framework target")

    gitignore_patterns = active_gitignore_patterns(read(".gitignore"))
    for expected in [
        "DerivedData/",
        "*.local.xcconfig",
        "*.secrets.xcconfig",
        "*.mobileprovision",
        "*.p12",
        "*.cer",
        "*.p8",
        ".xcode.env.local",
        ".env",
        ".explore/",
    ]:
        if expected not in gitignore_patterns:
            failures.append(f".gitignore must include {expected}")
    if not git_ignores(ROOT, ".explore/REPO_MAP.md"):
        failures.append(".gitignore must effectively ignore .explore/ files")

    readme_source = read("README.md")
    cocoapods_source_plan = read(
        "docs/plans/2026-06-25-cocoapods-source-boundary.md"
    )
    for fragment in [
        "### CocoaPods Source Boundary",
        "pod 'NetworkState', :git => 'https://github.com/garethpaul/NetworkState.git', :branch => 'master'",
        "The checked-in root podspec describes the current source, but its `0.0.2` version matches a historical tag that predates the current Swift implementation and tests.",
        "replace `:branch => 'master'` with a reviewed commit",
        "does not claim that `NetworkState` is available from the CocoaPods trunk",
    ]:
        if fragment not in readme_source:
            failures.append(f"README CocoaPods source boundary must include {fragment}")
    ruby_blocks = re.findall(r"```ruby\s+(.*?)```", readme_source, re.DOTALL)
    for ruby_block in ruby_blocks:
        declarations = re.findall(
            r"^\s*pod\s*(?:\(\s*)?['\"]NetworkState['\"].*?(?=^\s*pod\b|\Z)",
            ruby_block,
            re.DOTALL | re.MULTILINE,
        )
        for declaration in declarations:
            normalized_declaration = re.sub(r"\s+", " ", declaration)
            if not re.search(r"(?::git\s*=>|git:)", normalized_declaration):
                failures.append(
                    "README must not recommend trunk-only NetworkState installation"
                )
            if re.search(
                r"(?::tag\s*=>|tag:)\s*['\"]0\.0\.2['\"]",
                normalized_declaration,
            ):
                failures.append("README must not recommend the stale 0.0.2 source tag")
    trunk_disclaimer = (
        "does not claim that `NetworkState` is available from the CocoaPods trunk"
    )
    trunk_claim_source = readme_source.replace(trunk_disclaimer, "")
    if re.search(r"\bCocoaPods\s+trunk\b", trunk_claim_source, re.IGNORECASE):
        failures.append("README must not claim CocoaPods trunk availability")
    if not all(
        evidence in cocoapods_source_plan.lower()
        for evidence in [
            "status: completed",
            "historical 0.0.2 tag",
            "reviewed commit",
            "hostile mutations",
        ]
    ):
        failures.append(
            "CocoaPods source-boundary plan must record completed tag, pinning, and mutation evidence"
        )
    docs = readme_source + "\n" + read("VISION.md") + "\n" + read("SECURITY.md")
    location_independent_make_plan = read(
        "docs/plans/2026-06-13-location-independent-make.md"
    )
    spaced_makefile_plan = read("docs/plans/2026-06-21-spaced-makefile-path.md")
    if "make -f /path/to/NetworkState/Makefile check" not in readme_source:
        failures.append("README must document location-independent Makefile invocation")
    if not all(
        evidence in location_independent_make_plan.lower()
        for evidence in [
            "status: completed",
            "root and external-directory",
            "five isolated hostile mutations",
        ]
    ):
        failures.append(
            "location-independent Make plan must record completed root, external, and mutation verification"
        )
    if not all(value in spaced_makefile_plan for value in [
        "status: completed",
        "spaces, brackets, and an apostrophe",
        "MAKEFILE_LIST",
        "all six Make aliases",
    ]):
        failures.append("spaced Makefile path plan must preserve hostile-path and override verification")
    make_contract_docs = "\n".join(
        read(path)
        for path in [
            "README.md",
            "SECURITY.md",
            "AGENTS.md",
            "CHANGES.md",
            "docs/plans/2026-06-21-spaced-makefile-path.md",
        ]
    )
    for phrase in [
        "`/bin/sh`",
        "`/usr/bin/python3`",
        "additional `-f` Makefiles are caller-supplied Make programs",
        "outside the local Make trust boundary",
        "hosted direct workflow remains authoritative",
        "fake `python3`",
        "`MAKEFLAGS` `SHELL`",
    ]:
        if phrase not in make_contract_docs:
            failures.append(f"Make trust-boundary docs must mention {phrase}")
    for overclaim in [
        "reject additional `-f`",
        "additional `-f` Makefiles before",
        "recipe replacement were rejected",
        "before a replaced recipe can claim success",
    ]:
        if overclaim in make_contract_docs:
            failures.append(f"Make trust-boundary docs must not overclaim: {overclaim}")
    for phrase in [
        "make check",
        "pod spec lint",
        "SystemConfiguration",
        "local to the device",
        "reachability flag",
        "automatic connection",
        "requires the reachable flag",
        "combined automatic connection flags",
        "intervention-required flag",
        "automatic intervention matrix",
        "iOS 8.0",
        "framework version alignment",
        "shared framework scheme",
        "make lint",
        "make test",
        "make build",
    ]:
        if phrase not in docs:
            failures.append(f"docs must mention {phrase}")
    for relative_path in ["README.md", "SECURITY.md", "VISION.md", "CHANGES.md"]:
        if "wwan reachability flag matrix" not in read(relative_path).lower():
            failures.append(f"{relative_path} must document the WWAN reachability flag matrix")
        if "reachability decision truth table" not in read(relative_path).lower():
            failures.append(f"{relative_path} must document the reachability decision truth table")
    intervention_scope_guidance = {
        "README.md": "does not invalidate a route that is already reachable",
        "SECURITY.md": "only when a required connection still needs user action",
        "VISION.md": "scoped to connections that must first be established",
        "CHANGES.md": "preserving already reachable routes that need no connection",
    }
    for relative_path, phrase in intervention_scope_guidance.items():
        if phrase not in " ".join(read(relative_path).split()):
            failures.append(f"{relative_path} must document intervention-required scope")

    readme = " ".join(read("README.md").split())
    for phrase in [
        "synchronous snapshot",
        "IPv4 default route",
        "does not prove internet access",
        "DNS resolution",
        "captive-portal completion",
        "availability of a specific service",
        "legacy compatibility boundary",
        "CocoaPods is the only declared package-manager integration",
        "Swift Package Manager and Carthage are unsupported",
        "no remote probes",
    ]:
        if phrase not in readme:
            failures.append(f"README platform assumptions must mention {phrase}")

    security = " ".join(read("SECURITY.md").split())
    for phrase in [
        "local flag snapshot with no remote probes",
        "must not be documented as proof of internet access",
        "CocoaPods is the only declared package-manager integration",
    ]:
        if phrase not in security:
            failures.append(f"security platform assumptions must mention {phrase}")

    vision = " ".join(read("VISION.md").split())
    for phrase in [
        "iOS 8.0 is a legacy package boundary",
        "synchronous IPv4 default-route flag snapshot",
        "CocoaPods as the only declared package-manager integration",
        "no remote probes",
    ]:
        if phrase not in vision:
            failures.append(f"vision platform assumptions must mention {phrase}")

    plan = read("docs/plans/2026-06-08-network-state-baseline.md")
    if "status: completed" not in plan or "make check" not in plan:
        failures.append("completed plan must record status and verification")
    unsigned_plan = read("docs/plans/2026-06-09-unsigned-build-default.md")
    if "status: completed" not in unsigned_plan or "CODE_SIGNING_ALLOWED" not in unsigned_plan:
        failures.append("unsigned build plan must record status and signing verification")
    flag_plan = read("docs/plans/2026-06-09-reachability-flag-evaluation.md")
    if "status: completed" not in flag_plan or "make check" not in flag_plan:
        failures.append("reachability flag evaluation plan must record status and verification")
    automatic_plan_path = ROOT / "docs/plans/2026-06-09-automatic-reachability-flags.md"
    automatic_plan = automatic_plan_path.read_text(encoding="utf-8") if automatic_plan_path.exists() else ""
    if "status: completed" not in automatic_plan or "make check" not in automatic_plan:
        failures.append("automatic reachability flag plan must record status and verification")
    reachable_plan_path = ROOT / "docs/plans/2026-06-09-automatic-reachable-flag.md"
    reachable_plan = reachable_plan_path.read_text(encoding="utf-8") if reachable_plan_path.exists() else ""
    if "status: completed" not in reachable_plan or "make check" not in reachable_plan:
        failures.append("automatic reachable flag plan must record status and verification")
    deployment_plan_path = ROOT / "docs/plans/2026-06-09-podspec-deployment-target-alignment.md"
    deployment_plan = deployment_plan_path.read_text(encoding="utf-8") if deployment_plan_path.exists() else ""
    if "status: completed" not in deployment_plan or "make check" not in deployment_plan:
        failures.append("deployment target alignment plan must record status and verification")
    intervention_plan_path = ROOT / "docs/plans/2026-06-09-intervention-required-flag.md"
    intervention_plan = intervention_plan_path.read_text(encoding="utf-8") if intervention_plan_path.exists() else ""
    if "status: completed" not in intervention_plan or "make check" not in intervention_plan:
        failures.append("intervention-required flag plan must record status and verification")
    make_gate_plan_path = ROOT / "docs/plans/2026-06-09-make-gate-aliases.md"
    make_gate_plan = make_gate_plan_path.read_text(encoding="utf-8") if make_gate_plan_path.exists() else ""
    if "status: completed" not in make_gate_plan or "make check" not in make_gate_plan:
        failures.append("Make gate alias plan must record status and verification")
    framework_version_plan_path = ROOT / "docs/plans/2026-06-09-framework-version-alignment.md"
    framework_version_plan = framework_version_plan_path.read_text(encoding="utf-8") if framework_version_plan_path.exists() else ""
    if "status: completed" not in framework_version_plan or "make check" not in framework_version_plan:
        failures.append("framework version alignment plan must record status and verification")
    combined_flags_plan_path = ROOT / "docs/plans/2026-06-09-combined-automatic-flags.md"
    combined_flags_plan = combined_flags_plan_path.read_text(encoding="utf-8") if combined_flags_plan_path.exists() else ""
    if "status: completed" not in combined_flags_plan or "make check" not in combined_flags_plan:
        failures.append("combined automatic connection flag plan must record status and verification")
    shared_scheme_plan_path = ROOT / "docs/plans/2026-06-10-shared-framework-scheme-guard.md"
    shared_scheme_plan = shared_scheme_plan_path.read_text(encoding="utf-8") if shared_scheme_plan_path.exists() else ""
    if "status: completed" not in shared_scheme_plan or "make check" not in shared_scheme_plan:
        failures.append("shared framework scheme guard plan must record status and verification")
    non_reachability_plan = read("docs/plans/2026-06-10-non-reachability-flags.md")
    if "status: completed" not in non_reachability_plan or "make check" not in non_reachability_plan:
        failures.append("non-reachability flag guard plan must record status and verification")
    automatic_intervention_plan = read("docs/plans/2026-06-12-automatic-intervention-matrix.md")
    if "status: completed" not in automatic_intervention_plan or "hostile mutations" not in automatic_intervention_plan:
        failures.append("automatic intervention matrix plan must record completed verification")
    wwan_plan = read("docs/plans/2026-06-15-wwan-reachability-flag-matrix.md")
    if (
        "status: completed" not in wwan_plan
        or "All four Make gates passed" not in wwan_plan
        or "Six isolated hostile mutations were rejected" not in wwan_plan
        or "external directory" not in wwan_plan
    ):
        failures.append("WWAN reachability flag matrix plan must record completed verification")
    truth_table_plan = read("docs/plans/2026-06-15-reachability-decision-truth-table.md")
    if (
        "status: completed" not in truth_table_plan.lower()
        or "All four Make gates passed" not in truth_table_plan
        or "Seven isolated hostile mutations were rejected" not in truth_table_plan
        or "external directory" not in truth_table_plan
        or re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", truth_table_plan)
    ):
        failures.append("reachability decision truth table plan must record completed verification")
    intervention_scope_plan = read("docs/plans/2026-06-15-intervention-required-scope.md")
    if (
        "status: completed" not in intervention_scope_plan.lower()
        or "All four Make gates passed" not in intervention_scope_plan
        or "Six isolated hostile mutations were rejected" not in intervention_scope_plan
        or "external directory" not in intervention_scope_plan
        or re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", intervention_scope_plan)
    ):
        failures.append("intervention-required scope plan must record completed verification")

    hosted_plan = read("docs/plans/2026-06-10-hosted-project-validation.md")
    workflow = read(".github/workflows/check.yml")
    codeowners = read(".github/CODEOWNERS")
    if "status: completed" not in hosted_plan or "make check" not in hosted_plan:
        failures.append("hosted project validation plan must record status and verification")
    for expected in [
        "permissions:\n  contents: read",
        "cancel-in-progress: true",
        "runs-on: macos-15",
        "timeout-minutes: 10",
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
    ]:
        if expected not in workflow:
            failures.append(f"Check workflow must keep {expected}")
    if workflow != EXPECTED_WORKFLOW:
        failures.append("Check workflow must preserve the exact reviewed workflow")

    checkout_plan = read("docs/plans/2026-06-12-checkout-credential-boundary.md")
    if (
        "status: completed" not in checkout_plan
        or "persist-credentials: false" not in checkout_plan
        or "hostile mutations rejected" not in checkout_plan
    ):
        failures.append("checkout credential plan must record completed verification")
    assumptions_plan = read("docs/plans/2026-06-13-platform-network-assumptions.md")
    if (
        "status: completed" not in assumptions_plan
        or "make check" not in assumptions_plan
        or "hostile mutations rejected" not in assumptions_plan
    ):
        failures.append("platform assumptions plan must record completed verification")
    workflow_files = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / ".github/workflows").iterdir()
        if path.is_file()
    )
    if workflow_files != [".github/workflows/check.yml"]:
        failures.append("workflow inventory must contain only .github/workflows/check.yml")
    checkout_step = (
        "      - uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10\n"
        "        with:\n"
        "          persist-credentials: false"
    )
    if workflow.count("actions/checkout@") != 1 or checkout_step not in workflow:
        failures.append("Check workflow must keep one pinned credential-free checkout step")
    if "persist-credentials: true" in workflow:
        failures.append("Check workflow must not persist checkout credentials")
    if codeowners.strip() != "* @garethpaul":
        failures.append("CODEOWNERS must keep repository-wide owner review")
    guidance = " ".join(
        "\n".join(read(path) for path in ["README.md", "SECURITY.md", "VISION.md", "CHANGES.md"]).split()
    ).lower()
    for phrase in ["checkout credentials are not persisted", "credential-free checkout"]:
        if phrase not in guidance:
            failures.append(f"repository guidance must mention {phrase}")

    xcodebuild = Path("/usr/bin/xcodebuild")
    if xcodebuild.is_file() and os.access(xcodebuild, os.X_OK):
        result = subprocess.run(
            [str(xcodebuild), "-list", "-project", "NetworkState.xcodeproj"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            failures.append("xcodebuild could not parse NetworkState.xcodeproj: " + result.stderr.strip())
    else:
        print("xcodebuild unavailable; static iOS baseline only.")

    for plist_path in ["NetworkState/Info.plist", "NetworkStateTests/Info.plist"]:
        try:
            info = plistlib.loads((ROOT / plist_path).read_bytes())
        except Exception as error:
            failures.append(f"{plist_path} must parse as a plist: {error}")
            continue
        if (
            plist_path == "NetworkState/Info.plist"
            and podspec_version is not None
            and info.get("CFBundleShortVersionString") != podspec_version
        ):
            failures.append(f"framework Info.plist version must match NetworkState.podspec version {podspec_version}")

    for xml_path in [
        "docs/readme-overview.svg",
        "NetworkState.xcodeproj/xcshareddata/xcschemes/NetworkState.xcscheme",
        "NetworkState.xcodeproj/xcshareddata/xcschemes/NetworkStateTests.xcscheme",
    ]:
        try:
            ET.parse(ROOT / xml_path)
        except Exception as error:
            failures.append(f"{xml_path} must parse as XML: {error}")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("NetworkState baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
