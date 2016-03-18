#!/bin/sh

set -eu

function ci_lib() {
    NAME=$1
    xcodebuild -project NetworkState.xcodeproj \
               build
}

ci_lib "iPhone 5"
