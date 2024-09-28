import pygame

class Boardcast:
    def __init__(self):
        pygame.mixer.init()
    
    def Recentage(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/q/public security/sound/shape/rec.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)        
    
    def Triangle(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/q/public security/sound/shape/tri.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)        
    
    def Cricle(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/q/public security/sound/shape/cri.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)        
    
    def Star(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/q/public security/sound/shape/star.mp3")
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
        pygame.mixer.music.load("/home/q/public security/sound/color/red.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)    
    
    def green(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/q/public security/code/sound/color/green.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    
    def blue(self):
        # 加载mp3文件
        pygame.mixer.music.load("/home/q/public security/sound/color/blue.mp3")
        # 播放音乐
        pygame.mixer.music.play()
        # 等待音乐播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    
    def yellow(self):
        pass

