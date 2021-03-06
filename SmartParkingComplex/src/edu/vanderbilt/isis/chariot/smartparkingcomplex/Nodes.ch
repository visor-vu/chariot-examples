import edu.vanderbilt.isis.chariot.smartparkingcomplex.*
package edu.vanderbilt.isis.chariot.smartparkingcomplex {
	nodeCategory CameraNode {
		// Template for Wi-Fi enabled (wireless IP) 
		// camera nodes.
		nodeTemplate wifi_cam {
			memory 64 MB
			storage 1024 MB 	// 1 GB external
		}
	}
	
	nodeCategory ProcessingNode {
		// Template for Edison nodes.
		nodeTemplate edison {
			memory 1024 MB		// 1 GB
			storage 4096 MB		// 4 GB
		}
	}
	
	nodeCategory TerminalNode {	
		// Template for entry terminal nodes.
		nodeTemplate entry_terminal {
			memory 128 MB
			storage 8192 MB		// 8 GB
		}
	}
}