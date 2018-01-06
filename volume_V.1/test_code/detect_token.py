# import the necessary packages
import numpy as np
import imutils
import cv2
import matplotlib.pyplot as plt

# define detection function
def sort_area(element):
    return(cv2.contourArea(element))

def detect_min(contours):
    Xcenter = list()
    for c in contours:
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])
        Xcenter.append(cx)
    return min(Xcenter)
 
# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread("test1.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
 
# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
 
# find contours in the edge map
cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]


# classify contours
ref_object = detect_min(cnts)
for c in cnts:
    M = cv2.moments(c)
    cx = int(M['m10']/M['m00'])
    if cx == ref_object:
        cv2.drawContours(image, [c], 0, (255, 0, 0), 2) # blue for ref. object
    else:
        cv2.drawContours(image, [c], 0, (0, 255, 0), 2) # green for normal objects
            
        
# draw the output image
plt.axis("off")
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()

