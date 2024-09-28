import serial


#全局变量
MOVE_FLAG = None  # 空闲/未完成：0   完成：1
POINT_ID = None # 点号
MY_SERIAL = serial.Serial("COM3", 9600)


class Read_Serial:
    #读串口，封装数据
    def Read(self):
        pass
        

class MOVE:
    #构造函数
    def __init__(self):
        global MOVE_DICT
        
        # self.detect = Detect()
        self.read_serial = Read_Serial()
        
        #跑图动作组
        MOVE_DICT = {
                    "0":self.GO, 
                    "1":self.GO, 
                    "2":self.GO, 
                    }
    
    def Para_Init(self):
        global MOVE_FLAG, MY_SERIAL,POINT_ID
        COLOR_FLAG = 0
        MOVE_FLAG = 0

    def GO(self):
        global MOVE_FLAG, MY_SERIAL,POINT_ID
        #发
        arr = "@|1|" + str(10) + "|" + str(100) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        #收
        while True:
            #读move_flag，color_flag
            self.read_serial.Read()
            
            #阻塞等待运动至尽头执行完毕
            if MOVE_FLAG == 1:
                self.Para_Init()
                break
            
            

    def Distance(self):
        global MOVE_FLAG, MY_SERIAL,POINT_ID
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