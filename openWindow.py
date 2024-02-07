import mediapipe as mp
import cv2
import numpy as np
import uuid
import os

mp_drawing = mp.solutions.drawing_utils #mp components
mp_hands = mp.solutions.hands 

cap = cv2.VideoCapture(0) # getting webcam feed. Prosoxi sto (0)
while cap.isOpened(): # reading through each frame
    ret, frame = cap.read() # frame represents the image

    cv2.imshow('Hand Tracking', frame) # 'Hand Tracking' frame name. In general showing the image

    if cv2.waitKey(10) & 0xFF == ord('q'): #how to exit
        break
cap.release()
cv2.destroyAllWindows()
