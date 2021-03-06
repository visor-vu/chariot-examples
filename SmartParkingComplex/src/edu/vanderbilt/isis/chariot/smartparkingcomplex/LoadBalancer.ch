import edu.vanderbilt.isis.chariot.smartparkingcomplex.*
package edu.vanderbilt.isis.chariot.smartparkingcomplex {
	component LoadBalancer {
 		provides load_balancer {
 			detector_request_t as load_balancer.detector_request
 			detector_response_t as load_balancer.detector_response
 		}
 		
 		requires 128 MB memory
 		
 		startScript "sh LoadBalancer.sh"
 	}
}