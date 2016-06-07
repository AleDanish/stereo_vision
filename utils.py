#!/usr/bin/env python

#     Author: Alessandro Zanni
#     URL: https://github.com/AleDanish

def matrix_mean(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    sum = 0
    for i in range(rows):
        for j in range(columns):
    	    sum += matrix[i][j]
    return sum/(rows*columns)

def get_submatrix(matrix, x, y, filter_size):
    rows = len(matrix)
    columns = len(matrix[0])
    x1 = max(0, x - filter_size/2)
    x2 = min(rows, x + filter_size/2)
    y1 = max(0, y - filter_size/2)
    y2 = min(columns, y + filter_size/2)
    return matrix[x1:x2, y1:y2]

def get_min_value(matrix):
    value = matrix[0][0]
    for x in range(0, len(matrix)):
        for y in range(1, len(matrix[0])):
            value = min(value.all(), matrix[x,y].all())
    return value
