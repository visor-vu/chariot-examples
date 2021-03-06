import edu.vanderbilt.isis.chariot.imagingsatellitecluster.*
package edu.vanderbilt.isis.chariot.imagingsatellitecluster {
	component HighResolutionImageGrabberComponent {
		provides high_resolution_image_capture {
			hr_image_t as high_resolution_image_capture.high_resolution_image_sender
		}
		
		requires 512 MB memory
		requires ImagingSatellite.default_imaging_satellite.hr_camera device
	}
}
