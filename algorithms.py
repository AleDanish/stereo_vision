#!/usr/bin/env python

#     Author: Alessandro Zanni
#     URL: https://github.com/AleDanish

import numpy as np
import parameters as params
import utils
import cv2

class WindowAlgorithms(object):

    def __init__(self, imgL, imgR, filter_size):
        self.imgL = imgL
        self.imgR = imgR
        self.rows = len(imgL)
        self.columns = len(imgL[0])
        self.filter_size = filter_size
        print('calculating cost-cube...')
        self.cost_map = self.calculate_cost_map()
        print('calculating local costs using a ' + str(self.filter_size) + 'x' + str(self.filter_size) + ' patch...')
        self.fw_3D_matrix = self.get_fixed_window_matrix()
        self.fw_2D_matrix = np.zeros((self.rows, self.columns)) 

    def calculate_cost_map(self):
        self.cost_map = np.zeros((params.NUM_DISP, self.rows, self.columns))
        for d in range(params.NUM_DISP):
            for x in range(self.rows):
                for y in range(self.columns):
                    self.cost_map[d, x, y] = abs(int(self.imgL[x, y]) - int(self.imgR[x, y - d]))
        return self.cost_map

    def get_fixed_window_matrix(self):
        self.fw_3D_matrix = np.zeros((params.NUM_DISP, self.rows, self.columns))
        for d in range(params.NUM_DISP):
            self.fw_3D_matrix[d] = cv2.boxFilter(self.cost_map[d], -1, (self.filter_size, self.filter_size))
        return self.fw_3D_matrix

    def fixed_window(self):
        if self.fw_3D_matrix is None:
            print('re-calculating cost-cube and local costs using a ' + str(self.filter_size) + 'x' + str(self.filter_size) + ' patch...')
            self.get_fixed_window_matrix(self.calculate_cost_map())
        print('executing fixed window algorithm...')
        self.fw_2D_matrix = np.zeros((self.rows, self.columns))
        for x in range(self.rows):
            for y in range(self.columns):
                min_value = self.fw_3D_matrix[0, x, y]
                disp = 0
                for d in range(params.NUM_DISP):
                    if min_value > self.fw_3D_matrix[d, x, y]:
                        min_value = self.fw_3D_matrix[d, x, y]
                        disp = d
                self.fw_2D_matrix[x][y] = disp
        return self.fw_2D_matrix

    def variable_window(self):
        if self.fw_3D_matrix is None:
            print('re-calculating cost-cube and local costs using a ' + str(self.filter_size) + 'x' + str(self.filter_size) + ' patch...')
            self.get_fixed_window_matrix(self.calculate_cost_map())
        print('executing variable window algorithm...')
        vw_3D_matrix = np.zeros((params.NUM_DISP, self.rows, self.columns))
        self.fw_2D_matrix = np.zeros((self.rows, self.columns))
        for d in range(params.NUM_DISP):
            for x in range(self.rows):
                for y in range(self.columns):
                    submatrix = utils.get_submatrix(self.fw_3D_matrix[d], x, y, self.filter_size)
                    vw_3D_matrix[d, x, y] = utils.get_min_value(submatrix)
        for x in range(self.rows):
            for y in range(self.columns):
                min_value = vw_3D_matrix[0, x, y]
                disp = 0
                for d in range(params.NUM_DISP):
                    if min_value > vw_3D_matrix[d, x, y]:
                        min_value = vw_3D_matrix[d, x, y]
                        disp = d
                self.fw_2D_matrix[x][y] = disp
        return self.fw_2D_matrix
