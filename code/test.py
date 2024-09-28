import serial
import threading


#全局变量
MOVE_DICT = None #移动字典
MOVE_FLAG = None  # 空闲/未完成：0   完成：1
POINT_ID = None # 点号
MY_SERIAL = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)
COLOR_FLAG = None 

#串口（下位机）
class Read_Serial:
    #构造函数
    def __init__(self):
        self.H = 10
        self.S = 23
        self.L = 36
        self.allow_err = 500

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
        judge_err = [abs(self.H-h),abs(self.S-s),abs(self.L-l)]
        judge_err = sum(judge_err)
        print(judge_err)

        #如果差距小于允许误差
        if judge_err < self.allow_err:
            return True
        else:
            return False

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
        MOVE_DICT = {
                    "0":self.GO, 
                    "1":self.GO, 
                    "2":self.GO, 
                    }
    
    def Para_Init(self):
        global MOVE_FLAG, MY_SERIAL,POINT_ID,COLOR_FLAG
        COLOR_FLAG = 0
        MOVE_FLAG = 0

    def GO(self):
        global MOVE_FLAG, MY_SERIAL,POINT_ID,COLOR_FLAG
        #发
        arr = "@|1|" + str(25) + "|" + str(100) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        #收
        while True:
            data = MY_SERIAL.readline()
            data = data.decode('utf-8')
            if data:
                #DONE
                if data[0] == '@':
                    print("DONE")
                    break
                #hsl
                if data[0] == '#':
                    #侦擦任务
                    if self.read.read_HSL(data):
                        print("侦擦任务")
                #ID
                            
    def Distance(self):
        global MOVE_FLAG, MY_SERIAL,POINT_ID,COLOR_FLAG
        #发
        arr = "@|6|" + str(25) + "|" + str(100) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        #收
        while True:
            data = MY_SERIAL.readline()
            data = data.decode('utf-8')
            if data:
                #DONE
                if data[0] == '@':
                    print("DONE")
                    break
                #hsl
                if data[0] == '#':
                    #侦擦任务
                    if self.read.read_HSL(data):
                        print("侦擦任务")
                #ID
            
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









