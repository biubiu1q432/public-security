import serial


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
        global MOVE_FLAG, MY_SERIAL,COLOR_FLAG,POINT_ID
        COLOR_FLAG = 0
        MOVE_FLAG = 0

    def GO(self):
        global MOVE_FLAG, MY_SERIAL,COLOR_FLAG,POINT_ID
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

    def Distance(self):
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