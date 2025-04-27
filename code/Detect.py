'''
用于测试一次侦察任务
'''
from PIL import Image
import cv2
import numpy as np
import Boardcast
import time

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
        self.cap.set(3, 640)#宽度
        self.cap.set(4, 480)#高度
    
        self.brocast=Boardcast.Boardcast()

        '''可调参数'''
        #Canny阈值
        self.threshold1 = 50
        self.threshold2 = 88
        #面积过滤
        self.areaMin = 10000#30000
        #形状
        self.rec_min = 0.7
        self.rec_max = 1.3
        
        # self.squ_min = 0.8
        # self.squ_max = 1.2
        
        self.tra = 20
        
        #ROI
        self.roi_x = 7  #左上角
        self.roi_y = 7
        self.roi_w = 3  
        self.roi_h = 3  
        self.ROI_range= 10 #空心
        
        #颜色阈值
        self.red_low = np.array([0, 69,90])
        self.red_up = np.array([198, 228, 179])
        self.red_iter = 0
        
        self.blue_low = np.array([85, 98, 43])
        self.blue_up = np.array([133, 255, 152])
        self.blue_iter = 0
        
        self.white_low = np.array([53, 15, 119])
        self.white_up = np.array([141, 174, 217])
        self.white_iter = 0       
        
        # self.except_white_low = np.array([0, 36, 0])
        # self.except_white_up = np.array([255, 232, 186])
        # self.except_white_iter = 0

        self.except_white_threold = 93
        self._threold = 50
        
        #根据中心点微调
        self.center_min = 190
        self.center_max = 400

        self.imgnext = None
    #return ret,shape,color
    def Detect(self):
        Shape = []
        Color = []
        Shapes = []
        Colors = []
        Best_Color = []
        Best_Shape = []
        result = -1     #映射结果默认值
        
        for i in range(0,60):
            
            #拍照
            ret, frame = self.cap.read()
            
            #图片
        
            #空心蓝色矩形
            # frame = cv2.imread('/home/king/public security/photo/9.jpg')
            
            #空心红色夏提刑
            # frame = cv2.imread('/home/king/public security/photo/31.jpg')

            # #实习红色
            # frame = cv2.imread('/home/king/public security/photo/16.jpg')

            # #蓝色
            # frame = cv2.imread('/home/king/public security/photo/37.jpg')


            # cv2.imshow("f12312",frame)
            # cv2.waitKey(1)
            
            ret = True
            if ret:
                img,shape1,center_x,center_y,x,y = self.Shape_Detect(frame)
                #print("llllllll",shape1,center_x,center_y,x,y)
                if shape1 == None or center_x == None or center_y == None or x == None or y == None :
                    continue

                shape2,color=self.Color_Detect(img,center_x,center_y,x,y)
                
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
                Shapes.append(Shape)                
                Colors.append(Color)


        cv2.destroyAllWindows()            
        
        
        #过滤
        if len(Shapes) <= 4:
            return True,result

        #统计出出现次数最多的形状和颜色
        try:
            Best_Shape = max(set(Shapes), key=(Shapes.count))
            Best_Color = max(set(Colors), key=(Colors.count))
        except:
            print("没有检测到轮廓")
            return True,result
        
        
        #调试
        print("Best Shape:",Best_Shape)
        print("Best Color:",Best_Color)

        
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
        if Best_Shape == 1:
            self.brocast.b1()
        elif Best_Shape == 2:
            self.brocast.b2()
        elif Best_Shape == 3:
            self.brocast.b3()
        elif Best_Shape == 4:
            self.brocast.b4()
        elif Best_Shape == 5:
            self.brocast.b5()
        elif Best_Shape == 6:
            self.brocast.b6()
        elif Best_Shape == 7:
            self.brocast.b7()
        elif Best_Shape == 8:
            self.brocast.b8()
        #颜色播报
        if Best_Color == 1:
            self.brocast.red() 
        elif Best_Color == 2:
            self.brocast.blue()
        
        #最终结果映射
        if Best_Shape == 1 and Best_Color == 1:
            result = 1#实心矩形 红色
        elif Best_Shape == 1 and Best_Color == 2:
            result = 2#实心矩形 蓝色
        elif Best_Shape == 2 and Best_Color == 1:
            result = 3#空心矩形 红色
        elif Best_Shape == 2 and Best_Color == 2:
            result = 4#空心矩形 蓝色
        elif Best_Shape == 3 and Best_Color == 1:
            result = 5#实心上梯形 红色
        elif Best_Shape == 3 and Best_Color == 2:
            result = 6#实心上梯形 蓝色
        elif Best_Shape == 4 and Best_Color == 1:
            result = 7#空心上梯形 红色
        elif Best_Shape == 4 and Best_Color == 2:
            result = 8#空心上梯形 蓝色
        elif Best_Shape == 5 and Best_Color == 1:
            result = 9#实心下梯形 红色
        elif Best_Shape == 5 and Best_Color == 2:
            result = 10#实心下梯形 蓝色
        elif Best_Shape == 6 and Best_Color == 1:
            result = 11#空心下梯形 红色
        elif Best_Shape == 6 and Best_Color == 2:
            result = 12#空心下梯形 蓝色
        elif Best_Shape == 7 and Best_Color == 1:
            result = 13#实心正方形 红色
        elif Best_Shape == 7 and Best_Color == 2:
            result = 14#实心正方形 蓝色
        elif Best_Shape == 8 and Best_Color == 1:
            result = 15#空心正方形 红色
        elif Best_Shape == 8 and Best_Color == 2:
            result = 16#空心正方形 蓝色
        
        return False,result
    
    #扳机式参数：shape,center_x,center_y,left_x,left_y
    def Shape_Detect(self,img):
        #扳机式变量    
        shape = None
        center_x =None
        center_y = None
        x = None
        y = None


        frame = img
        
        #高斯滤波--》imgBlur
        imgBlur = cv2.GaussianBlur(img, (3, 3), 1)
        
        #转灰度--》imgGray
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
        
        #中值滤波-->imgBlur2
        #imgBlur2 = cv2.medianBlur(imgGray,7)
        imgBlur2 = imgGray
        #二值化+扩边界

        self._threold += 2
        if(self._threold > 170):
            self._threold = 50
        #print("_threold = " + str(self._threold))

        ret,imgBlur2 = cv2.threshold(imgBlur2,self._threold,255,cv2.THRESH_BINARY_INV)#self.except_white_threold

        #膨胀二值边界--》imgDil
        kernel = np.ones((3, 3))
        imgBlur2 = cv2.dilate(imgBlur2, kernel, 1)

        #过滤
        a_find = 0
        a = 0
        b_find = 0
        b = 639


        strips = []
        for i in range(0,300):
            strips = imgBlur2[:, i*2]

            strip_array = np.array(strips)
            total_pixels = 480
            white_pixels = np.sum(strip_array == 255)
            ratio = white_pixels / total_pixels

            if(ratio < 0.1):
                if(a_find == 0):
                    a = i*2
                    a_find = 1
                    continue
        strips = []
        for i in range(0,300):
            strips = imgBlur2[:, 639 - i*2]

            strip_array = np.array(strips)
            total_pixels = 480
            white_pixels = np.sum(strip_array == 255)
            ratio = white_pixels / total_pixels
            if(ratio < 0.1):
                if(b_find == 0):
                    b = 639 - i*2
                    b_find = 1
                    continue

        if(a>b):
            b = a + 10
        

        imgBlur2 = imgBlur2[0:480, a:b]
        frame = frame[0:480, a:b]

        # cv2.imshow("im",imgBlur2)
        # cv2.waitKey(1)

        imgBlur2 = cv2.copyMakeBorder(imgBlur2,20,20,20,20,cv2.BORDER_CONSTANT,value=[0,0,0])
        frame = cv2.copyMakeBorder(img,20,20,20,20,cv2.BORDER_CONSTANT,value=[0,0,0])

        # 
        self.imgnext = imgBlur2

        #Canny整图边界二值化--》imgCanny
        imgCanny = cv2.Canny(imgBlur2,50,88)
        imgCanny_ = cv2.resize(imgCanny, (300,200)) 
        #cv2.imshow("3", imgCanny_)
        #cv2.waitKey(1)

        #遍历轮廓
        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        #print(len(contours))
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # peri = cv2.arcLength(cnt, True)
            # approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)              
            # x, y ,w, h= cv2.boundingRect(approx)   
            #area = w*h

            # print("area:",str(area))

            # time.sleep(0.5)
            if area > self.areaMin:
                
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)              
                x, y ,w,h = cv2.boundingRect(approx)          
                                
                # x -= 20
                # y -= 20
                            
                # print("approx:",str(len(approx)))
                
                #过滤
                if len(approx) != 4:
                    #img_ = cv2.resize(img, (300,200)) 
                    #cv2.imshow("fliter", img_)
                    #cv2.waitKey(1)
                    continue
                # if x <= 10 or x >=630:
                #     continue
                
    
                #中心点
                center_x = int((x+x+w)/2)  
                center_y = int((y+y+h)/2)


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
                x = C[0]+self.roi_x
                y = C[1]-self.roi_y
                
     

                print("ratio:",AB/CD)

                #              实心1     空心2
                #矩形   1   
                #上梯形 2
                #下梯形 3
                #正方形 4
                #print(AB/CD)
                if AB/CD < 0.75:#self.tra:
                    print("上梯形")
                    shape = 2
                elif AB/CD > 1.3:#self.tra:
                    print("下梯形")
                    shape = 3
                
                elif (AB/AC) >= self.rec_max or (AB/AC) <= self.rec_min:
                    print("矩形")
                    shape = 1

                else:
                    print("正方形")
                    shape = 4    


                # cv2.imshow("1231",img_)
                # cv2.waitKey(1)        
        
        
        #         #调试
        #        cv2.drawContours(img_, cnt, -1, (25, 0, 205), 7)
        #         cv2.putText(img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
        #                     (0, 255, 0), 2)
        #         cv2.putText(img, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
        #                     (0, 255, 0), 2)
        #         #    print("Points: " + str(len(approx)))         
        #         #    print("Area: "+ str(int(area)))        
        
        # img_ = cv2.resize(img_, (300,200)) 
        # cv2.imshow("Result", img_)
        # cv2.waitKey(1)
        
        # img_ = cv2.resize(img, (300,200)) 
        #cv2.imshow("1", img_)
        
        
        return frame,shape,center_x,center_y,x,y
      
        #一次颜色提取，返回颜色
    
    #color:1红色 2蓝色
    def Color_Detect(self,img,center_x,center_y,x,y):
        
        shape = None
        color = None
        
        #限幅防止报错
        size = img.shape
        w = size[1] #宽度
        h = size[0] #高度
        if center_x <=self.ROI_range or center_x >= w-self.ROI_range:
            center_x = self.ROI_range
        if center_y <=self.ROI_range or center_y >= h-self.ROI_range:
            center_y = self.ROI_range

        #中心截图:  左上角--》右下角
        ROI_img = img[center_y-self.ROI_range:center_y+self.ROI_range, center_x-self.ROI_range:center_x+self.ROI_range]
        hsv = cv2.cvtColor(ROI_img,cv2.COLOR_BGR2HSV)
        
        #调试
        # cv2.imshow("ROI_img", ROI_img)
        #cv2.imwrite("/home/king/public security/code/roi.jpg",ROI_img)
        # cv2.waitKey(1)


        #分别二值化
        red_mask = cv2.inRange(hsv, self.red_low, self.red_up)
        # red_mask = cv2.erode(red_mask, None, iterations=self.red_iter)
        # red_mask = cv2.dilate(red_mask, None, iterations=self.red_iter)
        red_count = cv2.countNonZero(red_mask)

        blue_mask = cv2.inRange(hsv, self.blue_low, self.blue_up)
        # blue_mask = cv2.erode(blue_mask, None, iterations=self.blue_iter)
        # blue_mask = cv2.dilate(blue_mask, None, iterations=self.blue_iter)
        blue_count = cv2.countNonZero(blue_mask)

        white_mask = cv2.inRange(hsv, self.white_low, self.white_up)
        # white_mask = cv2.erode(white_mask, None, iterations=self.white_iter)
        # white_mask = cv2.dilate(white_mask, None, iterations=self.white_iter)
        white_count = cv2.countNonZero(white_mask)


        #比大小
        color = max(red_count,blue_count,white_count)
        
        #空心
        if color == white_count:
            shape = 2
            print("空心") 

            x = x + 5
            y = y - 5
            ROI_img_ = img[y-self.roi_w:y,x:x+self.roi_h]
            # ROI_img_ = img[y-50:y+50,x-50:x+50]


            #for colors in ROI_img_[1][1]:
            
            #print(colors)
            colors_B = ROI_img_[1][1][0]
            colors_R = ROI_img_[1][1][2]

            #差距
            dis = int(colors_R)-int(colors_B)
            print("dis",dis)
            if dis >= 50:
                color = 1
            else:
                color = 2

            # print("colors_B",colors_B)
            # print("colors_R",colors_R)

            #调试
            # cv2.imshow("ROI_img_", ROI_img_)
            #cv2.imwrite("/home/king/public security/code/roi_.jpg",ROI_img_)
            # cv2.waitKey(1)
       
       







       
            # hsv = cv2.cvtColor(ROI_img_,cv2.COLOR_BGR2HSV)
       
            # blue_mask_ = cv2.inRange(hsv, self.blue_low, self.blue_up)
            # # blue_mask_ = cv2.erode(blue_mask_, None, iterations=self.blue_iter)
            # # blue_mask_ = cv2.dilate(blue_mask_, None, iterations=self.blue_iter)
            # blue_count_ = cv2.countNonZero(blue_mask_)

            # red_mask_ = cv2.inRange(hsv, self.red_low, self.red_up)
            # # red_mask_ = cv2.erode(red_mask_, None, iterations=self.red_iter)
            # # red_mask_ = cv2.dilate(red_mask_, None, iterations=self.red_iter)
            # red_count_ = cv2.countNonZero(red_mask_)


            #print("red:",red_count_)
            #print("blue:",blue_count_)

            # color = max(red_count_,blue_count_)
            if color == 1:
                print("Red")
                color = 1
                
            elif color == 2:
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

    #判定中心偏差 
    def judge_center(self):
        a=[]     
        for i in range(0,11):
            ret,img = self.cap.read()
            if ret:    

                #灰度
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                dst = cv2.GaussianBlur(gray,(7,7),0)
                ret,thresh = cv2.threshold(dst,self.except_white_threold,255,cv2.THRESH_BINARY_INV)
                    
                # hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                # thresh = cv2.inRange(hsv, self.except_white_low, self.except_white_up)

                #获取色块轮廓（cv2.findContours()函数返回的轮廓列表是按轮廓大小排序的）
                contours,hierarchy= cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)                
                if contours :
                    for contour in contours:#筛选出目标色块
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        #调试
                        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                
                        area = w*h
                        print("area:",area)
                        #面积过滤
                        if area <= 20000 or area >=90000:
                            continue
                    
                        center_x = (x+x+w)/2 
                        
                        #print(center_x)

                        #范围判定
                        if center_x >= self.center_min and center_x <= self.center_max:#中心在范围内:1
                            a.append(1)
                            #print("中心在范围内")
                        elif center_x < self.center_min:#太左----》左转一点:2
                            a.append(2)
                            #print("太左----》左转一点")
                        elif center_x > self.center_max:#太右----》右转一点:3
                            a.append(3)
                            #print("太右----》右转一点")
        

                img_1 = cv2.resize(img, (100,100)) 
                cv2.imshow("1", img_1)

                img_ = cv2.resize(thresh, (100,100)) 
                cv2.imshow("2", img_)
                cv2.waitKey(1)

        cv2.destroyAllWindows()
        
        #拿到出现最多的数字
        try:
            num = max(set(a), key=(a.count))
            if(num == 1):
                print("中间")
            if(num == 2):
                print("左边")
            if(num == 3):
                print("右边")
            return True,num
        #白板
        except:
            return False,0


# d = Detect()
# # # num=d.judge_center() 
# # # print(num)
# # # while True:

# # #d.judge_center()

# # #time.sleep(2)

# d.Detect()


