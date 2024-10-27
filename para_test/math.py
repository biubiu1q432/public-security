import numpy as np
import cv2

'''
比较上下线长度判断上下梯形。    
sorted_points = points[np.argsort(points[:, 1])]ndexError: index 1 is out of bounds for axis 1 with size 1
'''
approx = np.array([[[226, 169]], [[396, 178]], [[169, 400]], [[444, 408]]])

def group_by_y(points, y_threshold=10):
    points = np.squeeze(points, axis=1)
    sorted_points = points[np.argsort(points[:, 1])]
    
    group1 = [sorted_points[0],sorted_points[1]]
    group2 = [sorted_points[2],sorted_points[3]]

    print(group1,group2)

group = group_by_y(approx)



