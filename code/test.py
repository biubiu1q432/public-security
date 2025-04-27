
import cv2
import numpy as np




'''摄像头测试'''
cap = cv2.VideoCapture(0)
cap.set(3, 640)#宽度
cap.set(4, 480)#高度
while True:
    ret, frame = cap.read()
    frame=cv2.resize(frame,(300,300))

    #二值化

    #找边界

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''摄像头测试'''


'''颜色识别测试(hsv)'''
# #颜色阈值
# red_low = np.array([120, 47, 75])
# red_up = np.array([209, 255, 194])
# red_iter = 0

# blue_low = np.array([92, 95, 0])
# blue_up = np.array([118, 255, 156])
# blue_iter = 0

# white_low = np.array([0, 0, 0])
# white_up = np.array([129, 112, 255])
# white_iter = 0


# #分别二值化
# ROI_img = cv2.imread("/home/king/public security/code/image.png")
# hsv = cv2.cvtColor(ROI_img,cv2.COLOR_BGR2HSV)

# #分别二值化
# red_mask = cv2.inRange(hsv, red_low, red_up)
# red_mask = cv2.erode(red_mask, None, iterations=red_iter)
# red_mask = cv2.dilate(red_mask, None, iterations=red_iter)
# red_count = cv2.countNonZero(red_mask)

# blue_mask = cv2.inRange(hsv, blue_low, blue_up)
# blue_mask = cv2.erode(blue_mask, None, iterations=blue_iter)
# blue_mask = cv2.dilate(blue_mask, None, iterations=blue_iter)
# blue_count = cv2.countNonZero(blue_mask)

# white_mask = cv2.inRange(hsv, white_low, white_up)
# white_mask = cv2.erode(white_mask, None, iterations=white_iter)
# white_mask = cv2.dilate(white_mask, None, iterations=white_iter)
# white_count = cv2.countNonZero(white_mask)

# #显示
# print("red_count:",red_count)
# print("blue_count:",blue_count)
# print("white_count:",white_count)

# red_mask = cv2.resize(red_mask, (300,300)) 
# blue_mask = cv2.resize(blue_mask, (300,300)) 
# white_mask = cv2.resize(white_mask, (300,300)) 

# cv2.imshow("red_mask", red_mask)
# cv2.imshow("blue_mask", blue_mask)
# cv2.imshow("white_mask", white_mask)
# cv2.imshow("roi", ROI_img)
# cv2.waitKey(0)
'''颜色识别测试'''




'''轮廓识别测试(except_white + canny)'''
# cap = cv2.VideoCapture(0) 

# except_white_threold = 81
# areaMin = 40000
# rec_min = 1.3
# rec_max = 1.6
# tra = 20

# while True:
#         ret,img = cap.read()
#         if ret:
            
#             #高斯滤波--》imgBlur
#             imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
            
#             #转灰度--》imgGray
#             imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
            
#             #中值滤波-->imgBlur2
#             imgBlur2 = cv2.medianBlur(imgGray,7)
            
#             #二值化+扩边界
#             ret,imgBlur2 = cv2.threshold(imgBlur2,except_white_threold,255,cv2.THRESH_BINARY_INV)
#             # ret2, imgBlur2 = cv2.threshold(imgBlur2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#             imgBlur2 = cv2.copyMakeBorder(imgBlur2,20,20,20,20,cv2.BORDER_CONSTANT,value=[0,0,0])

#             #Canny整图边界二值化--》imgCanny
#             imgCanny = cv2.Canny(imgBlur2,50,88)

#             #膨胀二值边界--》imgDil
#             kernel = np.ones((5, 5))
#             imgDil = cv2.dilate(imgCanny, kernel, 1)

#             imgDil_ = cv2.resize(imgDil, (300,200)) 
#             cv2.imshow("3", imgDil_)
#             cv2.waitKey(1)
            
#             #遍历轮廓
#             contours, hierarchy = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#             for cnt in contours:
#                 area = cv2.contourArea(cnt)
#                 print("area:",str(area))

#                 if area > areaMin:
                    
#                     peri = cv2.arcLength(cnt, True)
#                     approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)              
                    
#                     print("approx:",str(len(approx)))
#                     #过滤
#                     if len(approx) != 4:
#                         img_ = cv2.resize(img, (300,200)) 
#                         cv2.imshow("fliter", img_)
#                         cv2.waitKey(1)
                    
#                     x, y ,w,h = cv2.boundingRect(approx)
                    
#                     x-=20
#                     y-=20
                    
#                     #中心点
#                     center_x = int((x+x+w)/2)  
#                     center_y = int((y+y+h)/2)


#                     #形状判断
#                     approx = np.array(approx)
#                     approx = np.squeeze(approx, axis=1)
#                     sorted_points = approx[np.argsort(approx[:, 1],)] #按y值从小到大排序

#                     #------->x
#                     #|   A   B
#                     #|   C   D
#                     #v
                    
#                     #AB
#                     if sorted_points[0][0] <= sorted_points[1][0]:
#                         A = sorted_points[0]
#                         B = sorted_points[1]
#                     elif sorted_points[0][0] > sorted_points[1][0]:
#                         A = sorted_points[1]
#                         B = sorted_points[0]
#                     #CD
#                     if sorted_points[2][0] <= sorted_points[3][0]:
#                         C = sorted_points[2]
#                         D = sorted_points[3]
#                     elif sorted_points[2][0] >= sorted_points[3][0]:
#                         C = sorted_points[3]
#                         D = sorted_points[2]
    
#                     AB = int(np.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2))#AB距离计算               
#                     CD = int(np.sqrt((C[0]-D[0])**2 + (C[1]-D[1])**2)) #CD距离计算
#                     AC = int(np.sqrt((A[0]-C[0])**2 + (A[1]-C[1])**2))#AC距离计算
                       
#                     print(abs(AB/AC))                   
#                     if CD-AB > tra:
#                         print("上梯形")
#                         shape = 2
#                     elif AB-CD > tra:
#                         print("下梯形")
#                         shape = 3
                    
#                     elif (AB/AC) >= rec_min and (AB/AC) <= rec_max:
#                         print("矩形")
#                         shape = 1

#                     else:
#                         print("正方形")
#                         shape = 4    
                    
#                     #调试
#                     cv2.drawContours(img, cnt, -1, (255, 0, 255), 7)
#                     cv2.putText(img, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
#                                 (0, 255, 0), 2)
#                     cv2.putText(img, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
#                                 (0, 255, 0), 2)
 
#             img = cv2.resize(img, (300,200)) 
#             cv2.imshow("Result", img)
#             cv2.waitKey(1)
'''轮廓识别测试(except_white + canny)'''






'''微调识别测试(except_white + center_X)'''
# cap = cv2.VideoCapture(0)

# except_white_threold = 81
# center_min = 190
# center_max = 400

# while True:
#     ret,img = cap.read()
#     if ret:    

#         #灰度
#         gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#         dst = cv2.GaussianBlur(gray,(7,7),0)
#         ret,thresh = cv2.threshold(dst,except_white_threold,255,cv2.THRESH_BINARY_INV)
            
#         # hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#         # thresh = cv2.inRange(hsv, except_white_low, except_white_up)

#         #获取色块轮廓（cv2.findContours()函数返回的轮廓列表是按轮廓大小排序的）
#         contours,hierarchy= cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)                
#         if contours :
#             for contour in contours:#筛选出目标色块
#                 x, y, w, h = cv2.boundingRect(contour)
                
#                 #调试
#                 cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                        
#                 area = w*h
#                 print("area:",area)
#                 #面积过滤
#                 if area <= 20000 or area >=90000:
#                     continue
            
#                 center_x = (x+x+w)/2 
                
#                 print(center_x)

#                 #范围判定
#                 if center_x >= center_min and center_x <= center_max:#中心在范围内:1
#                     print("中心在范围内")
#                 elif center_x < center_min:#太左----》左转一点:2
#                     print("太左----》左转一点")
#                 elif center_x > center_max:#太右----》右转一点:3
#                     print("太右----》右转一点")


#         img_1 = cv2.resize(img, (100,100)) 
#         cv2.imshow("1", img_1)

#         img_ = cv2.resize(thresh, (100,100)) 
#         cv2.imshow("2", img_)
#         cv2.waitKey(1)
'''微调识别测试(except_white + center_X)'''
