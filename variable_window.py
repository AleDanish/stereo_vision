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
    cv2.imshow('disparity',  disparity)
    return disparity

def variable_window(disparity, x, y):
    print("size: ", disparity.size)
    size=3
    for i in range(1, size, disparity.size):
        step = size / 2
        a=[x-step : x+step][y-step : y+step]
        size += 2

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

    disparity(imgL, imgR, filter_size)

    cv2.imshow('left', imgL)
    cv2.imshow('right', imgR)
    cv2.waitKey()
    cv2.destroyAllWindows()
