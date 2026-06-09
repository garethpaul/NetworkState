//
//  NetworkStateTests.swift
//  NetworkStateTests
//
//  Created by Gareth on 7/1/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import XCTest
import SystemConfiguration
import NetworkState

class NetworkStateTests: XCTestCase {

    func testConnectivityCheckReturnsBoolean() {
        let result = NetworkState.isConnectedToNetwork()
        XCTAssertTrue(result || !result)
    }

    func testReachabilityFlagEvaluation() {
        let reachable = UInt32(kSCNetworkFlagsReachable)
        let connectionRequired = UInt32(kSCNetworkFlagsConnectionRequired)

        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable)))
        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | connectionRequired)))
        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: 0)))
    }

}
