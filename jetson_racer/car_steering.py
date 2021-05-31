from jetracer.nvidia_racecar import NvidiaRacecar
import time

"""

simple jetson racer car steering control interface test

"""

# initialize the car control
car = NvidiaRacecar()

# turn the car steering right
car.steering = -1
time.sleep(1.4)

# turn the car steering left
car.steering = 1
time.sleep(1.4)

# staight steering with a little fix
car.steering = 0 + 0.1
time.sleep(3)




print("script endded")
