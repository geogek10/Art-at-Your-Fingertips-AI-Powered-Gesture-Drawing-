import cv2
import numpy as np

canvas = np.zeros((600, 800, 3), np.uint8)

image_path = 'redBrush.png'
image = cv2.imread(image_path)

image_resized = cv2.resize(image, (50, 60))

height, width, _ = image_resized.shape

target_x = 30
target_y = 20

canvas_roi = canvas[target_y:target_y+height, target_x:target_x+width]

canvas[target_y:target_y+height, target_x:target_x+width] = image_resized

cv2.imshow("Image", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()