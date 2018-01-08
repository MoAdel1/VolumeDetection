## [Code imports]
# tensors operations module
import numpy as np
# image processing modules
import cv2
import imutils
# plotting modules
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
# linear regression model modules
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
# numerical integration modules
from scipy.integrate import quad
import scipy.spatial as ss
from math import pi
# system argument module
import argparse


## [software arguments]
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
ap.add_argument("-s", "--splits", required=True,
                help="number of object splits")
ap.add_argument("-p", "--poly_order", required=True,
                help="ML polynomial regression order")
ap.add_argument("-v", "--view_splits", required=True,
                help="visualize splits or not")
ap.add_argument("-c", "--curve_view", required=True,
                help="visualize half curve or not")
ap.add_argument("-l", "--length", required=True,
                help="maximum length of objects")
args = vars(ap.parse_args())
# set values required for system
path = str(args["image"]) # image path
splits = int(args["splits"]) # number of splits per shape 
poly_order = int(args["poly_order"]) # order of the polynomial 
split_flag = int(args["view_splits"]) # see splits or not
half_flag = int(args["curve_view"]) # put half curve or not
height_calib = float(args["length"]) # for calibrating pixel ratio

## [detect objects to measure]
img = cv2.imread(path)
drawing = False # true if mouse is pressed
ix,iy = -1,-1
# mouse callback function
def draw(event,x,y,flags,param):
    global ix,iy,drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img,(x,y),3,(0,0,255),-1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(img,(x,y),3,(0,0,255),-1)
cv2.namedWindow('select objects to measure (press s to submit)')
cv2.setMouseCallback('select objects to measure (press s to submit)',draw)
while(1):
    cv2.imshow('select objects to measure (press s to submit)',img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('s'):
        break
cv2.destroyAllWindows()
value = np.array([0,0,255])
mask_color = cv2.inRange(img, value, value)
img = cv2.bitwise_and(img,img, mask= mask_color)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
mask_objects = np.zeros(img.shape,np.uint8)
cv2.drawContours(mask_objects,cnts,-1,(255,255,255),-1)

## [detect objects to measure]
img = cv2.imread(path)
drawing = False # true if mouse is pressed
ix,iy = -1,-1
pixel_length = 0
# mouse callback function
def draw_line(event,x,y,flags,param):
    global ix,iy,drawing,img,pixel_length

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            # define image again 
            img = cv2.imread(path)
            cv2.line(img,(ix,iy),(x,y),(0,255,0),5)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(img,(ix,iy),(x,y),(0,0,255),5)
        pixel_length = y-iy
cv2.namedWindow('select Ref. to measure (press s to submit)')
cv2.setMouseCallback('select Ref. to measure (press s to submit)',draw_line)
while(1):
    cv2.imshow('select Ref. to measure (press s to submit)',img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('s'):
        break
cv2.destroyAllWindows()
length_per_pixel = height_calib/pixel_length

## [Define used functions]
def x_center(element):
    M = cv2.moments(element)
    cx = int(M['m10']/M['m00'])
    return(cx)

def fit_subplot(objects,x,fit,y):
    objects.scatter(x, y,  color='black')
    objects.plot(x, fit, color='blue', linewidth=2)

def fit3d_subplot(objects,x,regression_model,order):
    # point mapping per section for each point
    def f(x_point,r_m,o):
        x_point = np.array([[x_point]])
        poly_point = PolynomialFeatures(degree=o)
        x_t = poly_point.fit_transform(x_point)
        return(r_m.predict(x_t))          
    f = np.vectorize(f,otypes=[np.float])
    # plot the section
    u = np.linspace(min(x), max(x), 30) # x range and number of points taken
    v = np.linspace(0, 2*np.pi, 30) # orientation range
    U, V = np.meshgrid(u, v)
    X = U   # original x axis
    Y = f(U,regression_model,order)*np.cos(V)  # y axis projection
    Z = f(U,regression_model,order)*np.sin(V)  # z axis projection
    if(split_flag):
        objects.plot_surface(X, Y, Z)
    else:
        objects.plot_surface(X, Y, Z, color='red')

def get_volume(x,regression_model,poly_order):
    # point mapping function for each point
    def value_point(x_point,r_m,o):
        x_point = np.array([[x_point]])
        poly_point = PolynomialFeatures(degree=o)
        x_t = poly_point.fit_transform(x_point)
        function_value = r_m.predict(x_t)**2
        return(function_value)
    # numeric integration of given section
    I = quad(value_point,min(x),max(x),args=(regression_model,poly_order))
    section_vol = I[0]*pi
    return(section_vol)

def cnt_area(object_cnt):
    return(cv2.contourArea(object_cnt))


## [Read image and detect all objects]
# load the image 
image = mask_objects # image name
# convert it to grayscale, and blur it slightly
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
# perform edge detection, then perform a dilation + erosion to close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
# find contours in the edge map
cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
cnts.sort(key=cnt_area) # sort by area from smallest to largest 


## [split shapes,prepare training data and fit polynomial]
shapes = list()

for c in cnts:
    matrix = c.reshape((-1,2))
    points = matrix[matrix[:,0]>=x_center(c)]
    points.view('int32,int32').sort(order=['f1'], axis=0) # sorting to solve fitting issues
    shapes.append(points)

for shape in shapes:
    # volume variable
    volume = list()
    # define required plots
    fig = plt.figure()
    fig.suptitle("Shape reconstruction",fontsize=16)
    if(half_flag):
        draw_fit = fig.add_subplot(1,2,1)
        draw_fit.set_yticklabels([])
        draw_fit.set_xticklabels([])
        draw_fit.set_title("half shape fitting")
        draw_3d = fig.add_subplot(1,2,2,projection='3d')
        draw_3d.set_yticklabels([])
        draw_3d.set_xticklabels([])
        draw_3d.set_zticklabels([])
    else:
        draw_3d = fig.add_subplot(1,1,1,projection='3d')
        draw_3d.set_yticklabels([])
        draw_3d.set_xticklabels([])
        draw_3d.set_zticklabels([])
    # X axis values
    x = shape[:,1].reshape(-1, 1) # reshape as a matrix
    x = x-min(x)
    x = x*length_per_pixel #calibrate
    #print(max(x)-min(x)) #sanity check
    x = np.array_split(x,splits)
    # Y axis values
    y = shape[:,0].reshape(-1, 1) # reshape as a matrix
    y = y-min(y) # shift to axis center
    y = y*length_per_pixel #calibrate
    #print(max(y)-min(y)) #sanity check
    y = np.array_split(y,splits)
    # fit data using multi-section linear regression
    for i in range(len(x)):
        # transform X data into higher order polnomial
        poly = PolynomialFeatures(degree=poly_order)
        x_transformed = poly.fit_transform(x[i])
        # train the model and get fitted points
        regression_model = linear_model.LinearRegression(fit_intercept=False,copy_X=True,normalize=False)
        regression_model.fit(x_transformed,y[i])
        fitted = regression_model.predict(x_transformed)
        # plot scatter and fitted sub-section
        if(half_flag):
            fit_subplot(draw_fit,x[i],fitted,y[i])
        # plot 3D reconstruction of shape
        fit3d_subplot(draw_3d,x[i],regression_model,poly_order)
        # calculate volume of each section 
        volume.append(get_volume(x[i],regression_model,poly_order))
    # get volume of current shape and print it with 3d plot
    volume_value = sum(volume)  # calibrating shape volume 
    volume_string = "%.3f" % volume_value
    draw_3d.set_title("3D reconstruction -- Volume = "+volume_string)
    # show plots
    plt.show()

        



    

    
    




