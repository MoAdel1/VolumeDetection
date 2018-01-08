import cv2
import numpy as np
import math

drawing = False # true if mouse is pressed
ix,iy = -1,-1

# mouse callback function
def draw_line(event,x,y,flags,param):
    global ix,iy,drawing,img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            # define image again 
            img = np.zeros((512,512,3), np.uint8)
            cv2.line(img,(ix,iy),(x,y),(0,255,0),5)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(img,(ix,iy),(x,y),(0,0,255),5)
        #print(math.sqrt((ix-x)**2+(iy-y)**2))
        print((y-iy))
        


img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_line)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
