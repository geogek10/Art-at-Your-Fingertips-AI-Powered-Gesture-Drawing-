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

def redBrush(scale_factor=1.0):
    global redBrushImage
    global redBrushHeight
    global redBrushWidth
    global redBrushTarget_x
    global redBrushTarget_y

    redBrushImagePath = "redWhite.png"

    # Load the image
    redBrushImage = cv2.imread(redBrushImagePath)

    # Resize the image
    redBrushImage = cv2.resize(redBrushImage, None, fx=scale_factor, fy=scale_factor)

    # Continue with the rest of your code
    redBrushHeight, redBrushWidth, _ = redBrushImage.shape
    redBrushTarget_x = 50
    redBrushTarget_y = 0

    # Assuming 'frame' is defined somewhere in your code
    canvas_roi = frame[redBrushTarget_y:redBrushTarget_y+redBrushHeight, redBrushTarget_x:redBrushTarget_x+redBrushWidth]
    frame[redBrushTarget_y:redBrushTarget_y+redBrushHeight, redBrushTarget_x:redBrushTarget_x+redBrushWidth] = redBrushImage

def greenBrush(scale_factor=1.0):
    global greenBrushImage
    global greenBrushHeight
    global greenBrushWidth
    global greenBrushTarget_x
    global greenBrushTarget_y

    # green brush
    greenBrushImagePath = "greenWhite.png"

    # Load the image
    greenBrushImage = cv2.imread(greenBrushImagePath)

    # Resize the image
    greenBrushImage = cv2.resize(greenBrushImage, None, fx=scale_factor, fy=scale_factor)

    # Continue with the rest of your code
    greenBrushHeight, greenBrushWidth, _ = greenBrushImage.shape
    greenBrushTarget_x = 200
    greenBrushTarget_y = 0

    # Assuming 'frame' is defined somewhere in your code
    canvas_roi = frame[greenBrushTarget_y:greenBrushTarget_y+ greenBrushHeight, greenBrushTarget_x:greenBrushTarget_x+greenBrushWidth]
    frame[greenBrushTarget_y:greenBrushTarget_y+greenBrushHeight, greenBrushTarget_x:greenBrushTarget_x+greenBrushWidth] = greenBrushImage

def blueBrush(scale_factor=1.0):
    global blueBrushImage
    global blueBrushHeight
    global blueBrushWidth
    global blueBrushTarget_x
    global blueBrushTarget_y

    # blue brush
    blueBrushImagePath = "blueWhite.png"

    # Load the image
    blueBrushImage = cv2.imread(blueBrushImagePath)

    # Resize the image
    blueBrushImage = cv2.resize(blueBrushImage, None, fx=scale_factor, fy=scale_factor)

    # Continue with the rest of your code
    blueBrushHeight, blueBrushWidth, _ = blueBrushImage.shape
    blueBrushTarget_x = 350
    blueBrushTarget_y = 0

    # Assuming 'frame' is defined somewhere in your code
    canvas_roi = frame[blueBrushTarget_y:blueBrushTarget_y+ blueBrushHeight, blueBrushTarget_x:blueBrushTarget_x+blueBrushWidth]
    frame[blueBrushTarget_y:blueBrushTarget_y+blueBrushHeight, blueBrushTarget_x:blueBrushTarget_x+blueBrushWidth] = blueBrushImage

def whiteBrush(scale_factor=1.0):
    global whiteBrushImage
    global whiteBrushHeight
    global whiteBrushWidth
    global whiteBrushTarget_x
    global whiteBrushTarget_y

    # white brush
    whiteBrushImagePath = "whiteWhite.png"

    # Load the image
    whiteBrushImage = cv2.imread(whiteBrushImagePath)

    # Resize the image
    whiteBrushImage = cv2.resize(whiteBrushImage, None, fx=scale_factor, fy=scale_factor)

    # Continue with the rest of your code
    whiteBrushHeight, whiteBrushWidth, _ = whiteBrushImage.shape
    whiteBrushTarget_x = 500
    whiteBrushTarget_y = 0

    # Assuming 'frame' is defined somewhere in your code
    canvas_roi = frame[whiteBrushTarget_y:whiteBrushTarget_y+ whiteBrushHeight, whiteBrushTarget_x:whiteBrushTarget_x+whiteBrushWidth]
    frame[whiteBrushTarget_y:whiteBrushTarget_y+whiteBrushHeight, whiteBrushTarget_x:whiteBrushTarget_x+whiteBrushWidth] = whiteBrushImage


# function for creating the UI(User Interface)
def interface():
    # this loop draws a white area at the top of the screen
    for i in range(0, 100, 1):
            #cv2.line(image, start_point, end_point, color, thickness) 
            cv2.line(frame, (0, 65-i), (1500, 65-i), white, 1)

    # this loop creates a white are in the bottom of the screen
    for j in range(0, 100, 1):
        cv2.line(frame, (0, 600+j), (1500, 600+j), white, 1)

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

# variables for sending emails
from_email = "geogek10@gmail.com" # sender email
to_email = "geogekas10@gmail.com" # recipient email
smtp_server = "smtp.gmail.com" # connection server
smtp_port = 587 # port for connection server
subject = "Your Drawing!" # subject of email
pswd = "lsab farp kzew unup" # unique password 

msg = MIMEMultipart()
msg["From"] = from_email
msg["To"] = to_email
msg["Subject"] = subject

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

erase_button_x = 650
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
clear_button_y = 35

ngm_path = 'ngm.jpg'
ngm_image = cv2.imread(ngm_path)

width = 1800
height = 900
cap = cv2.VideoCapture(0) # getting webcam feed. Prosoxi sto (0)
ret = cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)
ret = cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
new_coordinates = (0,0)
past_coordinates = (0,0)
image_path = "0"

