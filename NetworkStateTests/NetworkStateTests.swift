//
//  NetworkStateTests.swift
//  NetworkStateTests
//
//  Created by Gareth on 7/1/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import XCTest
import SystemConfiguration
@testable import NetworkState

class NetworkStateTests: XCTestCase {

    func testMissingReachabilitySnapshotIsUnavailable() {
        XCTAssertFalse(NetworkState.isConnectedToNetwork(flagsProvider: { nil }))
    }

    func testProvidedReachabilitySnapshotUsesSharedEvaluator() {
        let reachable = SCNetworkReachabilityFlags.reachable
        let unavailable = SCNetworkReachabilityFlags()

        XCTAssertEqual(
            NetworkState.isConnectedToNetwork(flagsProvider: { reachable }),
            NetworkState.isReachableWithFlags(reachable)
        )
        XCTAssertEqual(
            NetworkState.isConnectedToNetwork(flagsProvider: { unavailable }),
            NetworkState.isReachableWithFlags(unavailable)
        )
    }

    func testReachabilityFlagEvaluation() {
        let reachable = SCNetworkReachabilityFlags.reachable.rawValue
        let connectionRequired = SCNetworkReachabilityFlags.connectionRequired.rawValue

        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable)))
        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | connectionRequired)))
        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: 0)))
    }

    func testReachabilityFlagEvaluationAllowsAutomaticConnection() {
        let reachable = SCNetworkReachabilityFlags.reachable.rawValue
        let connectionRequired = SCNetworkReachabilityFlags.connectionRequired.rawValue
        let connectionOnDemand = SCNetworkReachabilityFlags.connectionOnDemand.rawValue
        let connectionOnTraffic = SCNetworkReachabilityFlags.connectionOnTraffic.rawValue
        let interventionRequired = SCNetworkReachabilityFlags.interventionRequired.rawValue

        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | connectionRequired | connectionOnDemand)))
        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | connectionRequired | connectionOnTraffic)))
        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | connectionRequired | connectionOnDemand | interventionRequired)))
    }

    func testAutomaticConnectionStillRequiresReachableFlag() {
        let connectionRequired = SCNetworkReachabilityFlags.connectionRequired.rawValue
        let connectionOnDemand = SCNetworkReachabilityFlags.connectionOnDemand.rawValue
        let connectionOnTraffic = SCNetworkReachabilityFlags.connectionOnTraffic.rawValue

        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: connectionRequired | connectionOnDemand)))
        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: connectionRequired | connectionOnTraffic)))
    }

    func testCombinedAutomaticConnectionFlagsAreReachable() {
        let reachable = SCNetworkReachabilityFlags.reachable.rawValue
        let connectionRequired = SCNetworkReachabilityFlags.connectionRequired.rawValue
        let connectionOnDemand = SCNetworkReachabilityFlags.connectionOnDemand.rawValue
        let connectionOnTraffic = SCNetworkReachabilityFlags.connectionOnTraffic.rawValue

        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | connectionRequired | connectionOnDemand | connectionOnTraffic)))
    }

    func testInterventionRequiredDoesNotBlockEstablishedReachability() {
        let reachable = SCNetworkReachabilityFlags.reachable.rawValue
        let interventionRequired = SCNetworkReachabilityFlags.interventionRequired.rawValue

        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | interventionRequired)))
    }

    func testAutomaticConnectionModesRequireNoUserIntervention() {
        let reachable = SCNetworkReachabilityFlags.reachable.rawValue
        let connectionRequired = SCNetworkReachabilityFlags.connectionRequired.rawValue
        let connectionOnDemand = SCNetworkReachabilityFlags.connectionOnDemand.rawValue
        let connectionOnTraffic = SCNetworkReachabilityFlags.connectionOnTraffic.rawValue
        let interventionRequired = SCNetworkReachabilityFlags.interventionRequired.rawValue
        let requiredFlags = reachable | connectionRequired | interventionRequired

        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: requiredFlags | connectionOnDemand)))
        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: requiredFlags | connectionOnTraffic)))
        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: requiredFlags | connectionOnDemand | connectionOnTraffic)))
    }

    func testNonReachabilityFlagsDoNotCreateConnectivity() {
        let reachable = SCNetworkReachabilityFlags.reachable.rawValue
        let transientConnection = SCNetworkReachabilityFlags.transientConnection.rawValue
        let localAddress = SCNetworkReachabilityFlags.isLocalAddress.rawValue
        let direct = SCNetworkReachabilityFlags.isDirect.rawValue
        let ancillaryFlags = transientConnection | localAddress | direct

        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: ancillaryFlags)))
        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | ancillaryFlags)))
    }

    func testWWANFlagRequiresReachableBaseFlag() {
#if os(iOS)
        let reachable = SCNetworkReachabilityFlags.reachable.rawValue
        let wwan = SCNetworkReachabilityFlags.isWWAN.rawValue

        XCTAssertFalse(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: wwan)))
        XCTAssertTrue(NetworkState.isReachableWithFlags(SCNetworkReachabilityFlags(rawValue: reachable | wwan)))
#endif
    }

    func testReachabilityDecisionTruthTable() {
        let booleanValues = [false, true]
        var coveredRows = 0

        for isReachable in booleanValues {
            for connectionRequired in booleanValues {
                for connectionOnDemand in booleanValues {
                    for connectionOnTraffic in booleanValues {
                        for interventionRequired in booleanValues {
                            var rawValue: UInt32 = 0
                            if isReachable {
                                rawValue |= SCNetworkReachabilityFlags.reachable.rawValue
                            }
                            if connectionRequired {
                                rawValue |= SCNetworkReachabilityFlags.connectionRequired.rawValue
                            }
                            if connectionOnDemand {
                                rawValue |= SCNetworkReachabilityFlags.connectionOnDemand.rawValue
                            }
                            if connectionOnTraffic {
                                rawValue |= SCNetworkReachabilityFlags.connectionOnTraffic.rawValue
                            }
                            if interventionRequired {
                                rawValue |= SCNetworkReachabilityFlags.interventionRequired.rawValue
                            }

                            let canConnectAutomatically = connectionOnDemand || connectionOnTraffic
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
        }

        XCTAssertEqual(coveredRows, 32)
    }

}
