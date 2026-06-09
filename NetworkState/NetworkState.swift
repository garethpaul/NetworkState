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
        zeroAddress.sin_len = UInt8(sizeofValue(zeroAddress))
        zeroAddress.sin_family = sa_family_t(AF_INET)

        let defaultRouteReachability = withUnsafePointer(&zeroAddress) {
            SCNetworkReachabilityCreateWithAddress(nil, UnsafePointer($0))
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

    public class func isReachableWithFlags(flags: SCNetworkReachabilityFlags) -> Bool {
        let isReachable = (flags.rawValue & UInt32(kSCNetworkFlagsReachable)) != 0
        let needsConnection = (flags.rawValue & UInt32(kSCNetworkFlagsConnectionRequired)) != 0
        return (isReachable && !needsConnection)
    }
}
