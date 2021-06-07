import cv2 as cv
from jetracer.nvidia_racecar import NvidiaRacecar
import numpy as np

import jetson.inference
import jetson.utils
import time

glob_steer = 0


def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    `initial_img` should be the image before any processing.
    The result image is computed as follows:
    initial_img * α + img * β + λ
    NOTE: initial_img and img must be the same shape!
    """
    return cv.addWeighted(initial_img, α, img, β, λ)


def detect_line_segments(cropped_edges):
    # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
    rho = 1  # distance precision in pixel, i.e. 1 pixel
    angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
    min_threshold = 19  # minimal of votes
    line_segments = cv.HoughLinesP(cropped_edges, rho, angle, min_threshold,
                                   np.array([]), minLineLength=50, maxLineGap=9)

    return line_segments


def make_points(frame, line, bool):
    height, width, _ = frame.shape
    slope, intercept = line

    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]


def average_slope_intercept(frame, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    lane_lines = []
    if line_segments is None:
        print('No line_segment segments detected')
        return lane_lines


    height, width, _ = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1 / 3
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary  # right lane line segment should be on left 2/3 of the screen

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                # print('skipping vertical line segment (slope=inf): %s' % line_segment)
                continue

            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]

            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))

            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average, True))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average, False))

    # print('lane lines: %s' % lane_lines)  # [[[316, 720, 484, 432]], [[1009, 720, 718, 432]]]

    return lane_lines


def display_lines(frame, lines, line_color=(0, 0, 255), line_width=20):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                # print('x1 = ', x1, 'y1 = ', y1, 'x2 = ', x2, 'y2 = ', y2)
                cv.line(line_image, (x1, y1), (x2, y2), line_color, line_width)

    line_image = cv.addWeighted(frame, 0.8, line_image, 1, 1)

    height, width, chan = line_image.shape
    # print(width, height, chan)
    line_image = cv.circle(line_image, (width // 2, height - 50), 2, (255, 0, 0), 60)

    # print("image diemations ", line_image.shape)
    if (len(lines) == 2):
        x1L, y1L, x2L, y2L = lines[0][0]
        x1R, y1R, x2R, y2R = lines[1][0]

        slope_L = (x2R - x1R) / (y2R - y1R)
        slope_R = (x2L - x1L) / (y2L - y1L)
        # print(slope_L, slope_R)
        line_image = cv.circle(line_image, (x1R, y1R), 2, (255, 0, 0), 20)
        line_image = cv.circle(line_image, (x2R, y2R), 2, (255, 0, 0), 20)
        line_image = cv.circle(line_image, (x1L, y1L), 2, (0, 255, 0), 20)
        line_image = cv.circle(line_image, (x2L, y2L), 2, (0, 255, 0), 20)

        slope_avg = slope_R - slope_L
        steering = -(slope_avg) / 10
        car.steering = steering
        # print("slope L ", slope_L, " slope R ", slope_R, " steering ", steering)
        cv.putText(frame, "steering: " + str(steering), (400, 200), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        if steering > 0.2:
            cv.putText(line_image, "Go Left |<-| ", (50, 70), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        elif steering < -0.2:
            cv.putText(line_image, "Go Right |->| ", (50, 70), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 250, 255), 2)
        else:
            cv.putText(line_image, "Go Straight |^| ", (50, 70), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 250, 255), 2)





    elif (len(lines) == 1):

        x1L, y1L, x2L, y2L = lines[0][0]
        slope = (x2L - x1L) / (y2L - y1L)
        cv.putText(frame, "slope: " + str(slope), (100, 300), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        steering = (slope / 10)
        steering_up = steering * (3.6)

        if slope < 0:
            # Only left line detected
            if x1L > width //2:
                steering_up = -1
        elif slope > 0:
            if x1L < width // 2:
                steering_up = 1

        car.steering = steering_up
        # print("steering org  ", steering, " actual steering ", steering_up)
        cv.putText(line_image, "steering: " + str(steering_up), (400, 200), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        if steering_up > 0.2:
            cv.putText(line_image, "Go Left |<-| ", (50, 70), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        elif steering_up < -0.2:
            cv.putText(line_image, "Go Right |->| ", (50, 70), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 250, 255), 2)
        else:
            cv.putText(line_image, "Go Straight |^| ", (50, 70), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 250, 255), 2)

    # -0.2625  actual steering  -0.5775000000000001
    # (480, 640, 3) image dim.

    return line_image


def region_of_interest(edges):
    height, width = edges.shape
    mask = np.zeros_like(edges)

    # only focus bottom half of the screen
    polygon = np.array([[
        (0, height * 1 / 4),
        (width, height * 1 / 4),
        (width, height),
        (0, height),
    ]], np.int32)

    cv.fillPoly(mask, polygon, 255)
    cropped_edges = cv.bitwise_and(edges, mask)
    line_image = np.copy(cropped_edges)
    line_image = cv.circle(line_image, (0, int(height * 1 / 4)), 2, (255, 0, 0), 60)
    line_image = cv.circle(line_image, (width, int(height * 1 / 4)), 2, (255, 0, 0), 60)
    line_image = cv.circle(line_image, (width, height), 2, (255, 0, 0), 60)
    line_image = cv.circle(line_image, (0, height), 2, (255, 0, 0), 60)

    # cv.imshow('cropped_egdes', line_image)
    return cropped_edges


# define a range of black color in HSV

lower_black = np.array([0, 0, 0])
upper_black = np.array([227, 100, 70])

# Rectangular Kernel
rectKernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))

if __name__ == '__main__':
    is_stopped = False
    stop_sign = False
    timer = time.time()
    cap = cv.VideoCapture(1, cv.CAP_V4L)
    net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.6)
    cam = jetson.utils.gstCamera(640, 480, "csi://0")

    print('Started')
    car = NvidiaRacecar()

    car.throttle = 0.4

    ret, frame = cap.read()

# commencing subtraction
    while cap.isOpened():
        Img, width, hei = cam.CaptureRGBA()
        detection = net.Detect(Img, width, hei)
    # apply some gaussian blur to the image

        kenerl_size = (3, 3)

        gauss_image = cv.GaussianBlur(frame, kenerl_size, 0)

        # here we convert to the HSV colorspace

        hsv_image = cv.cvtColor(gauss_image, cv.COLOR_BGR2HSV)

        # apply color threshold to the HSV image to get only black colors
        cv.imshow('hsv ', hsv_image)

        #  thres_1 = cv.inRange(hsv_image, lower_black, upper_black)
        # cv.imshow('thres', thres_1)

        pts1 = np.float32([[110, 50], [530, 50], [10, 300], [630, 300]])
        pts2 = np.float32([[0, 0], [640, 0], [0, 480], [640, 480]])

        matrix = cv.getPerspectiveTransform(pts1, pts2)
        warp_img = cv.warpPerspective(hsv_image, matrix, (640, 640))
        cv.imshow('warp_img', warp_img)



        lowerWhite = np.array([4, 45, 45])
        upperWhite = np.array([15, 255, 255])
        thres_1 = cv.inRange(warp_img, lowerWhite, upperWhite)
        cv.imshow('threshold', thres_1)

        # dilate the the threshold image

        thresh = cv.dilate(thres_1, rectKernel, iterations=1)
        cv.imshow('dilate ', thresh)
        # apply canny edge detection
        low_threshold = 50  # 200
        high_threshold = 150  # 400

        # canny_edges = cv.Canny(gauss_image, low_threshold, high_threshold)
        canny_edges = cv.Canny(thres_1, low_threshold, high_threshold)
        # get a region of interest

        roi_image = region_of_interest(canny_edges)
        cv.imshow('roi ', roi_image)
        line_segments = detect_line_segments(roi_image)

        lane_lines = average_slope_intercept(frame, line_segments)
        if lane_lines is not None:
            lane_lines_backup = lane_lines
        if lane_lines is None:
            lane_lines = lane_lines_backup


# overlay the line image on the main frame
        line_image = display_lines(frame, lane_lines)

# cv.imshow('Frame', frame)

        # cv.imshow('Roi Image', roi_image)
        for detect in detection:
            if detect.ClassID == 13 or detect.ClassID == 1: # stop sign = 13
                stop_sign = True
                if detect.ClassID == 13:
                    cv.putText(line_image, "Detecting Stop Sign", (40, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 67, 255), 2)
                if detect.ClassID == 1:
                    cv.putText(line_image, "Detecting Pedestrian!", (40, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5,(255, 67, 255), 2)
                if not is_stopped:
                    is_stopped = True
                    car.throttle = 0
                    timer = time.time()
                    forward = timer + 20
                    print("Forword - &&&&&&&&&&&&&&&&&&&&&&&&& " , forward )

            timer = time.time()

            if stop_sign:
                print("time Current - $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ", timer)
                if timer > forward:
                    car.throttle = 0.4

                    is_stopped = False
                    stop_sign = False

            if detect.ClassID == 3:  # car = 3
                cv.putText(line_image, "Detecting Car", (400, 400), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 156, 255), 2)
                #car.throttle = 0
                car.throttle = 0.44

        cv.imshow('Line Image', line_image)

        ret, frame = cap.read()

        keyboard = cv.waitKey(30)
        if keyboard == 'q' or keyboard == 27:
            break

# cleanup
    cap.release()
    car.throttle = 0

    cv.destroyAllWindows()
    print('Stopped')

