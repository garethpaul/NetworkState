#!/bin/sh

set -eu

PROJECT=${PROJECT:-NetworkState.xcodeproj}
SCHEME=${SCHEME:-NetworkStateTests}
DESTINATION=${DESTINATION:-platform=iOS Simulator,name=iPhone 5}
SDK=${SDK:-iphonesimulator}

if ! command -v xcodebuild >/dev/null 2>&1; then
    echo "xcodebuild is required to run ${SCHEME}" >&2
    exit 127
fi

xcodebuild -project "${PROJECT}" \
           -scheme "${SCHEME}" \
           -destination "${DESTINATION}" \
           -sdk "${SDK}" \
           build test
