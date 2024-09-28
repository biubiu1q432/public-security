import serial
import threading


#全局变量
MOVE_DICT = None #移动字典
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
        self.allow_err = 10

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
        # print(judge_err)

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
        MOVE_DICT = [
                    self.GO, 
                    self.CW, 
                    self.GO,
                    self.CCW,
                    self.Distance_100,
                    self.CCW,
                    self.GO,
                    self.CW,
                    self.Distance_100,
                    self.CW,
                    self.GO,
                    self.CCW,
                    self.Distance_100,
                    self.CCW,
                    self.GO,
                    self.CW,
                    self.GO,
                    self.CW,
                    self.GO,
                    self.CW,
                    self.GO,
                    self.CW,
                    self.Distance_100,
                    self.CW,
                    self.GO,
                    self.CCW,
                    self.GO,
                    self.CCW,
                    self.Distance_100,
                    self.Distance_100,
                    self.CW,
                    self.CW,
                    self.GO,
                    self.CW,
                    self.Distance_100,
                    self.CW,
                    self.GO,
                    self.CCW,
                    self.Distance_50,
                    self.CW,
                    self.Distance_20,
        ]
    
    def GO(self):
        global MY_SERIAL,POINT_ID,COLOR_FLAG
        #发
        arr = "@|1|" + str(30) + "|" + str(60) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("GO")
        #收
        while True:
            data = MY_SERIAL.readline()
            data = data.decode('utf-8')
            if data:
                #DONE
                if data[0] == '@':
                    break
                #hsl
                if data[0] == '#':
                    #侦擦任务
                    if self.read.read_HSL(data):
                        print("侦擦任务")
                #ID
                    
    def Distance_100(self):
        global MY_SERIAL,POINT_ID,COLOR_FLAG
        #发
        arr = "@|6|" + str(30) + "|" + str(100) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("Distance")
        #收
        while True:
            data = MY_SERIAL.readline()
            data = data.decode('utf-8')
            if data:
                #DONE
                if data[0] == '@':
                    break
                #hsl
                if data[0] == '#':
                    #侦擦任务
                    if self.read.read_HSL(data):
                        print("侦擦任务")
                #ID
    def Distance_50(self):
        global MY_SERIAL,POINT_ID,COLOR_FLAG
        #发
        arr = "@|6|" + str(30) + "|" + str(50) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("Distance")
        #收
        while True:
            data = MY_SERIAL.readline()
            data = data.decode('utf-8')
            if data:
                #DONE
                if data[0] == '@':
                    break
                #hsl
                if data[0] == '#':
                    #侦擦任务
                    if self.read.read_HSL(data):
                        print("侦擦任务")
                #ID     
    def Distance_20(self):
        global MY_SERIAL,POINT_ID,COLOR_FLAG
        #发
        arr = "@|6|" + str(30) + "|" + str(20) + "|" + str(75) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("Distance")
        #收
        while True:
            data = MY_SERIAL.readline()
            data = data.decode('utf-8')
            if data:
                #DONE
                if data[0] == '@':
                    break

    #顺时针
    def CW(self):
        global MY_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(90) + "|" + str(0) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("CW")
        #收
        while True:
            data = MY_SERIAL.readline()
            data = data.decode('utf-8')
            if data:
                #DONE
                if data[0] == '@':
                    break

                #ID
    #逆时针
    def CCW(self):
        global MY_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(-90) + "|" + str(0) + "#"
        MY_SERIAL.write(arr.encode('utf-8'))
        print("CCW")
        #收
        while True:
            data = MY_SERIAL.readline()
            data = data.decode('utf-8')
            if data:
                #DONE
                if data[0] == '@':
                    break       

    def STOP(self):
        pass


#主函数
if __name__ == '__main__':
    move = MOVE()
    #遍历动作组
    for i in MOVE_DICT:
        i()
        


