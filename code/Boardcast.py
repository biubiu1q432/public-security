import cv2
import pygame
import RPi.GPIO as GPIO



class Boardcast:
    def __init__(self):
        pygame.mixer.init()
        #读取一张照片
        
        
    def b1(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/king/public security/sound/shape/1.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)        
    
    def b2(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/king/public security/sound/shape/2.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)           
    
    def b3(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/king/public security/sound/shape/3.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)            

    def b4(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/king/public security/sound/shape/4.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)

    def b5(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/king/public security/sound/shape/5.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
    
    def b6(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/king/public security/sound/shape/6.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
    
    def b7(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/king/public security/sound/shape/7.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)

    def b8(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/king/public security/sound/shape/8.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)

    def red(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/king/public security/sound/color/red.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)    
     
    def blue(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/king/public security/sound/color/blue.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
    
    def ID(self, id):
        # 加载mp3文件
        pygame.mixer.music.load("/home/king/public security/sound/point/" + str(id) + ".mp3")
        pygame.mixer.music.play()
        
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
        
        img = cv2.imread("/home/king/public security/code/img.jpg")
        img = cv2.resize(img, (640,480)) 

        # 在图像上绘制数字
        font = cv2.FONT_HERSHEY_SIMPLEX  # 字体类型
        font_scale = 4  # 字体大小
        font_color = (255, 0, 0)  # 字体颜色，这里使用蓝色 (BGR)
        thickness = 8 # 字体粗细
        position = (180, 180)  # 数字位置，这里假设在图像的左上角
        
        cv2.putText(img, str(id), position, font, font_scale, font_color, thickness)

        img = cv2.resize(img, (320,240)) 


        cv2.imshow("img", img)
        
        #等待1秒
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
    

    def Show_worlds(self,result):
        img = cv2.imread("/home/king/public security/result/"+str(result)+".png")
        #全屏窗口
        cv2.namedWindow("result", cv2.WINDOW_NORMAL)
        cv2.moveWindow("result",50,50)        
        img = cv2.resize(img,(400,200))
        cv2.imshow("1",img)
        cv2.waitKey(1500)
        cv2.destroyAllWindows()



# bc = Boardcast()
# bc.ID(12)