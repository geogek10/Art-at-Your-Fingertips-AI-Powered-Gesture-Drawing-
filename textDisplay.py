import mediapipe as mp
import cv2
import numpy as np
import os
import math 

center = (150, 150)
radius = 5
color = (0, 500, 100) 
thickness = 50 
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (500,0,100)
thickness2 = 1
lineType = 2

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
    
    print(cv2.putText(canvas, 'Hello World', center, font, fontScale, fontColor, thickness2, lineType))

                    

    image = cv2.addWeighted(image, 1, canvas, 1, 0)
                
                
    cv2.imshow('img', image) 
        
        
    if cv2.waitKey(10) & 0xFF == ord('q'): 
        break
cap.release()
cv2.destroyAllWindows()