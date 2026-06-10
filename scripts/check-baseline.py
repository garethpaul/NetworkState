#!/usr/bin/env python3
"""Static baseline checks for the legacy NetworkState Swift framework."""

from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ".gitignore",
    ".github/workflows/check.yml",
    ".travis.yml",
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
    "docs/readme-overview.svg",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


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
    if "public class func isReachableWithFlags(flags: SCNetworkReachabilityFlags) -> Bool" not in swift:
        failures.append("reachability flag evaluation must be exposed for fixture tests")
    if "return isReachableWithFlags(flags)" not in swift:
        failures.append("isConnectedToNetwork must use the shared flag evaluator")
    for phrase in [
        "canConnectAutomatically",
        "kSCNetworkFlagsConnectionOnDemand",
        "kSCNetworkFlagsConnectionOnTraffic",
        "kSCNetworkFlagsInterventionRequired",
    ]:
        if phrase not in swift:
            failures.append(f"reachability flag evaluation must handle {phrase}")
    if "return isReachable &&" not in swift:
        failures.append("automatic reachability handling must still require the reachable flag")
    if "return isReachable && !interventionRequired" not in swift:
        failures.append("reachability evaluation must reject intervention-required states")
    if "(flags.rawValue & UInt32(kSCNetworkFlagsReachable)) != 0" not in swift:
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
    if "testInterventionRequiredFlagPreventsReachability" not in tests:
        failures.append("tests must cover intervention-required reachability flags")
    if (
        "testNonReachabilityFlagsDoNotCreateConnectivity" not in tests
        or "kSCNetworkFlagsTransientConnection" not in tests
        or "kSCNetworkFlagsIsLocalAddress" not in tests
        or "kSCNetworkFlagsIsDirect" not in tests
    ):
        failures.append("tests must cover ancillary flags with and without the Reachable flag")
    if "testExample" in tests or "testPerformanceExample" in tests:
        failures.append("placeholder XCTest methods must be replaced")

    build = read("build.sh")
    for phrase in ["PROJECT=${PROJECT:-NetworkState.xcodeproj}", "SCHEME=${SCHEME:-NetworkStateTests}", "DESTINATION=${DESTINATION:-", "CODE_SIGNING_ALLOWED=${CODE_SIGNING_ALLOWED:-NO}", 'CODE_SIGNING_ALLOWED="${CODE_SIGNING_ALLOWED}"', "command -v xcodebuild"]:
        if phrase not in build:
            failures.append(f"build.sh must include {phrase}")
    if "function " in build:
        failures.append("build.sh must use POSIX shell function syntax or no shell functions")

    makefile = read("Makefile")
    for phrase in [
        ".PHONY: build check lint static-check test verify",
        "check: verify",
        "lint test build verify: static-check",
    ]:
        if phrase not in makefile:
            failures.append(f"Makefile must include standard gate alias: {phrase}")

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

    gitignore = read(".gitignore")
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
    ]:
        if expected not in gitignore:
            failures.append(f".gitignore must include {expected}")

    docs = read("README.md") + "\n" + read("VISION.md") + "\n" + read("SECURITY.md")
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
        "iOS 8.0",
        "framework version alignment",
        "shared framework scheme",
        "make lint",
        "make test",
        "make build",
    ]:
        if phrase not in docs:
            failures.append(f"docs must mention {phrase}")

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

    hosted_plan = read("docs/plans/2026-06-10-hosted-project-validation.md")
    workflow = read(".github/workflows/check.yml")
    if "status: completed" not in hosted_plan or "make check" not in hosted_plan:
        failures.append("hosted project validation plan must record status and verification")
    for expected in [
        "permissions:\n  contents: read",
        "cancel-in-progress: true",
        "runs-on: macos-15",
        "timeout-minutes: 10",
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "run: make check",
    ]:
        if expected not in workflow:
            failures.append(f"Check workflow must keep {expected}")

    if shutil.which("xcodebuild"):
        result = subprocess.run(
            ["xcodebuild", "-list", "-project", "NetworkState.xcodeproj"],
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
