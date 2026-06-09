#!/usr/bin/env python3
"""Static baseline checks for the legacy NetworkState Swift framework."""

from pathlib import Path
import plistlib
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ".gitignore",
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
    "NetworkState.xcodeproj/xcshareddata/xcschemes/NetworkStateTests.xcscheme",
    "docs/plans/2026-06-08-network-state-baseline.md",
    "docs/plans/2026-06-09-unsigned-build-default.md",
    "docs/plans/2026-06-09-reachability-flag-evaluation.md",
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

    tests = read("NetworkStateTests/NetworkStateTests.swift")
    if "import NetworkState" not in tests:
        failures.append("tests must import the framework module")
    if "NetworkState.isConnectedToNetwork()" not in tests:
        failures.append("tests must exercise the public connectivity API")
    if "testReachabilityFlagEvaluation" not in tests or "isReachableWithFlags" not in tests:
        failures.append("tests must cover reachability flag evaluation")
    if "testExample" in tests or "testPerformanceExample" in tests:
        failures.append("placeholder XCTest methods must be replaced")

    build = read("build.sh")
    for phrase in ["PROJECT=${PROJECT:-NetworkState.xcodeproj}", "SCHEME=${SCHEME:-NetworkStateTests}", "DESTINATION=${DESTINATION:-", "CODE_SIGNING_ALLOWED=${CODE_SIGNING_ALLOWED:-NO}", 'CODE_SIGNING_ALLOWED="${CODE_SIGNING_ALLOWED}"', "command -v xcodebuild"]:
        if phrase not in build:
            failures.append(f"build.sh must include {phrase}")
    if "function " in build:
        failures.append("build.sh must use POSIX shell function syntax or no shell functions")

    podspec = read("NetworkState.podspec")
    for phrase in ['s.framework  = "SystemConfiguration"', 's.source_files = "NetworkState/*.{swift}"', 's.social_media_url   = "https://twitter.com/gpj"']:
        if phrase not in podspec:
            failures.append(f"podspec must include {phrase}")
    if "http://twitter.com" in podspec or "http://docs.cocoapods.org" in podspec:
        failures.append("podspec metadata should use HTTPS URLs")

    travis = read(".travis.yml")
    if "- make check" not in travis or "- ./build.sh" not in travis:
        failures.append(".travis.yml must run static checks before the Xcode build")

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
    for phrase in ["make check", "pod spec lint", "SystemConfiguration", "local to the device", "reachability flag"]:
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

    for plist_path in ["NetworkState/Info.plist", "NetworkStateTests/Info.plist"]:
        try:
            plistlib.loads((ROOT / plist_path).read_bytes())
        except Exception as error:
            failures.append(f"{plist_path} must parse as a plist: {error}")

    for xml_path in ["docs/readme-overview.svg", "NetworkState.xcodeproj/xcshareddata/xcschemes/NetworkStateTests.xcscheme"]:
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
