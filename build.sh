#!/bin/sh

set -eu

function ci_lib() {
    NAME=$1
    xcodebuild -project NetworkState.xcodeproj \
               -target "NetworkState" \
               -destination "platform=iOS Simulator,name=${NAME}" \
               -sdk iphonesimulator \
               build test
}

ci_lib "iPhone 5"
