'''
用于测试一次侦察任务
'''

import time
import cv2
import numpy as np
import pygame

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
        self.ROI_range=30
        
        self.boardcast = Boardcast()

        '''可调参数'''
        #Canny阈值
        self.threshold1 = 32
        self.threshold2 = 38
        #面积过滤
        self.areaMin = 500
        #形状与角点个数
        self.Recentage = 4
        self.Triangle = 3
        self.Cricle = 8
        self.Star = 10
        
        #颜色阈值
        self.red_low = np.array([36, 78, 94])
        self.red_up = np.array([185, 172, 206])
        self.red_iter = 2
        
        self.blue_low = np.array([68, 77, 172])
        self.blue_up = np.array([188, 242, 249])
        self.blue_iter = 5
        
        self.green_low = np.array([0, 0, 0])
        self.green_up = np.array([255, 255, 255])
        self.green_iter = 2
        
        self.yellow_low = np.array([0, 0, 0])
        self.yellow_up = np.array([255, 255, 255])
        self.yellow_iter = 2
        
        self.white_low = np.array([0, 0, 0])
        self.white_up = np.array([255, 255, 255])
        self.white_iter = 2
        
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

        # green_mask = cv2.inRange(hsv, self.green_low, self.green_up)
        # green_mask = cv2.erode(green_mask, None, iterations=self.green_iter)
        # green_mask = cv2.dilate(green_mask, None, iterations=self.green_iter)
        # green_count = cv2.countNonZero(green_mask)

        # yellow_mask = cv2.inRange(hsv, self.yellow_low, self.yellow_up)
        # yellow_mask = cv2.erode(yellow_mask, None, iterations=self.yellow_iter)
        # yellow_mask = cv2.dilate(yellow_mask, None, iterations=self.yellow_iter)
        # yellow_count = cv2.countNonZero(yellow_mask)

        # white_mask = cv2.inRange(hsv, self.white_low, self.white_up)
        # white_mask = cv2.erode(white_mask, None, iterations=self.white_iter)
        # white_mask = cv2.dilate(white_mask, None, iterations=self.white_iter)
        # white_count = cv2.countNonZero(white_mask)

        # black_mask = cv2.inRange(hsv, self.black_low, self.black_up)
        # black_mask = cv2.erode(black_mask, None, iterations=self.black_iter)
        # black_mask = cv2.dilate(black_mask, None, iterations=self.black_iter)
        # black_count = cv2.countNonZero(black_mask)
        
        #比大小
        color = max(red_count,blue_count)#,green_count,yellow_count,white_count,black_count)
        if color == red_count:
            color = "Red"
        elif color == blue_count:
            color = "Blue"
        # elif color == green_count:
        #     color = "Green"
        # elif color == yellow_count:
        #     color = "Yellow"
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


#TEST
if __name__ == '__main__':
    detect=Detect()
    print("cw")
    if detect.Detect():
        print("ok")
    else:
        print("ccw")
        print("ccw")
        detect.Detect()
        print("ok")

    
    
