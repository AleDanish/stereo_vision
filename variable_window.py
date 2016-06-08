#!/usr/bin/env python

#     Author: Alessandro Zanni
#     URL: https://github.com/AleDanish

import numpy as np
import cv2
import argparse
import parameters as params
import utils

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

def cost_map(imgL, imgR):
    rows = len(imgL)
    columns = len(imgL[0])
    cost = np.zeros((rows, columns, params.NUM_DISP))
    for x in range(0, rows-1):
        for y in range(0, columns-1):
            for d in range(0, params.NUM_DISP):
                cost[x,y,d] = abs(int(imgL[x,y]) - int(imgR[x-d,y]))
    return cost

def get_fixed_window_matrix(cost_map, filter_size):
    rows = len(cost_map)
    columns = len(cost_map[0])
    matrix = np.zeros((rows, columns, params.NUM_DISP))
    for x in range(rows):
        for y in range(columns):
            for d in range(params.NUM_DISP):
                submatrix = utils.get_submatrix(cost_map, x, y, d, filter_size)
                matrix[x,y,d] = utils.get_min_value(submatrix)
#                print("submatrix: ", submatrix)
#                print("matrix[x,y,d]: ", matrix[x,y,d])
    print("marix row0: ", matrix[0,y,d])
    return matrix

def fixed_window(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    matrix_2D = np.zeros(shape=(rows,columns))
    for x in range(rows):
        for y in range(columns):
            min_value = matrix[x,y,0]
            for d in range(params.NUM_DISP):
                min_value = min(min_value, matrix[x,y,d])
            matrix_2D[x][y] = min_value
    return matrix_2D

def variable_window(cost_map, filter_size):
    matrix = []
    rows = len(cost_map)
    columns = len(cost_map[0])
   # for x in range(rows):
   #     for y in range(columns):
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--filter_size')
    args = parser.parse_args()
    args_dict = vars(args)
    filter_size = int(args_dict.get('filter_size'))
    if filter_size is None:
        filter_size = params.DEFAULT_FILTER_SIZE

    print('loading images...')
    # retrieve the intensity of the pixels by cv2.IMREAD_GRAYSCALE
    imgL = cv2.pyrDown(cv2.imread('images/img_L.png', cv2.IMREAD_GRAYSCALE))  # downscale images for faster processing
    imgR = cv2.pyrDown(cv2.imread('images/img_R.png', cv2.IMREAD_GRAYSCALE))
    print imgL[0,0]
    if imgL is not None:
        print("Shape: " + str(imgL.shape))
        print("Size: " + str(imgL.size))
        print("Type: " + str(imgL.dtype))

#    disparity = disparity(imgL, imgR, filter_size)
 
    #Cost cube aggregation
    cost_map = cost_map(imgL, imgR)
    fixed_window_matrix = get_fixed_window_matrix(cost_map, filter_size)

    # Fixed Window
    m = fixed_window(fixed_window_matrix)
    cv2.imshow('fixed window', m)

    # Variable Window
    #variable_window = variable_window(fixed_window_matrix, filter_size)
    #print("variable window", variable_window)

    cv2.imshow('left', imgL)
    cv2.imshow('right', imgR)
    cv2.waitKey()
    cv2.destroyAllWindows()
