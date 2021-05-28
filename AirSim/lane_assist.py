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
idx = 0 




while True: 
    ##### Collecting Data from LIDAR #####
    car_state = client.getCarState()
    print("Speed %d, Gear %d" % (car_state.speed, car_state.gear))
    front_lidarData = client.getLidarData("Emergancy-Brake");
    left_lidarData  = client.getLidarData("Left-Lane_Assist");
    right_lidarData = client.getLidarData("Right-Lane_Assist");
    #print("\t\tlidar position: %s" % (pprint.pformat(front_lidarData.pose.position)))
    print(funcs.far_distance(front_lidarData.point_cloud))
    
    front_dist_3d = funcs.avg_distance(front_lidarData.point_cloud)
    left_dist_3d = funcs.avg_distance(left_lidarData.point_cloud)
    right_dist_3d = funcs.avg_distance(right_lidarData.point_cloud)
    
    ###### PRINTINGS ######
    print("\nfront avg distance from closest obstacle is %s:" % front_dist_3d)
    print("\nleft avg distance from closest obstacle is %s:" % left_dist_3d)
    print("\nright avg distance from closest obstacle is %s:" %right_dist_3d)
    if(front_dist_3d > 20 and right_dist_3d > 2.8 and left_dist_3d > 2.8):
        car_controls.throttle = 0.4
    else :
        car_controls.throttle = 0.3 ####
    car_controls.steering = 0
    client.setCarControls(car_controls)
      
        
    far_point = funcs.far_distance(front_lidarData.point_cloud) # far Y point
    close_point = funcs.close_distance(front_lidarData.point_cloud) # close X point
    
    if right_dist_3d < 2.3:
        while right_dist_3d < 2.3:
            print("Correcting to the left\n")
            car_controls.steering = -0.2
            car_controls.throttle = 0.2
            client.setCarControls(car_controls)
            time.sleep(1.00)   # let car drive a bit
            right_lidarData = client.getLidarData("Right-Lane_Assist");
            right_dist_3d = funcs.avg_distance(right_lidarData.point_cloud)
            #funcs.take_pic(client)

        if left_dist_3d < 2.3:
            funcs.emergancy_brake(client,car_controls)
        
        else :
            car_controls.steering = 0.1
            car_controls.throttle = 0.2
            client.setCarControls(car_controls)
            time.sleep(0.50)   # let car drive a bit

    if left_dist_3d < 2.3:
        while left_dist_3d < 2.3:
            print("Correcting to the right\n")
            car_controls.steering = 0.2
            car_controls.throttle = 0.2
            client.setCarControls(car_controls)
            time.sleep(1)   # let car drive a bit
            left_lidarData  = client.getLidarData("Left-Lane_Assist");
            left_dist_3d = funcs.avg_distance(left_lidarData.point_cloud)
            #funcs.take_pic(client)

        if right_dist_3d < 2.3 :
            funcs.emergancy_brake(client,car_controls)
        
        else :
            car_controls.steering = -0.1
            car_controls.throttle = 0.2
            client.setCarControls(car_controls)
            time.sleep(0.50)   # let car drive a bit  # let car drive a bit

    if (front_dist_3d-((car_state.speed**2)/20) < 13 and car_state.speed > 2 and car_controls.throttle > 0.3):
        funcs.emergancy_brake(client,car_controls)   
        funcs.take_pic(client)
        time.sleep(5.50)

    if ((front_dist_3d+right_dist_3d)/2 < 6 ) or ((front_dist_3d+left_dist_3d)/2 < 6):
        funcs.emergancy_brake(client,car_controls)
        funcs.take_pic(client)
        time.sleep(5.50)    
