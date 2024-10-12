import time
import pygame
import serial
import Serial
import Detect

#全局变量
MOVE_DICT = None #移动字典
POINT_ID = None # 点号
MY_SERIAL = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)
COLOR_FLAG = None 

#运动
class MOVE:
    
    def __init__(self):
        global MOVE_DICT
        self.detect = Detect.Detect()
        self.read = Serial.Read_Serial()

        #跑图动作组
        MOVE_DICT = [
                    self.GO, 
                    self.CW, 
                    self.GO,
                    self.CCW,
                    self.Distance(100,2),
                    self.CCW,
                    self.GO,
                    self.CW,
                    self.Distance(100,2),
                    self.CW,
                    self.GO,
                    self.CCW,
                    self.Distance(100,2),
                    self.CCW,
                    self.GO,
                    self.CW,
                    self.GO,
                    self.CW,
                    self.GO,
                    self.CW,
                    self.GO,
                    self.CW,
                    self.Distance(100,2),
                    self.CW,
                    self.GO,
                    self.CCW,
                    self.GO,
                    self.CCW,
                    self.Distance(200,1),
                    self.CW,
                    self.CW,
                    self.GO,
                    self.CW,
                    self.Distance(100,2),
                    self.CW,
                    self.GO,
                    self.CCW,
                    self.Distance(50,2),
                    self.CW,
                    self.Distance(20,2),
        ]
    
    def GO(self):
        global MY_SERIAL,POINT_ID,COLOR_FLAG
        #发
        arr = "@|1|" + str(20) + "|" + str(60) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("GO")
        cnt = 0
        #收
        while True:
            cnt += 1
            try:
                data = MY_SERIAL.readline().decode('utf-8')
            except:
                continue
            if self.read.messages_config(data):
                continue
            
            #DONE
            if data[0] == '@':
                break
            
            #ID
            if data[0] == '!':
                id=self.read.read_ID(data)
                self.detect.boardcast.ID(id)

            #hsl
            if data[0] == '#' and cnt > 5:
                
                if self.read.read_HSL(data):
                    self.STOP()
                    time.sleep(0.5)
                    self.CW()
                    if self.detect.Detect():#侦擦任务完成，继续跑图
                        print("猜对了")
                        self.CCW()
                        self.GO()
                    else:
                        self.CW()
                        self.CW()
                        if self.detect.Detect():#侦擦任务完成，继续跑图
                            print("确实有")
                            self.CCW()
                            self.GO()
                        else:         #hsl误判断
                            print("误判")
                            self.CW()
                            self.GO()
                            return

    #mode1:hsl,done     mode0:done                              
    def Distance(self,dis,mode):
        global MY_SERIAL,POINT_ID,COLOR_FLAG
        #发
        arr = "@|6|" + str(25) + "|" + str(dis) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("Distance_100")
        cnt = 0
        #收
        while True:
            cnt += 1
            try:
                data = MY_SERIAL.readline().decode('utf-8')
            except:            
                continue
            if self.read.messages_config(data):
                continue
            
            #DONE
            if data[0] == '@':
                break
            
            #hsl
            # if data[0] == '#' and cnt > 5 and mode == 1:
                
            #     if self.read.read_HSL(data):
            #         self.STOP()
            #         time.sleep(0.5)
            #         self.CW()
            #         if self.detect.Detect():#侦擦任务完成，继续跑图
            #             print("猜对了")
            #             self.CCW()
            #             self.GO()
            #         else:
            #             self.CW()
            #             self.CW()
            #             if self.detect.Detect():#侦擦任务完成，继续跑图
            #                 print("确实有")
            #                 self.CCW()
            #                 self.GO()
            #             else:         #hsl误判断
            #                 print("误判")
            #                 self.CW()
            #                 self.GO()
            #                 return
    
    #顺时针
    def CW(self):
        global MY_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(90) + "|" + str(0) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("CW")
        #收
        while True:
            try:
                messages = MY_SERIAL.readline().decode('utf-8')
            except:            
                continue            
            if self.read.messages_config(messages):
                continue
            #DONE
            if messages[0] == '@':
                break
            #ID
            if messages[0] == '!':
                id=self.read.read_ID(messages)
                self.detect.boardcast.ID(id)
    #逆时针
    def CCW(self):
        global MY_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(-90) + "|" + str(0) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("CCW")
        #收
        while True:
            try:
                messages = MY_SERIAL.readline().decode('utf-8')
            except:            
                continue             
            if self.read.messages_config(messages):
                continue
            #DONE
            if messages[0] == '@':
                break
            #ID  
            if messages[0] == '!':
                id=self.read.read_ID(messages)
                self.detect.boardcast.ID(id)
    
    def STOP(self):
        arr = "@|5|" + str(0) + "|" + str(0) + "|" + str(0) + "#"
        MY_SERIAL.write(arr.encode("ascii"))
        print("STOP")

#播报
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
        pass

move = MOVE()
move.GO()

# #主函数
# if __name__ == '__main__':
#     move = MOVE()
#     #遍历动作组
#     for i in MOVE_DICT:
#         i()
          


