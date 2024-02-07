import mediapipe as mp 
import cv2
import numpy as np
import os
import math 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders

mp_drawing = mp.solutions.drawing_utils # mp components
mp_hands = mp.solutions.hands 

from_email = "geogek10@gmail.com"
to_email = "geogekas10@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587
subject = "Your Drawing!"
pswd = "lsab farp kzew unup"

msg = MIMEMultipart()
msg["From"] = from_email
msg["To"] = to_email
msg["Subject"] = subject

# Define the center and radius of the dot
center = (150, 150)
radius = 5
hand_color = (0, 0, 500)  # Define color
hand_thickness = -1  # Fill the circle
circle_thickness = 30
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1

white = (255, 255, 255)
black = (0, 0, 0)
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)

selected_color = black
selected_scale = 1
saved = False
sent = False

red_x = 50
red_y = 25
green_x = 150
green_y = 25
blue_x = 250
blue_y = 25
white_x = 350
white_y = 25
erase_button_X = 450
erase_button_y = 30
save_button_x = 350
save_button_y = 470
scale_1_x = 50
scale_1_y = 455
scale_2_x = 150
scale_2_y = 455
scale_3_x = 250
scale_3_y = 455
clear_button_x = 500
clear_button_y = 465

cap = cv2.VideoCapture(0) # getting webcam feed. Prosoxi sto (0)
ret = cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
ret = cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
new_coordinates = (0, 0)

# Create a blank canvas with the same dimensions as the image
canvas = np.zeros((int(cap.get(4)), int(cap.get(3)), 3), dtype=np.uint8)

