import jetson.inference
import jetson.utils
from jetracer.nvidia_racecar import NvidiaRacecar



def findLaneCenter():
    print("find lane center..")
    # averageLanesPoint()



def stopSignAction():
    print("stop sign action..")
    # checkDistance()
    # speedChange()


def pedestrianAction():
    print("pedestrian action..")
    # checkMovementDirection()
    # checkDistance()
    # speedChange()


def CarAction():
    print("pedestrian action..")
    findLaneCenter()

    # checkDistance()
    # speedChange()








"""
car decision making and control
for autonomous driving and object recognition
"""

# initialize network model format and threshold
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.6)

# initialize jetson camera
cam = jetson.utils.gstCamera(1280, 720, "csi://0")

# initialize display window
Disp = jetson.utils.glDisplay()

# initialize car speed and steering
car = NvidiaRacecar()
car.steering = 0 + 0.1
car.throttle = 0.4

while Disp.IsOpen():
    car.steering = 0 + 0.1

    # get the camera frame
    Img, width, hei = cam.CaptureRGBA()
    # get each object which detected data
    detection = net.Detect(Img, width, hei)
    flag = False
    for detect in detection:
        print(detect)

        # if stop sign detected id=13 stop the car
        if detect.ClassID == 13:
            print("Stop Sign Detected")
            stopSignAction()

        elif detect.ClassID == 1:
            print("Detecting Pedestrian")
            pedestrianAction()

    Disp.RenderOnce(Img, width, hei)
    Disp.SetTitle("Camera")

car.throttle = 0
print("car stopped")