<br /># Final Project

## Autonomous Driving System On Varoius Platforms 

### participants: 
Dor Getter <br />
Eldar Takach <br />
Oren Lacker <br />


### Overview 
In this project we examined and exprinenced various automonous driving systems on various platforms. <br />
At first, we worked with Microsoft's AirSim, An realistic open world driving simulator. <br />
##### The project life cycle: 

###### Air Sim simulator: 
We began our project by first dip our feets in the world of autonomous driving using the AIR-SIM simulator ( link to the software below ), 
in which we explore how to control the car in the simulator by using sensors such as Lidars <br /> ( link to interesting articale about lidars and autonomus-car https://www.automotiveworld.com/articles/lidars-for-self-driving-vehicles-a-technological-arms-race/) <br /> and cameras. We implemened the basic ideas such as self parking, maze oriantation, obstacle avoidanse and decision making in cross roads and creating an simulation envarioment to put to the test our code and algorithms.  
####### Conclusions 
The conclusions from this expireance was that the lidar system we need to implement this self-driving car using the lidars is expencive and new approach is needed, moreover this allows us to work with Json, C++ and Python which we not used in our scope of the degree , we stop exploring this platform since the computation power of our machines was not enogh when the envarionment started to be complicated. 

Its important to say thaא installing this simulator is quite challenging and time consuming, both in that the maintenance of the simulator is not so up to date and also because its installation on Windows requires prior knowledge of working with this operating system regarding permissions and more.

###### Udemy Course: 
As we neglected the lidar system for simulate the envarioment and we explore the web for camera based system to operate the self-driving car we encounter a course in Udemy (https://www.udemy.com/share/101WswAEcaeFpaRnoC/) which we learn how to implement image processing techniqes to detect the lane marks (using Hough transform and more) and builf Keras based deep-learning neural network for detecting objects in frames and also create a .h5 (Keras) model to predict the car steering, using the Udacity simulator which we used to gather data for the model training and test our model.  


###### Android Apllication - Phone: 
Then we explore the idea of using an android phone to serve as a stand alone device for this task of self-driving car. We look on some amazing technological inventions such as comma ai which implement this idea ( https://comma.ai/ ) using a custome made phone for this task. For exploring this idea of using only a phone to be able to create a self-driving car we first got familiar with the android studio IDE we explore how to use the phone camera and get frames to process, develope an api for the use and more. 
We been able to run tensorflow lite application for object detection and after a object detection model using Keras to detect cars and padestrains. 
Then we try to use OpenCV SDK library to be able to detect the driving lanes by using image processing techniqs such as hough line transform which we learn in the course we took, this was challanging since the OpenCV in the android studio is implemet in Java instead of python or C++ that we used before. 
To give our car the abillity to get a steering prediction based on the frames that captured by the phone's back camera we tried to combined the .h5 Keras model we construct in the course and the object detection model ( Tensorflow Lite ).
####### Conclusions 
The results of combining the two models together created an app that was very laggy and therefore unreliable for further progress in this layout. from an exploration that we made the solution for this problem was to dive in to the architacture of the hardware of the phone in order to make this kind of use relaiable. 
Another approach we made is use different models to try achiving less laggy performances such as use the Yolo models but with luck. 

##### Raspberry Pie 4:
Proceeding our goal to make this self-driving car run on embedded platform we began to use the Raspberry Pi 4 as our processing unit. 
This was the first time any of us work on an embedded hradware so installation and setup the envarionment was challanging and very time consuming. 
We first tried to run our previous models we implemented on our android device, but the results remained very laggy and not suitable for real-time performance. 
So to make things run faster we started to seek for optimized sulotions for object detection and lane detection models such as using YOLOv5s,YoloV4s... mobileNetSSD, DarkNet TensorFlow Lite, and Yolo tiny. The first FPS output was 0.4FPS for detecting only one class and as an end result we were able to make a detection model thats runs in 5-8FPS using the TensorFlow lite model and overclocking the Raspberry. As those results not really suitable for realtime application we explore ways to make this detection models run even faster and came across the TPU solution but this wasnt implemented as this TPU does not shipped to Isreal. 
####### Conclusions 
A fater more caclcultion power proccessing unit was needed in order to get our FPS higher which include a TPU or GPU configuration. 
The .h5 model we created was obsolete to this task because the computation power needed to run the neural network so a image proccessing solution was needed. 

##### Jetson Nano - Using the Jetson DonkeyCar Kit:
Moving to the Jetson Nano unit was very challanging because we had to use the Nvidia OS and libraries which was a bit challanging since the documantion is lack.
We started to get to know this machine by first building the car itself, and then go to the software setup. we came acrooss some challanging setups such as upgrading libraries and custome create our oun python3 envarionment. 
After installtaion and setup complete we started to try different approaches to lanes detection based on the privious lane detection we usen on our RP4. This was not very good as the lanes not detected properly so new approach was implemented using warp image, hough lines, color seperation, and Gstream to make the FPS faster and close to real-time.
Also we try our preiviosly YOLO and TensorFLow lite models which were not produced fast enough FPS ( 8-12 FPS ) So new approach was needed in this field as well. Finally using the Nvidia tools and TRT we made a object detection model which was able to detecet 80 classes Using SSD-mobileNetV2 and the COCO data set in Frame rate of ~30 Fps. 

Then we combined those to models into a single file MainDrive.py which able to make the car run the course autonomously detect object and obsticals, stop at a stop sign and alert using a messege on the screen about padestrains. 






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




####### TODO next: 
1. implement a decision making  based on padestrain detection and obstacles and to be able to correspond to this hazards. 
2. an addaptive cruise contol. 


