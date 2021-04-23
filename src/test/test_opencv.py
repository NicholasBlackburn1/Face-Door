
import cv2

cap = cv2.VideoCapture('rtspsrcsynk location=rtsp://192.168.1.17:8080/h264_ulaw.sdp ! decodebin ! gtksink')
ret,frame = cap.read()

while(True):

    ret, frame = cap.read()
    #img = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

    cv2.imshow('Stream IP Camera OpenCV',frame)
    cv2.imshow('Small',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()





