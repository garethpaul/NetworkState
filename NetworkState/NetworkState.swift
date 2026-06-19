//
//  NetworkState.h
//  NetworkState
//
//  Created by Gareth Jones on 1/10/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import SystemConfiguration

public class NetworkState {
    public class func isConnectedToNetwork() -> Bool {
        var zeroAddress = sockaddr_in()
        zeroAddress.sin_len = UInt8(MemoryLayout<sockaddr_in>.size)
        zeroAddress.sin_family = sa_family_t(AF_INET)

        let defaultRouteReachability = withUnsafePointer(to: &zeroAddress) {
            $0.withMemoryRebound(to: sockaddr.self, capacity: 1) {
                SCNetworkReachabilityCreateWithAddress(nil, $0)
            }
        }

        guard let reachability = defaultRouteReachability else {
            return false
        }

        var flags = SCNetworkReachabilityFlags()
        if !SCNetworkReachabilityGetFlags(reachability, &flags) {
            return false
        }
        return isReachableWithFlags(flags)
    }

    public class func isReachableWithFlags(_ flags: SCNetworkReachabilityFlags) -> Bool {
        let isReachable = flags.contains(.reachable)
        let needsConnection = flags.contains(.connectionRequired)
        let canConnectAutomatically = flags.contains(.connectionOnDemand) ||
            flags.contains(.connectionOnTraffic)
        let interventionRequired = flags.contains(.interventionRequired)
        let canConnectWithoutUserInteraction = canConnectAutomatically && !interventionRequired

        return isReachable && (!needsConnection || canConnectWithoutUserInteraction)
    }
}
