#!/usr/bin/env python

#     Author: Alessandro Zanni
#     URL: https://github.com/AleDanish

import numpy as np
import cv2
import argparse
from matplotlib import pyplot as plt

def disparity(imgL, imgR, filter_size):
    window_size = 3
    min_disp = 16
    num_disp = 112-min_disp
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
    print("disparity: ", disparity)
    cv2.imshow('disparity',  disparity)
    return disparity

def matrix_mean(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    sum = 0
    for i in range(rows):
        for j in range(columns):
    	    sum += matrix[i][j]
            print("sum_c:", sum)
        print("sum_r", sum)
    print("sum", sum)
    print("m:", sum/(rows*columns))
    return sum/(rows*columns)

def variable_window(disparity, x, y): #mappa di diparità e coordinate del punto
    print("disparity size: ", disparity.size)
    size=2
    mean=0
    for i in range(1, size, disparity.size):
        size += 1
        x1 = x - step
        x2 = x + step
        y1 = y - step
        y2 = y + step
        if (x1 < 0) or (x2 < 0) or (y1<0) or (y2<0): #near a border
            return mean
#        a=[x1:x2][y1:y2]
        a = [[1,2,],[3,4]]
        mean = matrix_mean(a)
        print("mean: ", mean)
        size += 1

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
    imgL = cv2.pyrDown(cv2.imread('images/img_L.png'))  # downscale images for faster processing
    imgR = cv2.pyrDown(cv2.imread('images/img_R.png'))

    if imgL is not None:
        print("Shape: " + str(imgL.shape))
        print("Size: " + str(imgL.size))
        print("Type: " + str(imgL.dtype))
#        cv2.imshow('box filt', cv2.boxFilter(imgL, cv2.CV_8U, (filter_size, filter_size)))
        #boxFilter(imgL, int(filter_size))

    disparity = disparity(imgL, imgR, filter_size)

#    variable_window(disparity)

    cv2.imshow('left', imgL)
    cv2.imshow('right', imgR)
    cv2.waitKey()
    cv2.destroyAllWindows()
