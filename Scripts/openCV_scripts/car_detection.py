import cv2

cap = cv2.VideoCapture('videos/drive_turn.mp4')
car_cascade = cv2.CascadeClassifier('xmls/cars.xml')

while True:
    ret, frames = cap.read()
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 9)
    # if str(np.array(cars).shape[0]) == '1':
    #     i += 1
    #     continue
    for (x,y,w,h) in cars:
        plate = frames[y:y + h, x:x + w]
        cv2.rectangle(frames,(x,y),(x +w, y +h) ,(0, 255, 0),2)
        cv2.rectangle(frames, (x, y - 40), (x + w, y), (0, 255, 0), -2)
        cv2.putText(frames, 'Car', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow('car',plate)
        print('car found!')
        print('car frame coordinate >>>   [ up left: ', (x, y,), 'down right: ', (x+w, y+h), ']')


    frames = cv2.resize(frames, (600, 600))
    cv2.imshow('Car Detection System', frames)
    # cv2.resizeWindow('Car Detection System', 600, 600)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()