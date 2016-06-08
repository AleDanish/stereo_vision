#!/usr/bin/env python

#     Author: Alessandro Zanni
#     URL: https://github.com/AleDanish

import parameters as params
import numpy as np

def matrix_mean(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    sum = 0
    for i in range(rows):
        for j in range(columns):
    	    sum += matrix[i][j]
    return sum/(rows*columns)

def get_submatrix(matrix, x, y, d, filter_size):
    rows = len(matrix)
    columns = len(matrix[0])
    x1 = max(0, x - filter_size/2)
    x2 = min(rows, x + filter_size/2)
    y1 = max(0, y - filter_size/2)
    y2 = min(columns, y + filter_size/2)
    return [row[y1:(y2+1), d] for row in matrix[x1:(x2+1)]]

def get_min_value(matrix):
    value = matrix[0][0]
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            value = min(value, matrix[x][y])
    return value
