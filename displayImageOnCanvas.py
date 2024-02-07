import cv2
import numpy as np

canvas = np.zeros((600, 800, 3), np.uint8)

image_path = 'ngm.jpg'

image = cv2.imread(image_path)

img = cv2.bitwise_or(image, canvas)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()