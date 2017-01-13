# SmartParkingComplex Example

This example models a complex smart parking system comprising two objectives and three replication constraints (see system description [here](src/edu/vanderbilt/isis/chariot/smartparkingcomplex/System.ch)). This example builds on the [SmartParkingBasic](https://github.com/visor-vu/chariot-examples/tree/master/SmartParkingBasic) example; the list below specifies the differences between the two smart parking systems:

1. Although the objectives are the same (*RequestHandling*, and *OccupancyChecking*), the functionalities required to satisfy these objectives are more complex for this example. The basic smart parking example uses three functionalities: (1) parking_client, (2) parking_manager, and (3) occupancy_sensor. The first two functionalities are also used by this (complex) example, however, the  *occupancy_sensor* functionality used in the basic example is divided into three different functionalities (*image_capture*, *load_balancer*, and *occupancy_detector*) in this example. As such, in total, this complex smart parking example uses five functionalities: (1) parking_client, (2) parking_manager, (3) image_capture, (4) load_balancer, and (5) occupancy_detector.

  There are five different component types, one for each functionality: (1) ParkingClient, (2) ParkingManager, (3) ImageCapture, (4) LoadBalancer, and (5) OccupancyDetector. The *ImageCapture* component type provides the *image_capture* functionality by periodically capturing images of one or more parking spaces. The *OccupancyDetector* component type provides the *occupancy_detector* functionality by receiving images from *ImageCapture* component instance(s), analyzing them to determine status of parking spaces captured in those images, and sending determined status to a *ParkingManager* component instance. An *ImageCapture* component instance does not directly send images to an *OccupancyDetector* component instance; since there can be multiple instances of the latter (due to replication constraint), a load balancer is required. The *LoadBalancer* component type provides the *load_balancer* functionality by distributing load between multiple instances of the *OccupancyDetectory* component type.

  The figure below presents a system description overview for this example:
  
  <img src="https://github.com/visor-vu/chariot-examples/blob/master/SmartParkingComplex/SmartParkingComplex.png" width="65%" height="65%"/>

2. As shown in the figure above, this example uses three different replication constraints. The *image_capture* and *parking_client* functionaities are associated with *per node* replication constraints. The *occupancy_detector* functionality is associated with a range-based cluster constraint with minimum of 3 and maximum of 5 replications. This means that during the initial deployment, there must be enough resources to deploy 5 instances of a component type that provides the *parking_manager* functionality.

3. Finally, unlike the basic smart parking example, this example requires heterogeneous hardware resources. The [hardware description](src/edu/vanderbilt/isis/chariot/smartparkingcomplex/Nodes.ch) for this example necessitates three categories of resources: (1) CameraNode, (2) ProcessingNode, and (3) TerminalNode. Each of these categories has a template each. In general, nodes belonging to the *CameraNode* category are camera enabled nodes that can host the *ImageCapture* component instance. The nodes belonging to the *ProcessingNode* category are nodes with greater processing power that can host instances of other component types except *ParkingClient*, which is hosted on nodes belonging to the *TerminalNode* categories (these nodes are parking lot terminals that are used to enter and exit a parking lot).