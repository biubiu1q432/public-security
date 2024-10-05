'''
用于测试一次侦察任务
'''

import time
import cv2
import numpy as np
import pygame
import serial



#全局变量
MOVE_DICT = None #移动字典
POINT_ID = None # 点号
MY_SERIAL = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)
COLOR_FLAG = None 


class Boardcast:
    def __init__(self):
        pygame.mixer.init()
    
    def Recentage(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/dad/public security/sound/color/blue.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)        
    
    def Triangle(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/dad/public security/sound/shape/tri.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)        
    
    def Cricle(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/dad/public security/sound/shape/cri.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)        
    
    def Star(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/dad/public security/sound/shape/star.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)        
    
    def white(self):
        pass
    
    def black(self):
        pass
    
    def red(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/dad/public security/sound/color/red.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)    
    
    def green(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/dad/public security/code/sound/color/green.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    
    def blue(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/dad/public security/sound/color/blue.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    
    def yellow(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/dad/public security/sound/color/yellow.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

#一次侦察流程，注意color_flag归位
class Detect:
    
    def __init__(self):
        #摄像头初始化
        self.cap = cv2.VideoCapture(0)
        #统计
        self.Shapes=[]
        self.Colors=[]
        self.Best_Shape=None
        self.Best_Color=None
        self.ROI_range=45
        
        self.boardcast = Boardcast()

        '''可调参数'''
        #Canny阈值
        self.threshold1 = 50
        self.threshold2 = 88
        #面积过滤
        self.areaMin = 5000
        #形状与角点个数
        self.Recentage = 4
        self.Triangle = 3
        self.Cricle = 8
        self.Star = 10
        
        #颜色阈值
        self.red_low = np.array([149, 136, 94])
        self.red_up = np.array([181, 208, 223])
        self.red_iter = 1
        
        self.blue_low = np.array([93, 54, 54])
        self.blue_up = np.array([152, 255, 156])
        self.blue_iter = 1
        
        self.green_low = np.array([26, 58, 198])
        self.green_up = np.array([85, 129, 255])
        self.green_iter = 1
        
        self.yellow_low = np.array([23, 129, 168])
        self.yellow_up = np.array([71, 212, 255])
        self.yellow_iter = 1
        
        self.white_low = np.array([0, 0, 0])
        self.white_up = np.array([255, 255, 255])
        self.white_iter = 1
        
        self.black_low = np.array([0, 0, 0])
        self.black_up = np.array([255, 255, 255])
        self.black_iter = 2

    #一次侦察流程
    def Detect(self):
        
        for i in range(0,21):
            #拍照
            ret,img = self.cap.read()
            if ret:
                #轮廓
                Shape,center_x,center_y=self.Shape_Detect(img)
                if Shape == None or center_y == None or center_x == None:#说明没有检测到轮廓，直接进入下一轮，避免报错
                    continue
                self.Shapes.append(Shape)                
                #颜色
                Color=self.Color_Detect(img,center_x,center_y)
                self.Colors.append(Color)
        
        #统计出出现次数最多的形状和颜色
        try:
            self.Best_Shape = max(set(self.Shapes), key=(self.Shapes.count))
            self.Best_Color = max(set(self.Colors), key=(self.Colors.count))
        except:
            print("没有检测到轮廓")
            return False
        
        #调试
        print("Best Shape:",self.Best_Shape)
        print("Best Color:",self.Best_Color)

        #语音播报
        if self.Best_Shape == "Recentage":
            self.boardcast.Recentage()
        elif self.Best_Shape == "Triangle":
            self.boardcast.Triangle()
        elif self.Best_Shape == "Cricle":
            self.boardcast.Circle()

        time.sleep(0.2)

        if self.Best_Color == "Red":
            self.boardcast.red()
        elif self.Best_Color == "Blue":
            self.boardcast.blue()
        elif self.Best_Color == "Green":
            self.boardcast.green()
        elif self.Best_Color == "Yellow":
            self.boardcast.yellow()
        elif self.Best_Color == "White":
            self.boardcast.white()
        elif self.Best_Color == "Black":
            self.boardcast.black()
            
        return True

    #一次形状提取，返回形状和轮廓信息
    def Shape_Detect(self,img):
        
        #如果没检测到轮廓就全返回None
        center_x=None
        center_y=None
        shape=None

        #高斯滤波--》imgBlur
        imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
        
        #转灰度--》imgGray
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
        
        #中值滤波-->imgBlur2
        imgBlur2 = cv2.medianBlur(imgGray,7)
        
        #Canny整图边界二值化--》imgCanny
        imgCanny = cv2.Canny(imgBlur2,self.threshold1,self.threshold2)
        
        #膨胀二值边界--》imgDil
        kernel = np.ones((5, 5))
        imgDil = cv2.dilate(imgCanny, kernel, 1)
    
        #遍历轮廓
        contours, hierarchy = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area > self.areaMin:
                
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                #轮廓提取
                x , y , w, h = cv2.boundingRect(approx)
                center_x = int((x + w + x) / 2)
                center_y = int((y + h + y) / 2)
                #形状识别
                if len(approx) == self.Recentage:
                    shape="Recentage"
                elif len(approx) == self.Triangle:
                    shape="Triangle"
                elif len(approx) == self.Cricle:
                    shape="Circle"
                elif len(approx) > self.Star:
                    shape="Star"
                else:
                    shape=None
                
        #         #调试
        #         img_debug = img.copy()
        #         cv2.drawContours(img_debug, cnt, -1, (255, 0, 255), 7)
        #         cv2.rectangle(img_debug, (x , y ), (x + w , y + h ), (0, 255, 0), 5)
        #         cv2.putText(img_debug, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
        #                     (0, 255, 0), 2)
        #         cv2.putText(img_debug, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
        #                     (0, 255, 0), 2)
        #         print("Points: " + str(len(approx)))         
        #         print("Area: "+ str(int(area)))        
                
            
        # #调试
        # cv2.imshow("Result", img_debug)
        # cv2.waitKey(1)
        # img_debug = []
        
        return shape,center_x,center_y

    #一次颜色提取，返回颜色
    def Color_Detect(self,img,center_x,center_y):
        
        #中心截图
        ROI_img = img[center_y:center_y+self.ROI_range, center_x:center_x+self.ROI_range]
        hsv = cv2.cvtColor(ROI_img,cv2.COLOR_BGR2HSV)
        # cv2.imshow("ROI", ROI_img)
        # cv2.waitKey(1)
        
        #分别二值化
        red_mask = cv2.inRange(hsv, self.red_low, self.red_up)
        red_mask = cv2.erode(red_mask, None, iterations=self.red_iter)
        red_mask = cv2.dilate(red_mask, None, iterations=self.red_iter)
        red_count = cv2.countNonZero(red_mask)

        blue_mask = cv2.inRange(hsv, self.blue_low, self.blue_up)
        blue_mask = cv2.erode(blue_mask, None, iterations=self.blue_iter)
        blue_mask = cv2.dilate(blue_mask, None, iterations=self.blue_iter)
        blue_count = cv2.countNonZero(blue_mask)

        green_mask = cv2.inRange(hsv, self.green_low, self.green_up)
        green_mask = cv2.erode(green_mask, None, iterations=self.green_iter)
        green_mask = cv2.dilate(green_mask, None, iterations=self.green_iter)
        green_count = cv2.countNonZero(green_mask)

        yellow_mask = cv2.inRange(hsv, self.yellow_low, self.yellow_up)
        yellow_mask = cv2.erode(yellow_mask, None, iterations=self.yellow_iter)
        yellow_mask = cv2.dilate(yellow_mask, None, iterations=self.yellow_iter)
        yellow_count = cv2.countNonZero(yellow_mask)

        # white_mask = cv2.inRange(hsv, self.white_low, self.white_up)
        # white_mask = cv2.erode(white_mask, None, iterations=self.white_iter)
        # white_mask = cv2.dilate(white_mask, None, iterations=self.white_iter)
        # white_count = cv2.countNonZero(white_mask)

        # black_mask = cv2.inRange(hsv, self.black_low, self.black_up)
        # black_mask = cv2.erode(black_mask, None, iterations=self.black_iter)
        # black_mask = cv2.dilate(black_mask, None, iterations=self.black_iter)
        # black_count = cv2.countNonZero(black_mask)
        
        #比大小
        color = max(red_count,blue_count,green_count,yellow_count)#,white_count,black_count)
        if color == red_count:
            color = "Red"
        elif color == blue_count:
            color = "Blue"
        elif color == green_count:
            color = "Green"
        elif color == yellow_count:
            color = "Yellow"
        # elif color == white_count:
        #     color = "White"
        # elif color == black_count:
        #     color = "Black"
        
        return color
    
    #形状提取，返回形状和轮廓信息(测试)
    def Shape_Detect_test(self):
        while True:
            ret,img=self.cap.read()
            if ret:
                shape,x,y=self.Shape_Detect(img)
                color = self.Color_Detect(img,x,y)
                print(shape)
                print(color)

#串口（下位机）
class Read_Serial:
    #构造函数
    def __init__(self):
        
        self.H_floor = 33
        self.S_floor = 79
        self.L_floor= 32
        
        self.H_color1= 9
        self.S_color1= 89
        self.L_color1= 35
        
        self.H_color2= 28
        self.S_color2= 113
        self.L_color2= 32
        
        self.allow_err= 32

    #消息认证
    def messages_config(self,messages):
        if messages[0] != '@' and messages[0] != '#' and  messages[0] != '!':
            return True
        else:
            return False

    #读HSL
    def read_HSL(self,messages):
        #找到第一个'|'
        index = messages.find('|')
        #找到第二个'|'
        index2 = messages.find('|',index+1)
        #找到第三个'|'
        index3 = messages.find('|',index2+1)
        #把index和index+1之间的字符串赋值给H
        h = int(messages[1:index])
        #把index2和index2+1之间的字符串赋值给S
        s = int(messages[index+1:index2])
        #把index2+3和index2+5之间的字符串赋值给L
        l = int(messages[index2+1:index3])
        print(h,s,l)
        
        #计算hsv和HSV的差距
        judge_err = [abs(self.H_floor-h),abs(self.S_floor-s),abs(self.L_floor-l)]
        judge_err = sum(judge_err)
        #print(judge_err)

    #HSL参数自界定
    def HSL_test(self,num):
        
        if num == 2:
            for i in range(30):
                messages = MY_SERIAL.readline().decode('utf-8')
                if read.messages_config(messages):
                    continue 
                index = messages.find('|')
                index2 = messages.find('|',index+1)
                index3 = messages.find('|',index2+1)
                h = int(messages[1:index])
                s = int(messages[index+1:index2])
                l = int(messages[index2+1:index3])   
                print(h,s,l)

                h_list= []
                s_list = []
                l_list = []
                h_list.append(h)
                s_list.append(s)
                l_list.append(l)
        
            print("颜色2： "+str(int(sum(h_list)/len(h_list))),str(int(sum(s_list)/len(s_list))),str(int(sum(l_list)/len(l_list))))
        
        elif num == 1:
            
            for i in range(30):
                messages = MY_SERIAL.readline().decode('utf-8')
                if read.messages_config(messages):
                    continue 
                index = messages.find('|')
                index2 = messages.find('|',index+1)
                index3 = messages.find('|',index2+1)
                h = int(messages[1:index])
                s = int(messages[index+1:index2])
                l = int(messages[index2+1:index3])   
                print(h,s,l)

                h_list= []
                s_list = []
                l_list = []
                h_list.append(h)
                s_list.append(s)
                l_list.append(l)            
        
            print("颜色1： "+str(int(sum(h_list)/len(h_list))),str(int(sum(s_list)/len(s_list))),str(int(sum(l_list)/len(l_list)) ))
                 
        elif num == 4:
            #计算允许误差
            err1 = int(abs(self.H_color1 - self.H_floor) + abs(self.S_color1 - self.S_floor) + abs(self.L_color1 - self.L_floor))#颜色1
            err2 = int(abs(self.H_color2 - self.H_floor) + abs(self.S_color2 - self.S_floor) + abs(self.L_color2 - self.L_floor))#颜色2
            #小的一项赋值
            print(str(min(err1,err2)))
            
        elif num == 3: 
        
            arr = "@|1|" + str(25) + "|" + str(60) + "|" + str(75) + "#"
            MY_SERIAL.write(arr.encode('utf-8'))
            
            while True:

                messages = MY_SERIAL.readline().decode('utf-8')
                if read.messages_config(messages):
                    continue
                if messages[0] == '@':
                    break

                index = messages.find('|')
                index2 = messages.find('|',index+1)
                index3 = messages.find('|',index2+1)
                h = int(messages[1:index])
                s = int(messages[index+1:index2])
                l = int(messages[index2+1:index3])   
                print(h,s,l)

                h_list= []
                s_list = []
                l_list = []
                h_list.append(h)
                s_list.append(s)
                l_list.append(l)
            
            #赋值
            print("地板颜色："+str(int(sum(h_list)/len(h_list))),str(int(sum(s_list)/len(s_list))),str(int(sum(l_list)/len(l_list))))
         
    #ID
    def read_ID(self,messages):
        pass

#运动
class MOVE:
    def __init__(self):
        global MOVE_DICT
        
        # self.detect = Detect()
        self.read = Read_Serial()
        
        #跑图动作组
        MOVE_DICT = [
                    self.GO, 
                    self.CW, 
                    self.GO,
                    self.CCW,
                    self.Distance_100,
                    self.CCW,
                    self.GO,
                    self.CW,
                    self.Distance_100,
                    self.CW,
                    self.GO,
                    self.CCW,
                    self.Distance_100,
                    self.CCW,
                    self.GO,
                    self.CW,
                    self.GO,
                    self.CW,
                    self.GO,
                    self.CW,
                    self.GO,
                    self.CW,
                    self.Distance_100,
                    self.CW,
                    self.GO,
                    self.CCW,
                    self.GO,
                    self.CCW,
                    self.Distance_100,
                    self.Distance_100,
                    self.CW,
                    self.CW,
                    self.GO,
                    self.CW,
                    self.Distance_100,
                    self.CW,
                    self.GO,
                    self.CCW,
                    self.Distance_50,
                    self.CW,
                    self.Distance_20,
        ]
    
    def GO(self):
        global MY_SERIAL,POINT_ID,COLOR_FLAG
        #发
        arr = "@|1|" + str(25) + "|" + str(60) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("GO")
        #收
        while True:
            data = MY_SERIAL.readline().decode('utf-8')
            if self.read.messages_config(data):
                continue
            
            #DONE
            if data[0] == '@':
                break
            #hsl
            if data[0] == '#':
                #侦擦任务
                if self.read.read_HSL(data):
                    print("侦擦任务")
                    break
            #ID
                    
    def Distance_100(self):
        global MY_SERIAL,POINT_ID,COLOR_FLAG
        #发
        arr = "@|6|" + str(30) + "|" + str(100) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("Distance")
        #收
        while True:
            data = MY_SERIAL.readline().decode('utf-8')
            if self.read.messages_config(data):
                continue
    
            #DONE
            if data[0] == '@':
                break
            #hsl
            if data[0] == '#':
                #侦擦任务
                if self.read.read_HSL(data):
                    print("侦擦任务")
            #ID
    def Distance_50(self):
        global MY_SERIAL,POINT_ID,COLOR_FLAG
        #发
        arr = "@|6|" + str(30) + "|" + str(50) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("Distance")
        #收
        while True:
            data = MY_SERIAL.readline().decode('utf-8')
            if self.read.messages_config(data):
                continue
    
            #DONE
            if data[0] == '@':
                break
            #hsl
            if data[0] == '#':
                #侦擦任务
                if self.read.read_HSL(data):
                    print("侦擦任务")
            #ID
    def Distance_20(self):
        global MY_SERIAL,POINT_ID,COLOR_FLAG
        #发
        arr = "@|6|" + str(30) + "|" + str(20) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("Distance")
        #收
        while True:
            data = MY_SERIAL.readline().decode('utf-8')
            if self.read.messages_config(data):
                continue
    
            #DONE
            if data[0] == '@':
                break

    #顺时针
    def CW(self):
        global MY_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(90) + "|" + str(0) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("CW")
        #收
        while True:
            messages = MY_SERIAL.readline().decode('utf-8')
            if self.read.messages_config(messages):
                continue
            #DONE
            if messages[0] == '@':
                break
            #ID
    #逆时针
    def CCW(self):
        global MY_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(-90) + "|" + str(0) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("CCW")
        #收
        while True:
            messages = MY_SERIAL.readline().decode('utf-8')
            if self.read.messages_config(messages):
                continue
            #DONE
            if messages[0] == '@':
                break
            #ID  

    def STOP(self):
        arr = "@|5|" + str(1) + "|" + str(0) + "|" + str(0) + "#"
        MY_SERIAL.write(arr.encode("ascii"))

#TEST
if __name__ == '__main__':
    detect=Detect()
    move = MOVE()
    if detect.Detect():
        pass
    else:
        move.CW()
        move.CW()
        detect.Detect()
        print("ok")

    
    
