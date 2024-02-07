import mediapipe as mp # the ai we are using for this project
import cv2 # OpenCv is the tool we use for image processing and performing computer vision tasks
import numpy as np # We use numpy functions to create and analyze numpy arrays. e.g we can create a canvas to work with
import os # OS module provides easy functions that allow us to interact and get Operating System information and even control processes up to a limit.
import math # library for doing math operations
# used for sending emails
import smtplib # creates the connection
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText # reads text
from email.mime.image import MIMEImage # reads images
from email import encoders # encodes our message

# function for creating the UI(User Interface)
def interface():
    # this loop draws a white area at the top of the screen
    for i in range(0, 100, 1):
            #cv2.line(image, start_point, end_point, color, thickness) 
            cv2.line(frame, (0, 50-i), (1500, 50-i), white, 1)

    # this loop creates a white are in the bottom of the screen
    for j in range(0, 100, 1):
        cv2.line(frame, (0, 600+j), (1500, 600+j), white, 1)

    # color pick
    red_circle = cv2.circle(frame, (red_x, red_y), 5, red, circle_thickness)
    green_circle = cv2.circle(frame, (green_x, green_y), 5, green, circle_thickness)
    blue_circle = cv2.circle(frame, (blue_x, blue_y), 5, blue, circle_thickness)
    white_circle = cv2.circle(frame, (white_x, white_y), 5, white, circle_thickness)
    circle = cv2.circle(frame, (white_x, white_y), 20, black, 1)
    # eraser
    erase_button = cv2.putText(frame, "ERASER", (erase_button_x, erase_button_y), font, fontScale, black, 1) 
    # scale pick
    scale_1 = cv2.circle(frame, (scale_1_x, scale_1_y), 5, black, 10)
    scale_2 = cv2.circle(frame, (scale_2_x, scale_2_y), 5, black, 20)
    scale_3 = cv2.circle(frame, (scale_3_x, scale_3_y), 5, black, 30)
    # save and clear button
    save_button = cv2.putText(frame, "SAVE", (save_button_x, save_button_y), font, 1.5, black) 
    clear_button = cv2.putText(frame, "CLEAR", (clear_button_x, clear_button_y), font, 1, red)

# Mp components. Hand recognising
mp_drawing = mp.solutions.drawing_utils # mp components
mp_hands = mp.solutions.hands 

radius = 5 # default radius for drawing circles
hand_color = (0, 0, 500)  # color in use
hand_thickness = -1  # Fill the circle
circle_thickness = 30 # circle thickness
# font variables
font = cv2.FONT_HERSHEY_SIMPLEX 
fontScale = 1

white = (255, 255, 255)
black = (0, 0, 0)
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)

saved = False # variable for letting us know if our drawing saved successfully

# coordinates for UI's elements
red_x = 100
red_y = 25
green_x = 250
green_y = 25
blue_x = 400
blue_y = 25
white_x = 550
white_y = 25
erase_button_x = 750
erase_button_y = 35
save_button_x = 680
save_button_y = 650
scale_1_x = 200
scale_1_y = 630
scale_2_x = 350
scale_2_y = 630
scale_3_x = 500
scale_3_y = 630
clear_button_x = 900
clear_button_y = 640

ngm_path = 'ngm.jpg'

ngm_image = cv2.imread("ngm.jpg") # path for ngm logo image

# variables needed to calculate were to draw
width = 1800
height = 900
new_coordinates = (0,0)
past_coordinates = (0,0)

cap = cv2.VideoCapture(0) # getting webcam feed. In this specific situation we are setting for our camera the laptop built in cam 
# resizing the window's dimensions
ret = cap.set(cv2.CAP_PROP_FRAME_WIDTH,width) 
ret = cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)

# Create a blank canvas with the same dimensions as the image
canvas = np.zeros((height, width, 3), np.uint8)