# Create a blank canvas with the same dimensions as the image
canvas = np.zeros((height, width, 3), np.uint8)

with mp_hands.Hands(False,1,min_detection_confidence=0.1, min_tracking_confidence=0.1) as hands:  # hands module
    while cap.isOpened(): # reading through each frame
        ret, frame = cap.read() # frame represents the image
        
        if frame is None:
            continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) 

        results = hands.process(frame)

        interface()
        redBrush()
        greenBrush()
        blueBrush()
        whiteBrush()

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

                index_tip_x = round(index_tip.x * width)
                index_tip_y = round(index_tip.y * height)
                thumb_tip_x = round(thumb_tip.x * width)
                thumb_tip_y = round(thumb_tip.y * height)

                it_coordinates_x = abs((index_tip_x - thumb_tip_x) / 2)
                it_coordinates_y = abs((index_tip_y - thumb_tip_y) / 2)

                # Calculate the distance between index finger tip and thumb tip
                distance_it = math.sqrt((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2 + (index_tip.z - thumb_tip.z)**2)
                distance_im = math.sqrt((index_tip.x - middle_tip.x)**2 + (index_tip.y - middle_tip.y)**2 + (index_tip.z - middle_tip.z)**2)

                if it_coordinates_x < 15 and it_coordinates_y < 15:
                    new_coordinates = (round((index_tip_x + thumb_tip_x) / 2), round((index_tip_y + thumb_tip_y) / 2))

                    if past_coordinates == (0,0):
                        past_coordinates = new_coordinates

                    cv2.line(canvas, past_coordinates, new_coordinates, hand_color, radius)

                    past_coordinates = new_coordinates
                else: 
                    past_coordinates = (0,0)

                if distance_im < 0.1:
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            # Extract landmarks for the index finger and middle finger (landmark ID 4 and 12)
                            index_finger_lm = hand_landmarks.landmark[4]
                            middle_finger_lm = hand_landmarks.landmark[12]

                            # Calculate the midpoint
                            midpoint_x = int((index_finger_lm.x + middle_finger_lm.x) * frame.shape[1] / 2)
                            midpoint_y = int((index_finger_lm.y + middle_finger_lm.y) * frame.shape[0] / 2)

                            if midpoint_x >= 30 and midpoint_x <= 100 and midpoint_y >= 5 and midpoint_y <= 70:
                                hand_color = red
                                if hand_color == red:
                                    redBrush(scale_factor=1.3)

                            if midpoint_x >= 340 and midpoint_x <= 390 and midpoint_y >= 7 and midpoint_y <= 70:
                                hand_color = blue
                                if hand_color == blue:
                                    blueBrush(scale_factor=1.3)

                            if midpoint_x >= 180 and midpoint_x <= 265 and midpoint_y >= 5 and midpoint_y <= 70:
                                hand_color = green
                                if hand_color == green:
                                    greenBrush(scale_factor=1.3)

                            if midpoint_x >= 490 and midpoint_x <= 540 and midpoint_y >= 5 and midpoint_y <= 70:
                                hand_color = white
                                if hand_color == white:
                                    whiteBrush(scale_factor=1.3)

                            if midpoint_x >= 640 and midpoint_x <= 780 and midpoint_y >= 5 and midpoint_y <= 70:
                                hand_color = black
                                if hand_color == black:
                                    cv2.rectangle(frame, (635, 7), (785, 38), black, 1)

                            if midpoint_x >= 890 and midpoint_x <= 1000 and midpoint_y >= 5 and midpoint_y <= 70:
                                canvas = np.zeros((height, width, 3), np.uint8)

                            if midpoint_x >= 170 and midpoint_x <= 230 and midpoint_y >= 590 and midpoint_y <= 640:
                                radius = 5
                                if radius == 5:
                                    scale_1 = cv2.circle(frame, (scale_1_x, scale_1_y), 6, black, circle_thickness)

                            if midpoint_x >= 325 and midpoint_x <= 370 and midpoint_y >= 590 and midpoint_y <= 650:
                                radius = 10
                                if radius == 10:
                                    scale_2 = cv2.circle(frame, (scale_2_x, scale_2_y), 7, black, circle_thickness)

                            if midpoint_x >= 470 and midpoint_x <= 535 and midpoint_y >= 590 and midpoint_y <= 640:
                                radius = 15
                                if radius == 15:
                                    scale_3 = cv2.circle(frame, (500, 630), 8, black, circle_thickness)

                            if midpoint_x >= 670 and midpoint_x <= 790 and midpoint_y >= 605 and midpoint_y <= 660:
                                ngm_image_resized = cv2.resize(ngm_image, (canvas.shape[1], canvas.shape[0]))
                                myDrawing = cv2.bitwise_or(canvas, ngm_image_resized)
                                cv2.imwrite("myDrawing.jpg", myDrawing)
                                saved = True
                                sent = True
                                image_path = "myDrawing.jpg"

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

                print("Email sent successfully")
            sent = False

        if cv2.waitKey(10) & 0xFF == ord('r'):
            cv2.imshow('Drawing', canvas)

        if saved == True:
            save_button = cv2.putText(frame, "SAVE", (save_button_x, save_button_y), font, 1.5, green)
        
        resized_frame = cv2.resize(frame, (width, height))
        canvas = cv2.resize(canvas, (resized_frame.shape[1], resized_frame.shape[0]))
        resized_frame = cv2.bitwise_or(resized_frame, canvas)
  
        cv2.imshow('Hand Tracking', resized_frame) # 'Hand Tracking' frame name. Command is showing the image
        
        if cv2.waitKey(1) & 0xFF == ord('q'): # how to exit
            break
cap.release()
cv2.destroyAllWindows()