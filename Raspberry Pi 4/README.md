# Raspberry Pi 4 - TryOut

The Pi 4 is an arm-based cpu microcontroller. <br />
The fact that it runs a unix-like OS makes it good platform for self-driving cars.
<br />
We decide to try using this ebedded device since the Android platform was too week.

<br />
<br />
# The Construction for testing the models on remote control car:
<br />

![image](https://user-images.githubusercontent.com/57401083/120466645-96135d80-c39f-11eb-843f-d1d7b4673d63.png)
<br />
# Object Detection & Lane Ditection Testing:
<br />

![WhatsApp Image 2021-07-27 at 16 44 25](https://user-images.githubusercontent.com/57047863/127165850-76245b4c-9af4-4e48-a631-1c15388d3c2a.jpeg)
<br />
![WhatsApp Image 2021-07-27 at 16 44 30](https://user-images.githubusercontent.com/57047863/127165963-5c32ce41-91a8-4d28-90d3-426b9872af43.jpeg)
<br />
<br />
At first we tried Darknet- an object detecion network based on Yolo V5.
The perforamnce was far from real-time, so we switched to Tiny-Yolo, 4-5FPS was the best we achived, still not good enough for real time applications.

Than we decided to go on TensorFlow lite , still nothing better than 4-5FPS, that's when we decided to juice things up and go for Nvidia's Jetson Nano <br />
