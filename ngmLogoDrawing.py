import cv2

path = 'ngm.jpg'
img = cv2.imread(path)

cv2.imshow("Image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()