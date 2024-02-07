import mediapipe as mp
import cv2
import numpy as np
import os
import math 

center = (150, 150)
coordinates = (300, 50)
radius = 10
color = (255, 255, 255) 
thickness = 50 
font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fontScale = 1
fontColor = (500,0,100)
thickness2 = 1
lineType = 2
path = r'"C:\Users\geoge\OneDrive\Έγγραφα\mediapipe-opencv-python\lego_face_happy.jpg"'
i = 0

cap = cv2.VideoCapture(0) 

canvas = np.zeros((int(cap.get(4)), int(cap.get(3)), 3), dtype=np.uint8)

while cap.isOpened():
    ret, frame = cap.read() 
        
    if frame is None:
        continue

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

    image = cv2.flip(image, 1)
        
    image.flags.writeable = False
        
    image.flags.writeable = True

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    print(cv2.putText(canvas, 'Hello World', coordinates, font, fontScale, fontColor, thickness2, lineType))
    for i in range(0, 100, 1):
        #cv2.line(image, start_point, end_point, color, thickness) 
        cv2.line(canvas, (0, 100-i), (700, 100-i), color, thickness2)

    cv2.circle(canvas, (50, 50), radius, (0, 0, 255), 50)

    image = cv2.addWeighted(image, 1, canvas, 1, 0)
                
    cv2.imshow('Hand Tracking', canvas) 
        
        
    if cv2.waitKey(10) & 0xFF == ord('q'): 
        break
cap.release()
cv2.destroyAllWindows()