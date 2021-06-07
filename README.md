<br /># Final Project

## Autonomous Driving System On Varoius Platforms 

### participants: 
Dor Getter <br />
Eldar Takach <br />
Oren Lacker <br />


### Overview 
In this project we examined and exprinenced various automonous driving systems on various platforms. <br />
At first, we worked with Microsoft's AirSim, An realistic open world driving simulator. <br />

#### Setup
1. link to the simulator github - https://github.com/microsoft/AirSim.
2. link to airsim site -  https://microsoft.github.io/AirSim/. 

<br />

### AIR SIM - real world simulation.

The AirSim simulator can Simulate various sensors, cameras and scenarios. <br />
We implemented our own "Auto-Pilot" system - Lane Assist and Auto Emergancy Brake based on data we recieved from sensors such as Lidar, front camera and more. 
later on we tested our algorithm on a custome made maze that we built and the objective was that the car will complete the maze by make turning desicions and avoid obstacales.
on our attempts we also write an akgorithm for self parking feature. <br />
<br />


![Emergancybrake](https://user-images.githubusercontent.com/57401083/119956114-08033580-bfa1-11eb-840a-dd5df808e5ee.gif)


<br />

### Android application

After understanding the concepts of the autononous driving on a simulator, we moved on to the real world <br />
Our next step was implementing those systems on an mobile android platform, we sucsessfully managed to detect lane and objects. <br />

#### Setup
1. android studio installation  <br />
https://developer.android.com/studio/install  <br />
2.  opencv sdk library for android studio <br />
https://medium.com/android-news/a-beginners-guide-to-setting-up-opencv-android-library-on-android-studio-19794e220f3c




![WhatsApp Image 2021-05-28 at 10 45 08](https://user-images.githubusercontent.com/57401083/119958917-c58f2800-bfa3-11eb-88db-2244a403dde7.jpeg)


<br />

### Raspberry Pie 4 

We continued our journey in the embedded world, we tried to implement those system on a RP4 platform , than test it on a RC car and a track, 
unfortunetly the RP4 was lacking the hardware to drive the car in realtime. <br />

#### Setup

1. To start working with jetson-nano, first download the Raspian OS. <br />
   https://www.raspberrypi.org/documentation/installation/installing-images/ <br />
2. Download OpenCV for RP4. <br />
   https://learnopencv.com/install-opencv-4-on-raspberry-pi/ <br /> 
3. Install Python 3.7 or higher version. <br />
   https://projects.raspberrypi.org/en/projects/generic-python-install-python3 <br />
4. Install Numpy, Scipy and matplotlib <br />
   https://www.programmersought.com/article/30944423335/ <br />

<br />


![image](https://user-images.githubusercontent.com/57401083/120466645-96135d80-c39f-11eb-843f-d1d7b4673d63.png)

![RP4_Lane](https://user-images.githubusercontent.com/57187365/120918184-c0289080-c6bb-11eb-8a48-662db10c40e2.jpeg)


<br />

### Nvidia Jetson Racer 

Since better performace was needed, we switched the Nvidia's Jetson Nano, a powerfull embedded system. <br />

#### Setup

1. To start working with jetson-nano, first complete the "Software Setup" (download the operation system image and complete the instructions). <br />
   https://github.com/waveshare/jetracer/blob/master/docs/software_setup.md <br />
2. To start working with the jetracer car it is necessary to setup the "jetracer" lib (enable python interface to manage the car controlers). <br />
   https://github.com/waveshare/jetracer <br /> 
3. Jetson-Inference instructional guide (to enable deep-learning include object detection). <br />
   https://github.com/dusty-nv/jetson-inference/

<br />

![WhatsApp Image 2021-05-30 at 18 31 42](https://user-images.githubusercontent.com/57047863/120110552-941a8600-c176-11eb-8cf9-af498cf963a2.jpeg)

![WhatsApp Image 2021-05-30 at 18 31 05](https://user-images.githubusercontent.com/57047863/120110584-b3191800-c176-11eb-8047-42890adbcf83.jpeg)

![WhatsApp Image 2021-05-30 at 18 31 05 (1)](https://user-images.githubusercontent.com/57047863/120110593-c1673400-c176-11eb-923e-b33c32021dea.jpeg)


<img width="749" alt="y" src="https://user-images.githubusercontent.com/57047863/120109769-8b748080-c173-11eb-9004-8af2cc07e8f1.png">


![Hnet-image (1)](https://user-images.githubusercontent.com/57187365/120111570-160cae00-c17b-11eb-9294-d9c78228fca1.gif)
![Hnet-image](https://user-images.githubusercontent.com/57187365/120111636-61bf5780-c17b-11eb-85e9-2967cf693b75.gif)


### Conclustions
The question that we had in mind doing this project is if it is possible to develop an cross-platform application that would be able the drive cars
autonomously, a piece of sftware that can be installed on a microprocessor such as raspberrt pi, mobile android device and a desktop PC.<br />
the answer is - it depends.
<br />
While there are some light softwares that enables basic autonomous cababilities, it is not reliable and cannot be used in the real world.





