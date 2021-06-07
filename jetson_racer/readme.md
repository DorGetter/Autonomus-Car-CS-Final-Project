# How To Run: 

###After the setup stage is complete run the MainDrive.py by the following command: <br />
1. Navigate to the MainDrive.py file location on the jetson racer. <br /> 
2. $python3 MainDrive.py <br />

this code is run on the two cameras: 
1. CSI camera which its purpose is to track and detect objects.  <br /> 
2. USB webcam which connect to the available USB port, which will use to detect the lanes and the track marks. <br /> 
make sure you spacified the right cameras name in the code. <br /> 
The CSI camera is open by the nvidia api, while the USB webcam is used by the OpenCV library ( as cv2.VideoCapture(1) ) . <br /> 