with mp_hands.Hands(False,1,min_detection_confidence=0.4, min_tracking_confidence=0.4) as hands:  # we "tell" the ai to recognise only one hand and only if it is (the ai) 40% sure 
    while cap.isOpened(): # reading through each frame
        ret, frame = cap.read() # frame represents the image from the webcam feed
        
        # checking if frame exists
        if frame is None:
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) 

        results = hands.process(frame)

        interface()

        cv2.circle(frame, (white_x+20, white_y), radius, black, hand_thickness)

        # the user can see how their drawing looks like on the canvas, mid-drawing
        if cv2.waitKey(10) & 0xFF == ord('r'):
            cv2.imshow('Drawing', canvas)

        # UI characteristic
        if saved == True:
            save_button = cv2.putText(frame, "SAVE", (350, 470), font, 1.5, green)

        if results.multi_hand_landmarks: # check if there are some results
            for num, hand in enumerate(results.multi_hand_landmarks): # loop inside results
                mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(0, 22, 500), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(350, 44, 250), thickness=2, circle_radius=2)
                                            ) 
                index_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]
                middle_tip = hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

                # get the coordinates(x,y) of every fingertip
                index_tip_x = round(index_tip.x * width)
                index_tip_y = round(index_tip.y * height)
                thumb_tip_x = round(thumb_tip.x * width)
                thumb_tip_y = round(thumb_tip.y * height)

                # getting the averages of the x and y of the two fingetips and then we can have the average coordinates
                it_coordinates_x = abs((index_tip_x - thumb_tip_x) / 2)
                it_coordinates_y = abs((index_tip_y - thumb_tip_y) / 2)

                # Calculate the distance between index finger tip and thumb tip
                distance_it = math.sqrt((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2 + (index_tip.z - thumb_tip.z)**2)
                distance_im = math.sqrt((index_tip.x - middle_tip.x)**2 + (index_tip.y - middle_tip.y)**2 + (index_tip.z - middle_tip.z)**2)

                if it_coordinates_x < 20 and it_coordinates_y < 20:
                    new_coordinates = (round((index_tip_x + thumb_tip_x) / 2), round((index_tip_y + thumb_tip_y) / 2))

                    if past_coordinates == (0,0):
                        past_coordinates = new_coordinates

                    cv2.line(canvas, past_coordinates, new_coordinates, hand_color, radius)

                    past_coordinates = new_coordinates
                else: 
                    past_coordinates = (0,0)

                if distance_im < 0.07:
                    coordinates = (int(index_tip.x * canvas.shape[1]) + int(middle_tip.x * canvas.shape[1]))/ 2, (int(index_tip.y * canvas.shape[0]) + int(middle_tip.y * canvas.shape[0]))/ 2
                    coordinates_x = (int(index_tip.x * width) + int(middle_tip.x * width))/ 2
                    coordinates_y = (int(index_tip.y * height) + int(middle_tip.y * height))/ 2
                    if coordinates_x > red_x-20 and coordinates_x < red_x + 20 and coordinates_y > red_y-20 and coordinates_y < red_y+20:
                        hand_color = red
                    if hand_color == red:
                        red_circle = cv2.circle(frame, (red_x, red_y), 7, red, circle_thickness)
                    if coordinates_x > green_x-20 and coordinates_x < green_x + 20 and coordinates_y > green_y-20 and coordinates_y < green_y+20:
                        hand_color = green
                        if hand_color == green:
                            green_circle = cv2.circle(frame, (green_x, green_y), 7, green, circle_thickness)
                    if coordinates_x > blue_x-20 and coordinates_x < blue_x + 20 and coordinates_y > blue_y-20 and coordinates_y < blue_y+20:
                        hand_color = blue
                        if hand_color == blue:
                            blue_circle = cv2.circle(frame, (blue_x, blue_y), 7, blue, circle_thickness)
                    if coordinates_x > white_x-20 and coordinates_x < white_x+20 and coordinates_y > white_y-20 and coordinates_y < white_y+20:
                        hand_color = white
                        if hand_color == white:
                            white_circle = cv2.circle(frame, (white_x, white_y), 7, white, circle_thickness)
                            circle = cv2.circle(frame, (white_x, white_y), 23, black, 1)
                   
                    if coordinates_x > save_button_x-0 and coordinates_x < save_button_x+200 and coordinates_y > save_button_y-0 and coordinates_y < save_button_y+40:
                        myDrawing = cv2.bitwise_or(canvas, ngm_image)
                        cv2.imwrite("myDrawing.jpg", myDrawing)
                        saved = True
                        image_path = r"C:\Users\geoge\OneDrive\Έγγραφα\mediapipe-opencv-python\programs\myDrawing.jpg"
                    if coordinates_x > scale_1_x-20 and coordinates_x < scale_1_x+20 and coordinates_y > scale_1_y-20 and coordinates_y > scale_1_y+20:
                        radius = 5
                        if radius == 5:
                            scale_1 = cv2.circle(frame, (scale_1_x, scale_1_y), 7, black, circle_thickness)
                    if coordinates_x > scale_2_x-20 and coordinates_x < scale_2_x+20 and coordinates_y > scale_2_y-20 and coordinates_y > scale_2_y+20:
                        radius = 10
                        if radius == 10:
                            scale_2 = cv2.circle(frame, (scale_2_x, scale_2_y), 7, black, circle_thickness)
                    if coordinates_x > scale_3_x-30 and coordinates_x < scale_3_x+30 and coordinates_y > scale_3_y-30 and coordinates_y > scale_3_y+30:
                        radius = 15
                        if radius == 15:
                            scale_3 = cv2.circle(frame, (scale_3_x, scale_3_y), 7, black, circle_thickness)
                    if coordinates_x > clear_button_x-0 and coordinates_x < clear_button_x+250 and coordinates_y > clear_button_y-0 and coordinates_y > clear_button_y+40:
                        canvas = np.zeros((600, 800, 3), np.uint8)
        

        resized_frame = cv2.resize(frame, (width, height)) # we resizing the frame to our canvas dimensions
        resized_frame = cv2.bitwise_or(resized_frame, canvas) 
  
        cv2.imshow('Hand Tracking', resized_frame) # 'Hand Tracking' frame name. Command is showing the image
        
        if cv2.waitKey(1) & 0xFF == ord('q'): # how to exit
            break
cap.release()
cv2.destroyAllWindows()