'''
核心逻辑
    1.侦察任务只会在GO过程中发生，所以仅在GO过程中检查color_flag，并作出相应动作
    2.把下位机回传的颜色数据封装为color_flag,把下位机回传的运动状态封装为move_flag
    3.采用扳机制全局变量color_flag，move_flag
    4.路径写死放入字典MOVE_DICT，通过KEY遍历函数组完成跑图任务
    5.报点任务最大概率在GO末尾过程产生，其余为CW和CCW
'''

import threading
import cv2
import serial
event = threading.Event()


#全局变量
MOVE_DICT = None
MOVE_FLAG = None  # 空闲/未完成：0   完成：1
POINT_ID = None # 点号
MY_SERIAL = serial.Serial("COM3", 9600)


#一次侦察流程，注意color_flag归位
class Detect:
    def __init__(self):
        #摄像头初始化
        self.cap = cv2.VideoCapture(0)
        #语言播报对象
        self.boardcast = Boardcast()

    #一次侦察流程
    def Detect(self):
        pass
    #一次形状提取
    def Shape_Detect(self):
        pass
    #一次颜色提取
    def Color_Detect(self):
        pass

#一次语言播报    
class Boardcast:
    def __init__(self):
        pass
    def red(self):
        pass
    def green(self):
        pass
    def blue(self):
        pass
    def yellow(self):
        pass


#串口（下位机）
'''
把消息翻译为MOVE_FLAG，COLOR_FLAG,HSV,POINT_ID
'''
class Read_Serial:
     
    #读串口，封装数据
    def Read(self):
        pass
        

#跑图，注意move_flag归位
'''
    1.下位机主动回传运动完成状态（一次）和颜色情况（连续/一次） 
    2.在尽头主动停下
    3.侦察任务，爆点任务出现在GO过程中，所以下位机尽量让GO完成信号在读卡器发信号前回传，使得所有逻辑在GO中完成
'''        
class MOVE:
    #构造函数
    def __init__(self):
        global MOVE_DICT
        
        self.detect = Detect()
        self.read_serial = Read_Serial()
        
        #跑图动作组
        MOVE_DICT = {
                    "0":self.GO, 
                    "1":self.GO, 
                    "2":self.GO, 

                    }
    
    def Para_Init(self):
        global MOVE_FLAG, MY_SERIAL,COLOR_FLAG,POINT_ID
        COLOR_FLAG = 0
        MOVE_FLAG = 0

    def GO(self):
        global MOVE_FLAG, MY_SERIAL,COLOR_FLAG,POINT_ID
        #发
        MY_SERIAL.write("".encode('utf-8'))
        #收
        while True:
            #读move_flag，color_flag
            self.read_serial.Read()
            
            #阻塞等待运动至尽头执行完毕
            if MOVE_FLAG == 1:
                self.Para_Init()
                break
            
            #突发侦察任务（只有前进过程才会用到）
            if COLOR_FLAG == 1:#红色
                #转向
                self.STOP()
                self.CW()
                #侦察
                self.detect.Detect()
                #继续本次执行运动任务
                MOVE_DICT[KEY]()
            
            if COLOR_FLAG == 2:#绿色
                #转向
                self.STOP()
                self.CCW()
                #侦察
                self.detect.Detect()
                #继续本次执行运动任务
                MOVE_DICT[KEY]()

    def CW(self):
        global MOVE_FLAG, MY_SERIAL
        #发
        MY_SERIAL.write("".encode('utf-8'))
        #收
        while True:
            #读move_flag，color_flag
            self.read_serial.Read()
            
            #等待运动执行完毕
            if MOVE_FLAG == 1:
                self.Para_Init()
                break

    def CCW(self):
        global MOVE_FLAG, MY_SERIAL       
        #发
        MY_SERIAL.write("".encode('utf-8')) 
        #收
        while True:
            #读move_flag，color_flag
            self.read_serial.Read()
            
            #等待运动执行完毕
            if MOVE_FLAG == 1:
                self.Para_Init()
                break
 
    def STOP(self):
        global MOVE_FLAG, MY_SERIAL
        #发命令
        MY_SERIAL.write("".encode('utf-8'))
        while True:
            #读move_flag，color_flag
            self.read_serial.Read()
            
            #等待运动执行完毕
            if MOVE_FLAG == 1:
                self.Para_Init()
                break


if __name__ == "__main__":
    move = MOVE()
    for KEY in MOVE_DICT:
        MOVE_DICT[KEY]()
    
        