with mp_hands.Hands(False,1,min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:  # hands module
    while cap.isOpened(): # reading through each frame
        ret, frame = cap.read() # frame represents the image
        
        if frame is None:
            continue

        # bgr to rgb
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

        # flip to horizontal
        frame = cv2.flip(frame, 1)
        
        # set flag
        frame.flags.writeable = False

        # Detections
        results = hands.process(frame)
        
        # Set flag
        frame.flags.writeable = True

        # rgb to bgr
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        print(results)

        for i in range(0, 100, 1):
            #cv2.line(image, start_point, end_point, color, thickness) 
            cv2.line(frame, (0, 50-i), (700, 50-i), white, 1)

        for j in range(0, 100, 1):
            cv2.line(frame, (0, 425+j), (700, 425+j), white, 1)

        red_circle = cv2.circle(frame, (red_x, red_y), 5, red, circle_thickness)
        green_circle = cv2.circle(frame, (green_x, green_y), 5, green, circle_thickness)
        blue_circle = cv2.circle(frame, (blue_x, blue_y), 5, blue, circle_thickness)
        white_circle = cv2.circle(frame, (white_x, white_y), 5, white, circle_thickness)
        circle = cv2.circle(frame, (white_x, white_y), 20, black, 1)
        erase_button = cv2.putText(frame, "ERASER", (450, 30), font, fontScale, black, 1)
        scale_1 = cv2.circle(frame, (50, 455), 5, black, 10)
        scale_2 = cv2.circle(frame, (150, 455), 5, black, 20)
        scale_3 = cv2.circle(frame, (250, 455), 5, black, 30)
        save_button = cv2.putText(frame, "SAVE", (350, 470), font, 1.5, black)
        clear_button = cv2.putText(frame, "CLEAR", (500, 465), font, 1, red)

        if saved == True:
            save_button = cv2.putText(frame, "SAVE", (350, 470), font, 1.5, green)

        if sent == True:
            with open(image_path, "rb") as image_file:
                image = MIMEImage(image_file.read(), name="myDrawing.jpg")
                msg.attach(image)

            body = "Hello, NGM Team sends you your masterpiece!"
            msg.attach(MIMEText(body, "plain"))
            sent = False

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(from_email, pswd)
                server.sendmail(from_email, to_email, msg.as_string())

            print("Email sent successfully!")

        # showing results
        if results.multi_hand_landmarks: # check if there are some results
            for num, hand in enumerate(results.multi_hand_landmarks): # loop inside results
                mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS,
                                         mp_drawing.DrawingSpec(color=(0, 22, 500), thickness=2, circle_radius=4),
                                         mp_drawing.DrawingSpec(color=(350, 44, 250), thickness=2, circle_radius=2)
                                         )
                # Get the landmarks of index finger and thumb
                index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]
                middle_tip = hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

                # Calculate the distance between index finger tip and thumb tip
                distance_it = math.sqrt((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2 + (index_tip.z - thumb_tip.z)**2)
                distance_im = math.sqrt((index_tip.x - middle_tip.x)**2 + (index_tip.y - middle_tip.y)**2 + (index_tip.z - middle_tip.z)**2)

                if distance_im < 0.07:
                    coordinates = (int(index_tip.x * canvas.shape[1]) + int(middle_tip.x * canvas.shape[1]))/ 2, (int(index_tip.y * canvas.shape[0]) + int(middle_tip.y * canvas.shape[0]))/ 2
                    print(coordinates)
                    coordinates_x = (int(index_tip.x * canvas.shape[1]) + int(middle_tip.x * canvas.shape[1]))/ 2
                    coordinates_y = (int(index_tip.y * canvas.shape[0]) + int(middle_tip.y * canvas.shape[0]))/ 2
                    if coordinates_x > red_x-15 and coordinates_x < red_x + 15 and coordinates_y > red_y-10 and coordinates_y < red_y+10:
                        hand_color = red
                        print("red")
                        if hand_color == red:
                            red_circle = cv2.circle(image, (red_x, red_y), 7, red, circle_thickness)
                    if coordinates_x > green_x-15 and coordinates_x < green_x + 15 and coordinates_y > green_y-10 and coordinates_y < green_y+10:
                        hand_color = green
                        print("green")
                        if hand_color == green:
                            green_circle = cv2.circle(image, (green_x, green_y), 7, green, circle_thickness)
                    if coordinates_x > blue_x-15 and coordinates_x < blue_x + 15 and coordinates_y > blue_y-10 and coordinates_y < blue_y+10:
                        hand_color = blue
                        print("blue")
                        if hand_color == blue:
                            blue_circle = cv2.circle(image, (blue_x, blue_y), 7, blue, circle_thickness)
                    if coordinates_x > white_x-15 and coordinates_x < white_x + 15 and coordinates_y > white_y-10 and coordinates_y < white_y+10:
                        hand_color = white
                        print("white")
                        if hand_color == white:
                            white_circle = cv2.circle(image, (white_x, white_y), 7, white, circle_thickness)
                            circle = cv2.circle(image, (white_x, white_y), 23, black, 1)
                    if coordinates_x > erase_button_X-15 and coordinates_x < erase_button_X+100 and coordinates_y > erase_button_y-20 and coordinates_y < erase_button_y+10:
                        hand_color = black
                        print("eraser")
                        if hand_color == black:
                          cv2.rectangle(image, (440, 7), (570, 33), black, 1)
                    if coordinates_x > save_button_x-5 and coordinates_x < save_button_x+115 and coordinates_y > save_button_y-25 and coordinates_y < save_button_y+5:
                        cv2.imwrite("myDrawing.jpg", canvas)
                        print("image saved")
                        saved = True
                        sent = True
                        image_path = r"C:\Users\geoge\OneDrive\Έγγραφα\mediapipe-opencv-python\myDrawing.jpg"
                    if coordinates_x > scale_1_x-15 and coordinates_x < scale_1_x+15 and coordinates_y > scale_1_y-15 and coordinates_y > scale_1_y+15:
                        radius = 5
                        print("radius = 5")
                        if radius == 5:
                            scale_1 = cv2.circle(image, (scale_1_x, scale_1_y), 7, black, circle_thickness)
                    if coordinates_x > scale_2_x-15 and coordinates_x < scale_2_x+15 and coordinates_y > scale_2_y-15 and coordinates_y > scale_2_y+15:
                        radius = 10
                        print("radius  = 10")
                        if radius == 10:
                            scale_2 = cv2.circle(image, (scale_2_x, scale_2_y), 7, black, circle_thickness)
                    if coordinates_x > scale_3_x-15 and coordinates_x < scale_3_x+15 and coordinates_y > scale_3_y-15 and coordinates_y > scale_3_y+15:
                        radius = 15
                        print("radius = 15")
                        if radius == 15:
                            scale_3 = cv2.circle(image, (scale_3_x, scale_3_y), 7, black, circle_thickness)
                    if coordinates_x > clear_button_x-5 and coordinates_x < clear_button_x+115 and coordinates_y > clear_button_y-25 and coordinates_y > clear_button_y+5:
                        canvas = np.zeros((int(cap.get(4)), int(cap.get(3)), 3), dtype=np.uint8)

                if distance_it < 0.05:
                    print("Distance is closer than 0.04")
                    coordinates = (int(thumb_tip.x * canvas.shape[1]), int(thumb_tip.y * canvas.shape[0]))
                    print(coordinates)
                    print(cv2.circle(canvas, coordinates, radius, hand_color, hand_thickness))
                    print(cv2.circle(frame, coordinates, 5, hand_color, hand_thickness))
                    

        # Overlay the canvas onto the webcam feed
        image = cv2.addWeighted(frame, 1, canvas, 1, 0)
                
        if cv2.waitKey(10) & 0xFF == ord('r'):
            cv2.imshow('Drawing', canvas)
        else:      
            cv2.imshow('Hand Tracking', image) # 'Hand Tracking' frame name. Command is showing the image
        
        
        if cv2.waitKey(10) & 0xFF == ord('q'): # how to exit
            break
cap.release()
cv2.destroyAllWindows()