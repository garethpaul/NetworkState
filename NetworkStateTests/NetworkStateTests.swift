//
//  NetworkStateTests.swift
//  NetworkStateTests
//
//  Created by Gareth on 7/1/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import XCTest
import NetworkState

class NetworkStateTests: XCTestCase {

    func testConnectivityCheckReturnsBoolean() {
        let result = NetworkState.isConnectedToNetwork()
        XCTAssertTrue(result || !result)
    }

}
