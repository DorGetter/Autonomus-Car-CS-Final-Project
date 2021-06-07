
import time
from jetracer.nvidia_racecar import NvidiaRacecar

car = NvidiaRacecar()


from subprocess import call 
# car.steering = 0 + 0.1
# car.throttle = 0
x = time.time()
y = x + 60
ste = -7 
j = 0
while(x < y):
	x = time.time()
	print("COMMAND")

	
	thr = call(["./throt"])
	
	ste = call(["./steer"])
	if ste == 0 :
		ste = 1
	else :
		ste = -1
	print(thr)
	print("STE   " , ste)	
	car.steering = ste + 0.1
	if j % 2 ==0 :
		car.throttle = thr
	j+=1
	
car.throttle = 0
exit()
