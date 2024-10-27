
############################################################################
#颜色二值化阈值调试
############################################################################


import math
import threading
import serial
import time
import cv2
import numpy as np
import sys


cap = None
start,end = 0.0,0.0
def nothing(x):
    pass
WindowName = 'result'
cv2.namedWindow(WindowName, cv2.WINDOW_KEEPRATIO)  # 建立空窗口
cv2.resizeWindow(WindowName, 200, 160)  # 调整窗口大小
cv2.createTrackbar('Bl', WindowName, 0, 255, nothing)  # 创建滑动条
cv2.createTrackbar('Gl', WindowName, 47, 255, nothing)  # 创建滑动条
cv2.createTrackbar('Rl', WindowName, 0, 255, nothing)  # 创建滑动条
cv2.createTrackbar('Bh', WindowName, 217, 255, nothing)  # 创建滑动条
cv2.createTrackbar('Gh', WindowName, 197, 255, nothing)  # 创建滑动条
cv2.createTrackbar('Rh', WindowName, 171, 255, nothing)  # 创建滑动条
cv2.createTrackbar('iterations', WindowName, 2, 20, nothing)  # 创建滑动条

def main():
    global cap
    for i in  range(0,100):
        try:
            cap = cv2.VideoCapture(i)
            print("cap on\n") 
            break
        except:
            pass  
    cap.set(cv2.CAP_PROP_FPS, 15)
    
    while True:
            global start,end
            ret, frame = cap.read()
            if ret:

                # 获取滑动条值
                Bl = cv2.getTrackbarPos('Bl', WindowName)  
                Gl = cv2.getTrackbarPos('Gl', WindowName)  
                Rl = cv2.getTrackbarPos('Rl', WindowName)  
                Bh = cv2.getTrackbarPos('Bh', WindowName) 
                Gh = cv2.getTrackbarPos('Gh', WindowName)  
                Rh = cv2.getTrackbarPos('Rh', WindowName)  
                ite = cv2.getTrackbarPos('iterations', WindowName)  

                
                #颜色空间转换
                hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                #开运算
                hsv_image = cv2.erode(hsv_image, np.ones((3,3),np.uint8), iterations=ite)
                hsv_image = cv2.dilate(hsv_image, np.ones((3,3),np.uint8), iterations=ite)
                
                #模糊处理
                hsv_image = cv2.blur(hsv_image,(9,9))

                #二值转换，进行颜色分割---》把色域内的像素点设为白色，其余像素点设为黑色
                lower_color = np.array([Bl, Gl, Rl])
                upper_color = np.array([Bh, Gh, Rh])
                mask = cv2.inRange(hsv_image, lower_color, upper_color)
                # print(cv2.countNonZero(mask))          
                
                #获取色块轮廓（cv2.findContours()函数返回的轮廓列表是按轮廓大小排序的）
                contours,hierarchy= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)                
                if contours :
                    for contour in contours:#筛选出目标色块
                        x, y, w, h = cv2.boundingRect(contour)
                        mu = cv2.moments(contour)
                        area = w*h
                        if area <= 20000:
                            continue
                        if mu['m00'] ==0:
                            continue
                        center_x = int(mu['m10']/mu['m00'])  
                
                        print(str(area) + " _____"  + str(center_x))
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                
                cv2.namedWindow("mask", cv2.WINDOW_KEEPRATIO)
                cv2.namedWindow("frame", cv2.WINDOW_KEEPRATIO)

                cv2.resizeWindow("mask", (300, 200))
                cv2.resizeWindow("frame", (300, 200))

                cv2.imshow("mask", mask)
                cv2.imshow("frame", frame)
                # 按下 'q' 键退出循环
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break



if __name__ == '__main__':
    main()
    cap.release()# 释放摄像头
    cv2.destroyAllWindows()
