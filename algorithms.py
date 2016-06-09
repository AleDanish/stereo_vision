#!/usr/bin/env python

#     Author: Alessandro Zanni
#     URL: https://github.com/AleDanish

import numpy as np
import parameters as params
import utils
import sys

class WindowAlgorithms(object):

    def __init__(self, imgL, imgR, filter_size):
        self.imgL = imgL
        self.imgR = imgR
        self.rows = len(imgL)
        self.columns = len(imgL[0])
        self.filter_size = filter_size
        #Cost cube aggregation
        print('calculating cost-cube...')
        self.cost_map = self.calculate_cost_map()
        # Patch application
        print('calculating local costs using a patch '+ str(self.filter_size) + 'x' + str(self.filter_size) + '...')
        self.fw_3D_matrix = self.get_fixed_window_matrix()
        self.fw_2D_matrix = np.zeros((self.rows, self.columns)) 

    def calculate_cost_map(self):
        self.cost_map = np.zeros((self.rows, self.columns, params.NUM_DISP))
        for x in range(0, self.rows-1):
            for y in range(0, self.columns-1):
                for d in range(0, params.NUM_DISP):
                    self.cost_map[x,y,d] = abs(int(self.imgL[x,y]) - int(self.imgR[x-d,y]))
        return self.cost_map

    def get_fixed_window_matrix(self):
        self.fw_3D_matrix = np.zeros((self.rows, self.columns, params.NUM_DISP))
        for x in range(self.rows):
            for y in range(self.columns):
                for d in range(params.NUM_DISP):
                    submatrix = utils.get_submatrix(self.cost_map, x, y, d, self.filter_size)
                    self.fw_3D_matrix[x,y,d] = utils.get_sum_value(submatrix)
        return self.fw_3D_matrix

    def fixed_window(self):
        if self.fw_3D_matrix is None:
            print('re-calculating cost-cube and local costs using a patch '+ str(self.filter_size) + 'x' + str(self.filter_size) + '...')
            self.get_fixed_window_matrix(self.calculate_cost_map())
        print('executing fixed window algorithm...')
        self.fw_2D_matrix = np.zeros((self.rows, self.columns))
        for x in range(self.rows):
            for y in range(self.columns):
                min_value = self.fw_3D_matrix[x,y,0]
                disp = 0
                for d in range(params.NUM_DISP):
                    if min_value > self.fw_3D_matrix[x,y,d]:
                        min_value = self.fw_3D_matrix[x,y,d]
                        disp = d
                self.fw_2D_matrix[x][y] = disp
        return self.fw_2D_matrix

    def variable_window(self):
        if self.fw_3D_matrix is None:
            print('re-calculating cost-cube and local costs using a patch '+ str(self.filter_size) + 'x' + str(self.filter_size) + '...')
            self.get_fixed_window_matrix(self.calculate_cost_map())
        print('executing variable window algorithm...')
        self.fw_2D_matrix = np.zeros((self.rows, self.columns))
        for x in range(self.rows):
            for y in range(self.columns):
                local_min = sys.maxsize
                for d in range(params.NUM_DISP):
                    submatrix = utils.get_submatrix(self.fw_3D_matrix, x, y, d, self.filter_size)
                    local_min = min(local_min, utils.get_min_value(submatrix))
                self.fw_2D_matrix[x,y] = local_min
        return self.fw_2D_matrix
