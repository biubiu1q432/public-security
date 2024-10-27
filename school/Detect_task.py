from collections import namedtuple
import cv2 # type: ignore
import numpy as np # type: ignore
from torch import tensor
from ultralytics import YOLO  
from cv2 import getTickCount, getTickFrequency
import time
import math
import threading
import serial
import time
import cv2
import sys
import pygame
from pygame.locals import *


##全局变量
#色块统计
blue_cnt=0
red_cnt=0
#转向标志位
flag_CCW=0
flag_CW=0
#摄像头
cap=None
#目标形状
class OBJECT:
    def __init__(self):
        self.shape=""
        self.color=""
Object= OBJECT()    
detected_objects = []
detected_colors =  []


##墙上颜色阈值(粗略，，互相分辨)
red_lower = np.array([146, 79, 67])
red_upper = np.array([255, 255, 255])
red_ite=0

blue_lower = np.array([95, 94, 0])
blue_upper = np.array([144, 255, 255])
blue_ite=0


##定义过滤参数
#找色块
red_target_area=11000
blue_target_area=11000
y_range=310
#二值区域
picture_area=5000
threshold1 = 47
threshold2 = 42


##OPENCV
#可调： 颜色阈值（find_color）  +    面积过滤(area)     +   二值化
#可升级:中心动态调整转向角度(y与center_y)
def pattern_recognition(img): 
 ################################################二值化之全图阈值过滤#####################################   
    
    # #转灰度
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # #高斯滤波
    # blur = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # #二值化
    # _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # #调试
    # cv2.namedWindow("thresh", cv2.WINDOW_KEEPRATIO)
    # cv2.imshow("thresh", thresh)
    # cv2.waitKey(1)

 ###############################################二值化之边界#########################################

    #高斯滤波--》imgBlur
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    
    #转灰度--》imgGray
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    
    #中值滤波-->imgBlur2
    imgBlur2 = cv2.medianBlur(imgGray,7)
    
    #Canny整图边界二值化--》imgCanny
    imgCanny = cv2.Canny(imgBlur2,threshold1,threshold2)
    
    #膨胀二值边界--》imgDil
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, 1)
    
    # #调试
    # cv2.namedWindow("imgBlur2",cv2.WINDOW_KEEPRATIO)
    # cv2.imshow("imgBlur2",imgBlur2)
    # cv2.waitKey(1)

    # cv2.namedWindow("imgCanny",cv2.WINDOW_KEEPRATIO)    
    # cv2.imshow("imgCanny",imgCanny)
    # cv2.waitKey(1)       
    
    # cv2.namedWindow("imgDil",cv2.WINDOW_KEEPRATIO)
    # cv2.imshow("imgDil",imgDil)
    # cv2.waitKey(1)

 ######################################顶点####################################################

    #拿顶点
    contours, hierarchy = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours_poly = [None] * len(contours)
    
    #近似
    for i in range(len(contours)):
        contours_poly[i] = cv2.approxPolyDP(contours[i], 0.02 * cv2.arcLength(contours[i], True), True)
    
    #结果
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
                
        #过滤
        if area > picture_area :
            x, y, w, h = cv2.boundingRect(contours[i])
            #形状
            ratio = w / h
            color = (0, 0, 0)
            if len(contours_poly[i]) == 3:
                Object.shape = "Triangle"
                color = (0, 0, 255)
            
            elif len(contours_poly[i]) == 4:
                
                if 0.99 < ratio < 1.01:
                    Object.shape = "Square"
                    color = (0, 255, 255)
                else:
                    Object.shape = "Rectangle"
                    color = (0, 255, 0)
            
            elif len(contours_poly[i]) == 8:
                Object.shape = "Circle"
                color = (255, 255, 0)
            
            elif len(contours_poly[i]) == 10:
                Object.shape = "Star"
                color = (255, 0, 255)
                        
            
            #调试
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, Object.shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(img, str(area), (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(img, str(len(contours_poly[i])), (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                       
            #颜色
            x1=x
            x2=x+w
            y1=y
            y2=y+h
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)                
            find_color(img,cx,cy)
            
    return img

#统计筛选
def find_color(img,ROI_x,ROI_y):
    global Object 
    
    if ROI_x-30 in range(1,480) and ROI_y-30 in range(1,640) and ROI_x+30 in range(1,480) and ROI_y+30 in range(1,640):#截图越界保险

        #预处理
        ROI_img = img[ROI_y:ROI_y+30, ROI_x:ROI_x+30]
        hsv = cv2.cvtColor(ROI_img,cv2.COLOR_BGR2HSV)        
        
        # cv2.imshow("ROI_img",ROI_img)
        # cv2.waitKey(1)

        ##根据颜色阈值进行分割+腐蚀
        red_mask = cv2.inRange(hsv, red_lower, red_upper)
        red_mask = cv2.erode(red_mask, np.ones((3,3),np.uint8),red_ite )
        red_mask = cv2.dilate(red_mask, np.ones((3,3),np.uint8),red_ite )
                      
        blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
        blue_mask = cv2.erode(blue_mask, np.ones((3,3),np.uint8),blue_ite )
        blue_mask = cv2.dilate(blue_mask, np.ones((3,3),np.uint8),blue_ite )            
        

        ##对每个颜色区域的像素进行统计            
        red_count = cv2.countNonZero(red_mask)
        blue_count = cv2.countNonZero(blue_mask)

        ##(调试用）打印每个颜色的像素数量
        print("Red:", red_count)
        print("Blue:", blue_count)
            
        final_color=max(red_count,blue_count)
    
        if 0 == final_color:
            print("未检测到颜色")
            Object.color="none"
        
        elif blue_count ==final_color:
            print("其颜色为蓝色")
            Object.color="blue"

        elif red_count ==final_color:
            print("其颜色为红色")
            Object.color="red"
        

    else:
        return

#统计 flag=1->图片识别统计 flag=2 ->颜色识别统计
def analyse(flag):
    global Object
    global detected_objects
    global detected_colors

    if 1==flag:
        for i in range(71):
            ret,img = Cap_read()
            if ret:
                if i>20:
                    #一次分析 
                    result = pattern_recognition(img)
                    
                    #一次统计
                    detected_objects.append(Object.shape)
                    detected_colors.append(Object.color)
                    
                    # #调试
                    # cv2.namedWindow("test", cv2.WINDOW_KEEPRATIO)
                    # cv2.imshow("test", result)
                    # cv2.waitKey(1)

        #结果筛选
        Best_broadcast_shape = max(set(detected_objects), key=(detected_objects.count))
        Best_broadcast_color = max(set(detected_colors), key=(detected_colors.count))

        #语言播报
        
        print("语言播报已发送")
        print(str(Best_broadcast_shape)+"-------"+str(Best_broadcast_color))
        
        ##形状
        if Best_broadcast_shape=="Circle":
            circle()
        elif Best_broadcast_shape=="Rectangle":
            rectangle()
        elif Best_broadcast_shape=="Triangle":
            triangle()
        elif Best_broadcast_shape=="Star":
            star()
        else:    
            none()
        ##颜色
        if Best_broadcast_color=="red":
            red()
        elif Best_broadcast_color=="yellow":
            yellow()
        elif Best_broadcast_color=="blue":
            blue()
        elif Best_broadcast_color=="green":
            green()
        else:    
            none()

    elif 2==flag:
        for i in range(41):
            ret,img = Cap_read()
            if ret:
                if i>30:
                    #一次分析 
                    result = pattern_recognition(img) 
                    #一次统计
                    detected_colors.append(Object.color)   
        #结果筛选
        Turn_color_try = max(set(detected_colors), key=(detected_colors.count))
        
        #调试
        # cv2.namedWindow("test", cv2.WINDOW_KEEPRATIO)
        # cv2.imshow("test", result)
        # cv2.waitKey(1)

        #重置
        detected_colors=[]
        Object=OBJECT()
        
        return Turn_color_try


##阻塞找色块
#可调： 颜色阈值（find_color） + 面积过滤(area)  
#可升级:中心定位急停(x与center_x)
def find_red():
    red_Bl, red_Gl, red_Rl ,red_Bh, red_Gh, red_Rh,red_ite=118,94,111,215,224,190,0
    global red_cnt
    global cap
    
    ret,frame = Cap_read()  
    if ret == False:
        return

    #色域设置
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([red_Bl, red_Gl, red_Rl])
    upper_color = np.array([red_Bh, red_Gh, red_Rh])
    
    #开运算
    hsv_image = cv2.erode(hsv_image, np.ones((3,3),np.uint8), iterations=red_ite)
    hsv_image = cv2.dilate(hsv_image, np.ones((3,3),np.uint8), iterations=red_ite)
    
    #模糊处理
    hsv_image = cv2.blur(hsv_image,(9,9))

    #二值转换，进行颜色分割---》把色域内的像素点设为白色，其余像素点设为黑色
    mask = cv2.inRange(hsv_image, lower_color, upper_color)
    
    
    #获取色块轮廓（cv2.findContours()函数返回的轮廓列表是按轮廓大小排序的）
    contours,hierarchy= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    biggest_area = 0
    
    #迭代器
    if contours :
        for contour in contours:#筛选出目标色块
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)            
            if area > biggest_area:
                biggest_area = area
            #调试
            print("red:"+str(biggest_area))
            #结果分析
            if biggest_area > red_target_area and int((y+y+w)/2) >= y_range:  #可调试
                red_cnt+=1
   
def find_blue():
    blue_Bl, blue_Gl, blue_Rl ,blue_Bh, blue_Gh, blue_Rh,blue_ite=87,108,173,128,220,247,0
    global blue_cnt
    global cap
    
    ret,frame = Cap_read()
    if ret == False:
        return

    #色域设置
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([blue_Bl, blue_Gl, blue_Rl])
    upper_color = np.array([blue_Bh, blue_Gh, blue_Rh])
    
    #开运算
    hsv_image = cv2.erode(hsv_image, np.ones((3,3),np.uint8), iterations=blue_ite)
    hsv_image = cv2.dilate(hsv_image, np.ones((3,3),np.uint8), iterations=blue_ite)
    
    #模糊处理
    hsv_image = cv2.blur(hsv_image,(9,9))

    #二值转换，进行颜色分割---》把色域内的像素点设为白色，其余像素点设为黑色
    mask = cv2.inRange(hsv_image, lower_color, upper_color)
    
    
    #获取色块轮廓（cv2.findContours()函数返回的轮廓列表是按轮廓大小排序的）
    contours,hierarchy= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    biggest_area = 0
    
    #迭代器
    if contours :
        for contour in contours:#筛选出目标色块
            #调试
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            if area > biggest_area:
                biggest_area = area
                #调试
                print("blue"+str(biggest_area))
            #结果分析
            if biggest_area > blue_target_area :#待调试
                blue_cnt+=1
    
    # #调试
    # cv2.namedWindow("hsv", cv2.WINDOW_NORMAL)
    # cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
    # cv2.imshow("mask", mask)
    # cv2.imshow("hsv", hsv_image)
 
#return: "red"  "blue" 
def Turn_Scan():
    global red_cnt,blue_cnt
    while True:   
        find_blue()
        find_red()
        if blue_cnt>3:
            print("##########################################")
            print("检测到蓝色")
            print("##########################################")
            return "blue"
        
        elif red_cnt>3:
            print("##########################################")
            print("检测到红色")
            print("##########################################")
            return "red"      




##运动命令
def STOP():
    arr = "@|5|" + str(1) + "|" + str(0) + "|" + str(0) + "#"
    car_port.write(arr.encode("ascii"))
    Task_judge()

def FORWARD(distance):
    arr = "@|6|" + str(distance) + "|" + str(0) + "|" + str(0) + "#"
    car_port.write(arr.encode("ascii"))
    print(arr)

def GO_AHEAD():
    arr = "@|1|" + str(0.1) + "|" + str(50) + "|" + str(15) + "#"
    car_port.write(arr.encode("ascii"))
    print(arr)
    Task_judge()

def CCW():
    arr = "@|2|" + str(1) + "|" + str(270) + "|" + str(0) + "#"
    car_port.write(arr.encode("ascii"))
    print(arr)
    Task_judge()

def CW():
    arr = "@|2|" + str(2) + "|" + str(90) + "|" + str(0) + "#"
    car_port.write(arr.encode("ascii"))
    print(arr)
    Task_judge()

def Cap_up():
    arr = "@|4|" + str(1) + "|" + str(30) + "|" + str(0) + "#"
    car_port.write(arr.encode("ascii"))
    print(arr)
    Task_judge()

def Cap_down():
    arr = "@|4|" + str(1) + "|" + str(90) + "|" + str(0) + "#"
    car_port.write(arr.encode("ascii"))
    print(arr)   
    Task_judge()

def Task_judge():
    global car_port
    while True:
        try:
            if car_port.in_waiting > 0:
                message = car_port.readline()                  
                if message:
                    #获取message前四个字符
                    message = message.decode(encoding="UTF-8")    
                    data = message[:4]
                    if data == "DONE":
                        print("OK")
                        return

        except:
            pass


#摄像头
def Cap_read():
    global cap
    ret,img = cap.read()
    if ret:
        return True,img
    
    else:
        for i in range(0,13):
            cap=cv2.VideoCapture(i)
            ret,img = cap.read()
            if ret:
                print(i)
                return True,img
    
    return False,img
                 
def Open_Cap():
    global cap
    for i in range(0,13):
        cap=cv2.VideoCapture(i)
        ret=cap.read()[0]
        if ret:
            print(i)
            return 


#播报
def red():
    pygame.mixer.music.load("/home/aipc/Desktop/My_voice/red.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
def yellow():
    pygame.mixer.music.load("/home/aipc/Desktop/My_voice/yellow.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
def blue():
    pygame.mixer.music.load("/home/aipc/Desktop/My_voice/blue.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
def green():
    pygame.mixer.music.load("/home/aipc/Desktop/My_voice/green.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
def rectangle():
    pygame.mixer.music.load("/home/aipc/Desktop/My_voice/rec.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
def triangle():
    pygame.mixer.music.load("/home/aipc/Desktop/My_voice/tri.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
def circle():
    pygame.mixer.music.load("/home/aipc/Desktop/My_voice/cri.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
def star():
    pygame.mixer.music.load("/home/aipc/Desktop/My_voice/star.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
def none():
    pygame.mixer.music.load("/home/aipc/Desktop/My_voice/none.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def OLED():
    #读取一张照片
    img = cv2.imread("/home/aipc/Desktop/image.png")
    #显示照片3s然后关闭窗口
    cv2.imshow("image", img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

def Detect():   
    global flag_CCW,flag_CW,red_cnt,blue_cnt,detected_objects,detected_colors,Object
# while True:
    #急停        
    Turn_color=Turn_Scan()

    #吞掉所有指令
    for i in range(20):
        if car_port.in_waiting > 0:
            message = car_port.readline()

    STOP()

    #前进+试探转向+抬头
    FORWARD(0.13)  
    #吞掉所有指令
    time.sleep(4)
    for i in range(20):
        if car_port.in_waiting > 0:
            message = car_port.readline()    
    
    CCW()
    Cap_up()    
    #验证猜想
    Turn_color_try=analyse(2)
    
    ##相同颜色
    if Turn_color_try == Turn_color :
        print("试对了")
        flag_CCW=1
    
    ##不同颜色
    else:
        print("试错了")
        CW()
        CW()
        flag_CW=1 
    
    #图像检测    
    print("##########################################")
    analyse(1)
 
    #归位    
    if flag_CW == 1:
        CCW()
            
    elif flag_CCW == 1:
        CW()
    
    Cap_down()
    
    flag_CCW=0
    flag_CW=0
    red_cnt=0
    blue_cnt=0
    detected_objects=[]
    detected_colors=[]
    Object=OBJECT()
    #关闭摄像头
    cap.release()




#初始化
pygame.mixer.init()
car_port = serial.Serial(port="/dev/ttyAMA2",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)
print("uart on")
Open_Cap()

#尽头+转弯
GO_AHEAD()
CW()
OLED()

#任务
FORWARD(0.5)
Detect()
GO_AHEAD()
OLED()

#尽头+转弯
CW()
GO_AHEAD()
OLED()

#回头
CCW()
CCW()

#前进指定距离
FORWARD(0.83)
time.sleep(25)
for i in range(20):
    if car_port.in_waiting > 0:
        message = car_port.readline()
CCW()

#任务
FORWARD(0.5)
Detect()
GO_AHEAD()
CCW()
GO_AHEAD()

