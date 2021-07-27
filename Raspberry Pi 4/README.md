# Raspberry Pi 4 - TryOut

The Pi 4 is an arm-based cpu microcontroller. <br />
The fact that it runs a unix-like OS makes it good platform for self-driving cars.
![image](https://user-images.githubusercontent.com/57401083/120466645-96135d80-c39f-11eb-843f-d1d7b4673d63.png)
<br />

At first we tried Darknet- an object detecion network based on Yolo V5.
The perforamnce was far from real-time, so we switched to Tiny-Yolo, 4-5FPS was the best we achived, still not good enough for real time applications.

Than we decided to go on TensorFlow lite , still nothing better than 4-5FPS, that's when we decided to juice things up and go for Nvidia's Jetson Nano <br />
