## [imports section]
import cv2
import numpy as np

## [basic operation]
img = cv2.imread('test1.jpg')
cv2.imshow('original',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

## [add two images together]
img1 = cv2.imread('test1.jpg') # rted half apples
img1 = cv2.resize(img1,(300,300)) # resize pic
img2 = cv2.imread('test2.jpg')
img2 = cv2.resize(img2,(300,300)) # pepsi can 
com_img = cv2.addWeighted(img1,1,img2,0.2,0)
cv2.imshow('added image',com_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

## [extract a color from an image]
img = cv2.imread('test2.jpg') # pepsi can
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# blue color bounds
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])
# detect the blue color
mask = cv2.inRange(hsv,lower_blue,upper_blue)
# and mask with original frame
res = cv2.bitwise_and(img, img, mask=mask)
# display results
cv2.imshow('original', img)
cv2.imshow('mask', mask)
cv2.imshow('res', res)
cv2.waitKey(0)
cv2.destroyAllWindows()
# very bad for token object because of light conditions

## [geometric transformation of images]


