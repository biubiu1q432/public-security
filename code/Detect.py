'''
用于测试一次侦察任务
'''
import cv2
import numpy as np
import Boardcast
#shape:            color                                    
#1 实心矩形         1 红色
#2 空心矩形         2 蓝色
#3 实心上梯形
#4 空心上梯形
#5 实心下梯形
#6 空心下梯形
#7 实心正方形
#8 空心正方形

  
class Detect:
    
    def __init__(self):
        #摄像头初始化
        self.cap = cv2.VideoCapture(0,cv2.CAP_V4L2)
        self.cap.set(3, 640)
        self.cap.set(4, 480) 
        #统计
        self.Shapes=[]
        self.Colors=[]
        self.Best_Shape=None
        self.Best_Color=None
        self.brocast=Boardcast.Boardcast()

        '''可调参数'''
        #Canny阈值
        self.threshold1 = 50
        self.threshold2 = 88
        #面积过滤
        self.areaMin = 5000
        #形状
        self.rec = 100
        self.squ = 15
        self.tra = 20
        
        #ROI
        self.roi_x = 5  #左上角
        self.roi_y = 5
        self.roi_w = 5  
        self.roi_h = 5  
        self.ROI_range=45 #空心
        
        #颜色阈值
        self.red_low = np.array([0, 120, 101])
        self.red_up = np.array([232, 209, 217])
        self.red_iter = 1
        
        self.blue_low = np.array([78, 77, 47])
        self.blue_up = np.array([148, 189, 129])
        self.blue_iter = 1
        
        self.white_low = np.array([0, 0, 104])
        self.white_up = np.array([137, 100, 255])
        self.white_iter = 1
        
     #一次侦察流程
    def Detect(self):
        
        for i in range(0,31):
            
            ret, frame = self.cap.read()
            if ret:
                shape1,center_x,center_y,x,y = self.Shape_Detect(frame)
                if shape1 == None or center_x == None or center_y == None or x == None or y == None :
                    continue

                shape2,color=self.Color_Detect(frame,center_x,center_y,x,y)
                
                #              实心1     空心2   红色1    蓝色2
                #矩形   1   
                #上梯形 2
                #下梯形 3
                #正方形 4   
      
                #形状映射           
                if shape1 == 1 :#矩形
                    #实心
                    if shape2 == 1:
                        Shape = 1
                    #空心
                    elif shape2 == 2:
                        Shape = 2
                elif shape1 == 2 :#上梯形
                    #实心
                    if shape2 == 1:
                        Shape = 3
                    #空心
                    elif shape2 == 2:
                        Shape = 4
                elif shape1 == 3 :#下梯形
                    #实心
                    if shape2 == 1:
                        Shape = 5
                    #空心
                    elif shape2 == 2:
                        Shape = 6
                elif shape1 == 4 :#正方形
                    #实心
                    if shape2 == 1:
                        Shape = 7
                    #空心
                    elif shape2 == 2:
                        Shape = 8
                
                #颜色映射
                if color == 1:
                    Color = 1
                elif color == 2:
                    Color = 2

                #统计
                self.Shapes.append(Shape)                
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

        
        #shape:            color                                    
        #1 实心矩形         1 红色
        #2 空心矩形         2 蓝色
        #3 实心上梯形
        #4 空心上梯形
        #5 实心下梯形
        #6 空心下梯形
        #7 实心正方形
        #8 空心正方形
        
        #形状播报
        if self.Best_Shape == 1:
            self.brocast.b1()
        elif self.Best_Shape == 2:
            self.brocast.b2()
        elif self.Best_Shape == 3:
            self.brocast.b3()
        elif self.Best_Shape == 4:
            self.brocast.b4()
        elif self.Best_Shape == 5:
            self.brocast.b5()
        elif self.Best_Shape == 6:
            self.brocast.b6()
        elif self.Best_Shape == 7:
            self.brocast.b7()
        elif self.Best_Shape == 8:
            self.brocast.b8()
        #颜色播报
        if self.Best_Color == 1:
            self.brocast.red()
        elif self.Best_Color == 2:
            self.brocast.blue()
        
        return True

    #扳机式参数：shape,center_x,center_y,left_x,left_y
    def Shape_Detect(self,img):
        
        #扳机式变量    
        shape = None
        center_x =None
        center_y = None
        x = None
        y = None

        #高斯滤波--》imgBlur
        imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
        
        #转灰度--》imgGray
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
        
        #中值滤波-->imgBlur2
        imgBlur2 = cv2.medianBlur(imgGray,7)
        
        #Canny整图边界二值化--》imgCanny
        imgCanny = cv2.Canny(imgBlur2,50,88)

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
                
                #过滤
                if len(approx) != 4:
                    # img = cv2.resize(img, (300,200)) 
                    # cv2.imshow("Result", img)
                    # cv2.waitKey(1)
                    return None,None,None,None,None
                
                x, y ,w,h = cv2.boundingRect(approx)
                mu = cv2.moments(cnt)
                #中心点
                center_x = int(mu['m10']/mu['m00'])  
                center_y = int(mu['m01']/mu['m00'])

                #形状判断
                approx = np.array(approx)
                approx = np.squeeze(approx, axis=1)
                sorted_points = approx[np.argsort(approx[:, 1],)] #按y值从小到大排序

                #------->x
                #|   A   B
                #|   C   D
                #v
                
                #AB
                if sorted_points[0][0] <= sorted_points[1][0]:
                    A = sorted_points[0]
                    B = sorted_points[1]
                elif sorted_points[0][0] > sorted_points[1][0]:
                    A = sorted_points[1]
                    B = sorted_points[0]
                #CD
                if sorted_points[2][0] <= sorted_points[3][0]:
                    C = sorted_points[2]
                    D = sorted_points[3]
                elif sorted_points[2][0] >= sorted_points[3][0]:
                    C = sorted_points[3]
                    D = sorted_points[2]
   
                AB = int(np.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2))#AB距离计算               
                CD = int(np.sqrt((C[0]-D[0])**2 + (C[1]-D[1])**2)) #CD距离计算
                AC = int(np.sqrt((A[0]-C[0])**2 + (A[1]-C[1])**2))#AC距离计算
                
                #左上角坐标
                x = A[0]+self.roi_x
                y = A[1]+self.roi_y
                
                # print(AB,CD,AC)

                #              实心1     空心2
                #矩形   1   
                #上梯形 2
                #下梯形 3
                #正方形 4
                if AB - AC > self.rec:
                    print("矩形")
                    shape = 1
                elif CD-AB > self.tra:
                    print("上梯形")
                    shape = 2
                elif AB-CD > self.tra:
                    print("下梯形")
                    shape = 3
                elif abs(AB-AC) <= self.squ :
                    print("正方形")
                    shape = 4    
                else:
                    # cv2.imshow("Result", img)
                    # cv2.waitKey(1)
                    return None,None,None,None,None
                
                #调试
        #         cv2.drawContours(img, cnt, -1, (255, 0, 255), 7)
        #         cv2.putText(img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
        #                     (0, 255, 0), 2)
        #         cv2.putText(img, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
        #                     (0, 255, 0), 2)
        #         #    print("Points: " + str(len(approx)))         
        #         #    print("Area: "+ str(int(area)))        
                
        # #调试
        # img = cv2.resize(img, (300,200)) 
        # cv2.imshow("Result", img)
        # cv2.waitKey(1)
        
        return shape,center_x,center_y,x,y
      
        #一次颜色提取，返回颜色
    
    #color:1红色 2蓝色
    def Color_Detect(self,img,center_x,center_y,x,y):
        
        shape = None
        color = None
        
        #中心截图
        ROI_img = img[center_y:center_y+self.ROI_range, center_x:center_x+self.ROI_range]
        hsv = cv2.cvtColor(ROI_img,cv2.COLOR_BGR2HSV)
        
        #分别二值化
        red_mask = cv2.inRange(hsv, self.red_low, self.red_up)
        red_mask = cv2.erode(red_mask, None, iterations=self.red_iter)
        red_mask = cv2.dilate(red_mask, None, iterations=self.red_iter)
        red_count = cv2.countNonZero(red_mask)

        blue_mask = cv2.inRange(hsv, self.blue_low, self.blue_up)
        blue_mask = cv2.erode(blue_mask, None, iterations=self.blue_iter)
        blue_mask = cv2.dilate(blue_mask, None, iterations=self.blue_iter)
        blue_count = cv2.countNonZero(blue_mask)

        white_mask = cv2.inRange(hsv, self.white_low, self.white_up)
        white_mask = cv2.erode(white_mask, None, iterations=self.white_iter)
        white_mask = cv2.dilate(white_mask, None, iterations=self.white_iter)
        white_count = cv2.countNonZero(white_mask)


        #比大小
        color = max(red_count,blue_count,white_count)
        
        #空心
        if color == white_count:
            shape = 2
            print("空心")
            ROI_img_ = img[y:y+self.roi_w,x:x+self.roi_h]
            hsv = cv2.cvtColor(ROI_img_,cv2.COLOR_BGR2HSV)
       
            red_mask_ = cv2.inRange(hsv, self.red_low, self.red_up)
            red_mask_ = cv2.erode(red_mask_, None, iterations=self.red_iter)
            red_mask_ = cv2.dilate(red_mask_, None, iterations=self.red_iter)
            red_count_ = cv2.countNonZero(red_mask_)

            blue_mask_ = cv2.inRange(hsv, self.blue_low, self.blue_up)
            blue_mask_ = cv2.erode(blue_mask_, None, iterations=self.blue_iter)
            blue_mask_ = cv2.dilate(blue_mask_, None, iterations=self.blue_iter)
            blue_count_ = cv2.countNonZero(blue_mask_)

            color = max(red_count_,blue_count_)
            if color == red_count_:
                print("Red")
                color = 1
                
            elif color == blue_count_:
                print("Blue")
                color = 2

            return shape,color
        
        #实心
        else:
            print("实心")
            shape = 1
            if color == red_count:
                print("Red")
                color = 1
                
            elif color == blue_count:
                print("Blue")
                color = 2

        return shape,color

