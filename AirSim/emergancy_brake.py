import setup_path 
import airsim
import funcs
import time
import pprint

# connect to the AirSim simulator 
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()
print("OK TEST")


while True: 
    ##### Collecting Data from LIDAR #####
    car_state = client.getCarState()
    car_controls.throttle = 1.0
    car_controls.brake = 0
    client.setCarControls(car_controls)
    front_lidarData = client.getLidarData("Emergancy-Brake");
    front_dist_3d = funcs.avg_distance(front_lidarData.point_cloud)
    #time.sleep(0.50)   # let car drive a bit  # let car drive a bit
    if(front_dist_3d-((car_state.speed**2)/20)) < 13:
        funcs.emergancy_brake(client,car_controls)  
        time.sleep(0.50)

    
