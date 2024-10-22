import time
import serial
import Serial
import Detect

#全局变量
MOVE_SERIAL = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)
K2L0_SERIAL = serial.Serial(port="/dev/ttyUSB1",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)
#运动
class MOVE:
    
    def __init__(self):
        self.detect = Detect.Detect()
        self.read = Serial.Read_Serial()
    
    def GO(self):
        global MOVE_SERIAL,K2L0_SERIAL
        #发
        arr = "@|1|" + str(20) + "|" + str(60) + "|" + str(75) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("GO")
        flag_id = True
        #收
        while True:
            try:
                data = MOVE_SERIAL.readline().decode('utf-8')
                k2l0 = K2L0_SERIAL.readline().decode('utf-8')
            except:
                continue
            if self.read.messages_config(data):
                continue
            
            #DONE
            if data[0] == '@':
                break
            
            #ID
            if data[0] == '!' and flag_id == True:
                flag_id = False
                id=self.read.read_ID(data)
                self.detect.boardcast.ID(id)

            #k2l0
            if k2l0 == "ok\r\n":    
                self.STOP()
                time.sleep(0.5)
                self.CW()
                if self.detect.Detect():#侦擦任务完成，继续跑图
                    print("猜对了")
                    self.CCW()
                    self.GO()#递归
                    return
                
                else:
                    self.Turn()
                    if self.detect.Detect():#侦擦任务完成，继续跑图
                        print("确实有")
                        self.CCW()
                        self.GO()#递归
                        return
                    else:         #hsl误判断
                        print("误判")
                        self.CW()
                        self.GO()#递归
                        return
    
    def Distance(self,dis):
        global MOVE_SERIAL,K2L0_SERIAL
        #发
        arr = "@|6|" + str(25) + "|" + str(dis) + "|" + str(75) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("Distance_100")
        #收
        while True:
            try:
                data = MOVE_SERIAL.readline().decode('utf-8')
                k2l0 = K2L0_SERIAL.readline().decode('utf-8')
            except:            
                continue
            if self.read.messages_config(data):
                continue
            
            #DONE
            if data[0] == '@':
                break
            
            #k2l0
            if k2l0 == "ok\r\n":    
                self.STOP()
                time.sleep(0.5)
                self.CW()
                if self.detect.Detect():#侦擦任务完成，继续跑图
                    print("猜对了")
                    self.CCW()
                    self.GO()#递归
                    return
                
                else:
                    self.Turn()
                    if self.detect.Detect():#侦擦任务完成，继续跑图
                        print("确实有")
                        self.CCW()
                        self.GO()#递归
                        return
                    else:         #hsl误判断
                        print("误判")
                        self.CW()
                        self.GO()#递归
                        return    
    #顺时针
    def CW(self):
        global MOVE_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(90) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("CW")
        flag_id=True
        #收
        while True:
            try:
                messages = MOVE_SERIAL.readline().decode('utf-8')
            except:            
                continue            
            if self.read.messages_config(messages):
                continue
            #DONE
            if messages[0] == '@':
                break
            #ID
            if messages[0] == '!' and flag_id == True:
                flag_id = False
                id=self.read.read_ID(messages)
                self.detect.boardcast.ID(id)
    
    #逆时针
    def CCW(self):
        global MOVE_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(-90) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("CCW")
        flag_id=True
        #收
        while True:
            try:
                messages = MOVE_SERIAL.readline().decode('utf-8')
            except:            
                continue             
            if self.read.messages_config(messages):
                continue
            #DONE
            if messages[0] == '@':
                break
            #ID  
            if messages[0] == '!' and flag_id == True:
                flag_id = False
                id=self.read.read_ID(messages)
                self.detect.boardcast.ID(id)
    
    #180
    def Turn(self):
        global MOVE_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(180) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("CCW")
        #收
        while True:
            try:
                messages = MOVE_SERIAL.readline().decode('utf-8')
            except:            
                continue             
            if self.read.messages_config(messages):
                continue
            #DONE
            if messages[0] == '@':
                break

    def STOP(self):
        global MOVE_SERIAL
        arr = "@|5|" + str(0) + "|" + str(0) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode("ascii"))
        print("STOP")


move = MOVE()
# move.GO()

#跑图动作组
MOVE_DICT = [
            move.GO, 
            move.CW, 
            move.GO,
            move.CCW,
            move.Distance(100),
            move.CCW,
            move.GO,
            move.CW,
            move.Distance(100),
            move.CW,
            move.GO,
            move.CCW,
            move.Distance(100),
            move.CCW,
            move.GO,
            move.CW,
            move.GO,
            move.CW,
            move.GO,
            move.CW,
            move.GO,
            move.CW,
            move.Distance(100),
            move.CW,
            move.GO,
            move.CCW,
            move.GO,
            move.CCW,
            move.Distance(200),
            move.CW,
            move.CW,
            move.GO,
            move.CW,
            move.Distance(100),
            move.CW,
            move.GO,
            move.CCW,
            move.Distance(50),
            move.CW,
            move.Distance(20),
]


          


