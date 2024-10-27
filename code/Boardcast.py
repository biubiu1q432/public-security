import cv2
import pygame

class Boardcast:
    def __init__(self):
        pygame.mixer.init()
        #读取一张照片
        self.img = cv2.imread("/home/king/public security/code/img.jpg")
        self.img = cv2.resize(self.img, (1000,1000)) 

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
        
        #全屏显示图片
        cv2.imshow("img", self.img)
        #等待1秒
        cv2.waitKey(600)
        #关闭图片
        cv2.destroyAllWindows()



# bc = Boardcast()
# bc.ID(2)
