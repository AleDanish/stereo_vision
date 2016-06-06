#!/usr/bin/env python

#     Author: Alessandro Zanni
#     URL: https://github.com/AleDanish

import numpy as np
import cv2
import argparse
from matplotlib import pyplot as plt

NUM_DISP=32

def disparity(imgL, imgR, filter_size):
    window_size = 3
    min_disp = 0#16
    num_disp = NUM_DISP#112-min_disp
    block_size = 5
    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=block_size,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2,
        disp12MaxDiff = 1,
        uniquenessRatio = 10,
        speckleWindowSize = 100,
        speckleRange = 32)
    print('computing disparity...')
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0
    disparity = (disp-min_disp)/num_disp
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
    cost = np.zeros((rows, columns, NUM_DISP))
    for x in range(0, rows-1):
        for y in range(0, columns-1):
            for d in range(0, NUM_DISP-1):
                cost[x,y,d] = abs(imgL[x,y] - imgR[x-d,y])
    return cost

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
    cm = cost_map(imgL, imgR)
    print("cost map: ", cm)

    #Fixed Window

    #Variable Window


    cv2.imshow('left', imgL)
    cv2.imshow('right', imgR)
    cv2.waitKey()
    cv2.destroyAllWindows()
