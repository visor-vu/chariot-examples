import edu.vanderbilt.isis.chariot.imagingsatellitecluster.*
package edu.vanderbilt.isis.chariot.imagingsatellitecluster {
	component LowResolutionImageGrabberComponent {
		provides low_resolution_image_capture {
			lr_image_t as low_resolution_image_capture.low_resolution_image_sender
		}
		
		requires 256 MB memory
		requires ImagingSatellite.default_imaging_satellite.lr_camera device
	}
}
