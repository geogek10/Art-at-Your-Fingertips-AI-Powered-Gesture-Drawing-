import cv2
import numpy as np

canvas = np.zeros((600, 800, 3), np.uint8)
image_path = 'myDrawing.jpg'

image = cv2.imread(image_path)
new_canvas = cv2.bitwise_or(image, canvas)

cv2.imshow("Image", new_canvas)

cv2.waitKey(0)
cv2.destroyAllWindows()