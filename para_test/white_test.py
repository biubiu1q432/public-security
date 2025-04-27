
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
cv2.createTrackbar('iterations', WindowName, 0, 255, nothing)  # 创建滑动条

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

                ite = cv2.getTrackbarPos('iterations', WindowName)  

                #二值化
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                dst = cv2.GaussianBlur(gray,(5,5),0)
                ret,thresh = cv2.threshold(dst,ite,255,cv2.THRESH_BINARY_INV)
                
                #获取色块轮廓（cv2.findContours()函数返回的轮廓列表是按轮廓大小排序的）
                contours,hierarchy= cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)                
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

                cv2.imshow("mask", thresh)
                cv2.imshow("frame", frame)
                # 按下 'q' 键退出循环
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break



if __name__ == '__main__':
    main()
    cap.release()# 释放摄像头
    cv2.destroyAllWindows()