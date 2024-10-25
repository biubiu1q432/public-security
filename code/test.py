import cv2



#录像
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (300,200)) 

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

