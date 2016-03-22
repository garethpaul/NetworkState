#!/bin/sh

set -eu

function ci_lib() {
    NAME=$1
    xcodebuild -project NetworkState.xcodeproj
}

ci_lib "iPhone 5"
