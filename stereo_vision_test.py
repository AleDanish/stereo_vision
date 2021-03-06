#!/usr/bin/env python

#     Author: Alessandro Zanni
#     URL: https://github.com/AleDanish

import numpy as np
import cv2
import argparse
import parameters as params
from algorithms import WindowAlgorithms

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
    disp = stereo.compute(imgL, imgR).astype(np.float32) / params.NUM_DISP
    disparity = (disp-params.MIN_DISP)/params.NUM_DISP
    cv2.imshow('disparity',  disparity)
    return disparity

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filter_size')
    parser.add_argument('-w', '--window_type')
    args = parser.parse_args()
    args_dict = vars(args)
    filter_size = args_dict.get('filter_size')
    window_type = args_dict.get('window_type')
    if (filter_size is None) or (filter_size not in params.FILTER_SIZES):
        print("filter size not supported -> will be used the default 3x3 patch")
        filter_size = params.DEFAULT_FILTER_SIZE
    else:
        filter_size = int(filter_size)
    if (window_type is None) or (window_type not in params.WINDOW_TYPES):
        print("window type not supported -> will be used the default 'all'")
        window_type = params.DEFAULT_WINDOW_TYPE

    print('loading images...')
    imgL = cv2.pyrDown(cv2.imread('images/Tsukuba_L.png', cv2.IMREAD_GRAYSCALE)) # retrieve the intensity of the pixels by cv2.IMREAD_GRAYSCALE
    imgR = cv2.pyrDown(cv2.imread('images/Tsukuba_R.png', cv2.IMREAD_GRAYSCALE)) # downscale images for faster processing
    if imgL is not None:
        print("Shape: " + str(imgL.shape) + ", Size: " + str(imgL.size) + ", Type: " + str(imgL.dtype))

    if window_type == 'disparity':
        disparity = disparity(imgL, imgR, filter_size)
        cv2.imshow('disparity', disparity)
    else:
        wa = WindowAlgorithms(imgL, imgR, filter_size)
        if (window_type == 'all') or (window_type == 'fixed'): # Fixed Window
            fixed_window = wa.fixed_window()
            cv2.imshow('fixed window', fixed_window / params.NUM_DISP)
        if (window_type == 'all') or (window_type == 'variable'): # Variable Window
            variable_window = wa.variable_window()
            cv2.imshow('variable window', variable_window / params.NUM_DISP)
    cv2.imshow('left', imgL)
    cv2.imshow('right', imgR)
    cv2.waitKey()
    cv2.destroyAllWindows()
    print('done')
