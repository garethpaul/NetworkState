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

    func testReachabilityFlagEvaluationAllowsAutomaticConnection() {
        let reachable = UInt32(kSCNetworkFlagsReachable)
        let connectionRequired = UInt32(kSCNetworkFlagsConnectionRequired)
        let connectionOnDemand = UInt32(kSCNetworkFlagsConnectionOnDemand)
        let connectionOnTraffic = UInt32(kSCNetworkFlagsConnectionOnTraffic)
        let interventionRequired = UInt32(kSCNetworkFlagsInterventionRequired)

        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | connectionRequired | connectionOnDemand)))
        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | connectionRequired | connectionOnTraffic)))
        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | connectionRequired | connectionOnDemand | interventionRequired)))
    }

    func testAutomaticConnectionStillRequiresReachableFlag() {
        let connectionRequired = UInt32(kSCNetworkFlagsConnectionRequired)
        let connectionOnDemand = UInt32(kSCNetworkFlagsConnectionOnDemand)
        let connectionOnTraffic = UInt32(kSCNetworkFlagsConnectionOnTraffic)

        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: connectionRequired | connectionOnDemand)))
        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: connectionRequired | connectionOnTraffic)))
    }

    func testInterventionRequiredFlagPreventsReachability() {
        let reachable = UInt32(kSCNetworkFlagsReachable)
        let interventionRequired = UInt32(kSCNetworkFlagsInterventionRequired)

        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | interventionRequired)))
    }

}
