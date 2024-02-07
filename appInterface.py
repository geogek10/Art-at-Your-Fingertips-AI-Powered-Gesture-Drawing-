import mediapipe as mp
import cv2
import numpy as np
import os

cap = cv2.VideoCapture(0) 

start_point = (0, 50)
end_point = (1000, 50)
color = (500, 0, 0)
thickness = 1

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
    
    #cv2.line(image, start_point, end_point, color, thickness) 
    cv2.line(canvas, start_point, end_point, color, thickness)
    cv2.circle(canvas, (0,480), 2, color, 100)
    cv2.circle(canvas, (0,0), 2, color, 100)
    cv2.line(canvas, (0,400), (1000, 400), color, thickness)

    height, width, channels = canvas.shape

    # Print the dimensions
    print("Height:", height)
    print("Width:", width)
    print("Number of Channels:", channels)

    image = cv2.addWeighted(image, 1, canvas, 1, 0)
                
    cv2.imshow('Hand Tracking', canvas) 
        
        
    if cv2.waitKey(10) & 0xFF == ord('q'): 
        break
cap.release()
cv2.destroyAllWindows()