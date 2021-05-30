# Our Journey
This is our journey in exploring autonomous driving system on various platforms, we started on:

## PC
On the pc we experienced AirSim, an realistic, open world driving simulator. <br />
We started with basic controll of the viechle thorugh python scripts, once we figured out how to drive the car with nothing but python scripts we started implementing
some features using data we collected from the simulator with Lidar sensors. <br />
We first implemented an auto-braking system that will break the car in case of speeding towards an obstacle, we did it by using a single Lidar sensor that has been mounted
in the front of the car.
Since the speed of the car is known to us, we only needed the distance to the obstacle to calculate when we should brake the car to avoid collision. <br />
Next, we moved to implement the Side-Objects Avoidance System which uses 4 Lidar sensor that is mounted to the sides of the car, front and back. <br />
Once the sensors indicating that an object is to close to one of the sides of the car, the car will steer slightly to the opposite side, if possible, to 
avoid hitting the object from the side. <br />
With those system it is possbile the drive a maze without hitting the walls.
<br />
The next step should have been implementing those kind of systems with Neural Networks-DL, ML and CV, but unfortunetly our PCs we lacking the juice to run
Real-Life enviroments upon AirSim. <br />
That fact made us think about the question - is it possible to implement those kind of systems on an android device.

## Android
We continued out juorney in the Android realm, trying to implement safety systems on an android device. <br />
we started with basic Lane Detection, we indeed were able the detect lanes, we used OpenCV's HughLines but the performance was
disappointing. <br />
Next, we used TFLite for android to detect object. <br /> 
Unfortunetly, we reached the border at this point, We coudn't get real-time performance on our android device, we needed something a little stronger <br />

## Raspberry Pi 4
In search of better hardware we came across the RP4, an Arm-based CPU microcontroller running an linux-like OS <br />
The plan was taking ML and CV to the next level and test it on an RC car <br />
ML and CV algorthims would run on the RP4, than based on the results of the algorthims, an output would be sent to an Arduino or another microcontroller to controll the car. <br />
Out first Experience was DarkNet, an YOLO-based Framework for object detection, getting around 1FPS was far from ideal we switched to Tiny-Yolo which gave us around 3-4 FPS.<br />
Much better than the full-Yolo but not quite enough. <br />
Next we tested TFLite, again with the results of around 4-5 FPS was not quite what we were hoping for. We needed alittle more juice.
<br />
## Jetson
The Jestson is a powerfull machine designed for ML and DL, but this time we wanted to do things diffrently, tweaking and changing the algorithms to run best on our conditions.
Installing and setting up the new Nvidia Jetson Nano was surprisingly time consuming and unintuitive. From protobuf version conflicts, to Tensorflow versions, OpenCV recompiling with GPU, models running, models optimized, and general chaos in the ranks. <br />
Eventually we made the car drive the course and stop at a stop-sign, we coded the software by ourselfs. <br />


#### The End
We started from PC and simulations and ended in real-world embedded, we learned alot and gained both practical and theoretical knowledge and experience. <br />
We spent hours compiling,testing,optimizing and writing code. <br />


