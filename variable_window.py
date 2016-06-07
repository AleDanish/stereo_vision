#!/usr/bin/env python

#     Author: Alessandro Zanni
#     URL: https://github.com/AleDanish

import numpy as np
import cv2
import argparse
import parameters as params

def disparity(imgL, imgR, filter_size):
    window_size = filter_size
    stereo = cv2.StereoSGBM_create(
        minDisparity=params.MIN_DISP,
        numDisparities=params.NUM_DISP,
        blockSize=params.BLOCK_SIZE,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2,
        disp12MaxDiff = params.DISP12MAXDIFF,
        uniquenessRatio = params.UNIQUENESSRATIO,
        speckleWindowSize = params.SPECKLEWINDOWSIZE,
        speckleRange = params.SPECKLERANGE)
    print('computing disparity...')
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0
    disparity = (disp-params.MIN_DISP)/params.NUM_DISP
    cv2.imshow('disparity',  disparity)
    return disparity

def matrix_mean(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    sum = 0
    for i in range(rows):
        for j in range(columns):
    	    sum += matrix[i][j]
    return sum/(rows*columns)

#def variable_window(disparity, x, y):
    #mappa di diparita' e coordinate del punto

def cost_map(imgL, imgR):
    rows = len(imgL)
    columns = len(imgL[0])
    cost = np.zeros((rows, columns, params.NUM_DISP))
    for x in range(0, rows-1):
        for y in range(0, columns-1):
            for d in range(0, params.NUM_DISP-1):
                cost[x,y,d] = abs(int(imgL[x,y]) - int(imgR[x-d,y]))
    return cost

def getSubMatrix(matrix, x, y, filter_size):
    rows = len(matrix)
    columns = len(matrix[0])
    x1 = max(0, x - filter_size/2)
    x2 = min(rows, x + filter_size/2)
    y1 = max(0, y - filter_size/2)
    y2 = min(columns, y + filter_size/2)
    return matrix[x1:x2, y1:y2]

def getMinValue(matrix):
    value = matrix[0][0]
    for x in range(0, len(matrix)):
        for y in range(1, len(matrix[0])):
            value = min(value.all(), matrix[x,y].all())
    return value

def fixed_window(cost_map, filter_size):
    matrix = []
    rows = len(cost_map)
    columns = len(cost_map[0])
    for x in range(rows):
        for y in range(columns):
            sub_matrix = getSubMatrix(cost_map, x, y, filter_size)
            cost_map[x][y] = getMinValue(sub_matrix)
    return cost_map

def variable_window(cost_map_ filter_size):
    matrix = []
    rows = len(cost_map)
    columns = len(cost_map[0])
    for x in range(rows):
        for y in range(columns):
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--filter_size')
    args = parser.parse_args()
    args_dict = vars(args)
    filter_size = int(args_dict.get('filter_size'))
    if filter_size is None:
        filter_size = 3

    print('loading images...')
    # retrieve the intensity of the pixels by cv2.IMREAD_GRAYSCALE
    imgL = cv2.pyrDown(cv2.imread('images/img_L.png', cv2.IMREAD_GRAYSCALE))  # downscale images for faster processing
    imgR = cv2.pyrDown(cv2.imread('images/img_R.png', cv2.IMREAD_GRAYSCALE))
    print imgL[0,0]
    if imgL is not None:
        print("Shape: " + str(imgL.shape))
        print("Size: " + str(imgL.size))
        print("Type: " + str(imgL.dtype))
#        cv2.imshow('box filt', cv2.boxFilter(imgL, cv2.CV_8U, (filter_size, filter_size)))

    disparity = disparity(imgL, imgR, filter_size)
    #variable_window(disparity, 0, 0)

    #Cost cube aggregation
    cost_map = cost_map(imgL, imgR)
    print("cost map: ", cost_map)

    #Fixed Window
#    fixed_window = fixed_window(cost_map, filter_size)
#    getMatrix(cost_map, 10, 10, filter_size)
    c = getMinValue(cost_map)
    print ("min val: ", c)
    #Variable Window
    #variable_window(fixed_window, filter_size)

    cv2.imshow('left', imgL)
    cv2.imshow('right', imgR)
    cv2.waitKey()
    cv2.destroyAllWindows()
