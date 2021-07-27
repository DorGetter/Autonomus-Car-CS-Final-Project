#Autopilot Functions for AirSim.

import setup_path 
import airsim
import time
import os
idx = 0 
def emergancy_brake(client,car_controls):
    client.enableApiControl(True)
    print("Emergancy Braking Activated!!")
    car_controls.brake = 1
    car_controls.throttle = 0
    client.setCarControls(car_controls)
    time.sleep(2)   # let car drive a bit
    #client.enableApiControl(False)
    
#measure the avg distance to the closeest obstacle from each lidar
def avg_distance(point_cloud):
    point_3d = 0
    for i in range(0,len(point_cloud)-3,3):
        
        point_x = point_cloud[i]
        point_y = point_cloud[i+1]
        point_z = point_cloud[i+2]

        formula = (point_x**2+point_y**2+point_z**2)**0.5
        point_3d += formula

    front_dist_3d = point_3d/(len(point_cloud)/3)
    return front_dist_3d

#measure the distace to the farest point for the obstacle of each lidar
def far_distance(point_cloud):
    point = 0
    most_far = 0
    for i in range(0,len(point_cloud)-3,3):
        
        point_y = point_cloud[i+1]
        point+=point_y
    most_far = point/(len(point_cloud)/3)
    return most_far

#measure the distace to the closeset point for the obstacle of each lidar
def close_distance(point_cloud):
    point_3d = 0
    most_close = 99
    for i in range(0,len(point_cloud)-3,3):
        
        point_x = point_cloud[i]
        if most_close > point_x :
            most_close = point_x

    return most_close

#takes a pic from the cameras and save 
def take_pic(client):
    global idx 
    
    responses = client.simGetImages([airsim.ImageRequest("1", airsim.ImageType.Scene),
                                     airsim.ImageRequest("2", airsim.ImageType.Scene),
                                     airsim.ImageRequest("3", airsim.ImageType.Scene),])  
    for response in responses:
        idx+=1
        filename = 'C:/Users/Eldar/AirSim/PythonClient/log/py' + str(idx)
        if not os.path.exists('C:/Users/Eldar/AirSim/PythonClient/log/'):
            os.makedirs('C:/Users/Eldar/AirSim/PythonClient/log/')

        if response.compress: #png format
            print("Image Captured : Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)

#log the car stats            
def log_it(client):
    car_state = client.getCarState()
    speed = car_state.speed
    gear = car_state.gear
    position = car_state.position

"""
    ##### Avg point from front Sensor #####
    for i in range(0,len(front_lidarData.point_cloud)-3,3):
        
        point_x = front_lidarData.point_cloud[i]
        point_y = front_lidarData.point_cloud[i+1]
        point_z = front_lidarData.point_cloud[i+2]

        formula = (point_x**2+point_y**2+point_z**2)**0.5
        if formula < front_closest_point:
            front_closest_point = formula
        point_3d += formula

    front_dist_3d = point_3d/(len(front_lidarData.point_cloud)/3)

    ##### Avg point from left Sensor #####
    point_3d = 0
    for i in range(0,len(left_lidarData.point_cloud)-3,3):
        
        point_x = left_lidarData.point_cloud[i]
        point_y = left_lidarData.point_cloud[i+1]
        point_z = left_lidarData.point_cloud[i+2]

        point_3d += (point_x**2+point_y**2+point_z**2)**0.5
    left_dist_3d = point_3d/(len(left_lidarData.point_cloud)/3)

    ##### Avg point from right Sensor #####
    point_3d = 0
    for i in range(0,len(right_lidarData.point_cloud)-3,3):
        
        point_x = right_lidarData.point_cloud[i]
        point_y = right_lidarData.point_cloud[i+1]
        point_z = right_lidarData.point_cloud[i+2]

        point_3d += (point_x**2+point_y**2+point_z**2)**0.5

    right_dist_3d = point_3d/(len(right_lidarData.point_cloud)/3)
"""
