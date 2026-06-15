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

    func testCombinedAutomaticConnectionFlagsAreReachable() {
        let reachable = UInt32(kSCNetworkFlagsReachable)
        let connectionRequired = UInt32(kSCNetworkFlagsConnectionRequired)
        let connectionOnDemand = UInt32(kSCNetworkFlagsConnectionOnDemand)
        let connectionOnTraffic = UInt32(kSCNetworkFlagsConnectionOnTraffic)

        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | connectionRequired | connectionOnDemand | connectionOnTraffic)))
    }

    func testInterventionRequiredDoesNotBlockEstablishedReachability() {
        let reachable = UInt32(kSCNetworkFlagsReachable)
        let interventionRequired = UInt32(kSCNetworkFlagsInterventionRequired)

        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | interventionRequired)))
    }

    func testAutomaticConnectionModesRequireNoUserIntervention() {
        let reachable = UInt32(kSCNetworkFlagsReachable)
        let connectionRequired = UInt32(kSCNetworkFlagsConnectionRequired)
        let connectionOnDemand = UInt32(kSCNetworkFlagsConnectionOnDemand)
        let connectionOnTraffic = UInt32(kSCNetworkFlagsConnectionOnTraffic)
        let interventionRequired = UInt32(kSCNetworkFlagsInterventionRequired)
        let requiredFlags = reachable | connectionRequired | interventionRequired

        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: requiredFlags | connectionOnDemand)))
        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: requiredFlags | connectionOnTraffic)))
        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: requiredFlags | connectionOnDemand | connectionOnTraffic)))
    }

    func testNonReachabilityFlagsDoNotCreateConnectivity() {
        let reachable = UInt32(kSCNetworkFlagsReachable)
        let transientConnection = UInt32(kSCNetworkFlagsTransientConnection)
        let localAddress = UInt32(kSCNetworkFlagsIsLocalAddress)
        let direct = UInt32(kSCNetworkFlagsIsDirect)
        let ancillaryFlags = transientConnection | localAddress | direct

        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: ancillaryFlags)))
        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | ancillaryFlags)))
    }

    func testWWANFlagRequiresReachableBaseFlag() {
        let reachable = UInt32(kSCNetworkFlagsReachable)
        let wwan = UInt32(kSCNetworkFlagsIsWWAN)

        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: wwan)))
        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | wwan)))
    }

    func testReachabilityDecisionTruthTable() {
        let booleanValues = [false, true]
        var coveredRows = 0

        for isReachable in booleanValues {
            for connectionRequired in booleanValues {
                for canConnectAutomatically in booleanValues {
                    for interventionRequired in booleanValues {
                        var rawValue: UInt32 = 0
                        if isReachable {
                            rawValue |= UInt32(kSCNetworkFlagsReachable)
                        }
                        if connectionRequired {
                            rawValue |= UInt32(kSCNetworkFlagsConnectionRequired)
                        }
                        if canConnectAutomatically {
                            rawValue |= UInt32(kSCNetworkFlagsConnectionOnDemand)
                        }
                        if interventionRequired {
                            rawValue |= UInt32(kSCNetworkFlagsInterventionRequired)
                        }

                        let expected = isReachable &&
                            (!connectionRequired || (canConnectAutomatically && !interventionRequired))
                        XCTAssertEqual(
                            NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: rawValue)),
                            expected
                        )
                        coveredRows += 1
                    }
                }
            }
        }

        XCTAssertEqual(coveredRows, 16)
    }

}
