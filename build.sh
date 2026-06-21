#!/bin/sh

set -eu

PROJECT=${PROJECT:-NetworkState.xcodeproj}
SCHEME=${SCHEME:-NetworkStateTests}
DESTINATION=${DESTINATION:-platform=iOS Simulator,name=iPhone 16 Pro}
SDK=${SDK:-iphonesimulator}
SWIFT_VERSION=${SWIFT_VERSION:-5.0}
IPHONEOS_DEPLOYMENT_TARGET=${IPHONEOS_DEPLOYMENT_TARGET:-12.0}
CODE_SIGNING_ALLOWED=${CODE_SIGNING_ALLOWED:-NO}
XCODEBUILD=/usr/bin/xcodebuild

if [ ! -x "$XCODEBUILD" ]; then
    echo "xcodebuild is required to run ${SCHEME}" >&2
    exit 127
fi

"$XCODEBUILD" -project "${PROJECT}" \
           -scheme "${SCHEME}" \
           -destination "${DESTINATION}" \
           -sdk "${SDK}" \
           SWIFT_VERSION="${SWIFT_VERSION}" \
           IPHONEOS_DEPLOYMENT_TARGET="${IPHONEOS_DEPLOYMENT_TARGET}" \
           CODE_SIGNING_ALLOWED="${CODE_SIGNING_ALLOWED}" \
           build test
