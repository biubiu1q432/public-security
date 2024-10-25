import serial
import Serial
import Detect
import time

#全局变量
MOVE_SERIAL = serial.Serial(port="/dev/tty_move",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)
K2L0_SERIAL = serial.Serial(port="/dev/tty_k2l0",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)

#运动
class MOVE:
    
    def __init__(self):
        self.detect = Detect.Detect()
        self.read = Serial.Read_Serial()
        self.ahead = 13
        self.err = 26

    #mode1:k2l0,done mode0:done
    def GO(self,mode):
        global MOVE_SERIAL,K2L0_SERIAL
        #发
        arr = "@|1|" + str(20) + "|" + str(60) + "|" + str(75) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("GO")
        MOVE_SERIAL.flushInput()
        #收
        while True:
            
            #底盘
            if MOVE_SERIAL.in_waiting > 0:
                data = MOVE_SERIAL.readline().decode('utf-8')
                
                #DONE
                if data[0] == '@':
                    print("DONE")
                    break
                
            
            #k2l0
            if K2L0_SERIAL.in_waiting > 0 and mode == 1:
                k2l0 = K2L0_SERIAL.readline().decode('utf-8')
                print("k2l0:",k2l0)

                #k2l0
                if self.read.read_k2l0(k2l0):    
                    self.STOP()
                    time.sleep(2.5)
                    self.Distance(13,self.ahead,0)
                    self.CW()
                    #猜对
                    if self.detect.Detect():
                        print("猜对了")
                        self.CCW()
                        self.GO(0)#递归
                        return
                    #猜错
                    else:
                        self.Turn()
                        if self.detect.Detect():
                            print("确实有")
                            self.CW()
                            self.GO(0)#递归

                            return
                        else:         #hsl误判断
                            print("误判")
                            self.CW()
                            #读完串口缓冲区
                            K2L0_SERIAL.flushInput()
                            self.GO(1)#递归
                            return   
    
    #mode1:k2l0,done,dis mode0:done 
    def Distance(self,val,dis,mode):
        global MOVE_SERIAL,K2L0_SERIAL
        #发
        arr = "@|6|" + str(val) + "|" + str(dis) + "|" + str(61) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("Distance")
        
        int(dis)
        rest_dis=0
        MOVE_SERIAL.flushInput()

        #收
        while True:
            
            #底盘
            if MOVE_SERIAL.in_waiting > 0:
                data = MOVE_SERIAL.readline().decode('utf-8')
                print("move:",data)
                
                #DONE
                if data[0] == '@':
                    break
                
                #dis
                if data[0] == '$'and mode == 1:
                    now_dis=self.read.read_DIS(data)
                    int(now_dis)
                    rest_dis = (dis - now_dis - self.err)
                    int(rest_dis)
            
            #k2l0
            if K2L0_SERIAL.in_waiting > 0 and mode == 1:
                k2l0 = K2L0_SERIAL.readline().decode('utf-8')
                print("k2l0:",k2l0)

                #k2l0
                if self.read.read_k2l0(k2l0):    
                    self.STOP()
                    time.sleep(2.5)
                    self.Distance(13,self.ahead,0)
                    self.CW()
                    #猜对
                    if self.detect.Detect():
                        print("猜对了")
                        self.CCW()
                        print("准备走",rest_dis)
                        self.Distance(20,rest_dis,0)#递归
                        return
                    #猜错
                    else:
                        self.Turn()
                        if self.detect.Detect():
                            print("确实有")
                            self.CW()
                            print("准备走",rest_dis)
                            self.Distance(20,rest_dis,0)#递归

                            return
                        else:         #hsl误判断
                            print("误判")
                            self.CW()
                            #读完串口缓冲区
                            K2L0_SERIAL.flushInput()
                            print("准备走",rest_dis)
                            self.Distance(20,rest_dis,1)#递归
                            return   
    
    #顺时针
    def CW(self):
        global MOVE_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(90) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("CW")
        flag_id=True
        
        MOVE_SERIAL.flushInput()

        
        #收
        while True:
            try:
                messages = MOVE_SERIAL.readline().decode('utf-8')
                print(messages)
            except:            
                continue            
            if self.read.messages_config(messages):
                continue
            
            #DONE
            if messages[0] == '@':
                break
            # #ID
            # if messages[0] == '!' and flag_id == True:
            #     flag_id = False
            #     id=self.read.read_ID(messages)
            #     self.detect.boardcast.ID(id)
    
    #逆时针
    def CCW(self):
        global MOVE_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(-90) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("CCW")
        flag_id=True
        
        MOVE_SERIAL.flushInput()

        
        #收
        while True:
            try:
                messages = MOVE_SERIAL.readline().decode('utf-8')
                print(messages)
            except:            
                continue             
            if self.read.messages_config(messages):
                continue
            #DONE
            if messages[0] == '@':
                break
            # #ID  
            # if messages[0] == '!' and flag_id == True:
            #     flag_id = False
            #     id=self.read.read_ID(messages)
            #     self.detect.boardcast.ID(id)
    
    #180
    def Turn(self):
        global MOVE_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(180) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("Turn")
        
        MOVE_SERIAL.flushInput()

        
        #收
        while True:
            try:
                messages = MOVE_SERIAL.readline().decode('utf-8')
                print(messages)
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
# move.GO(1)


#跑图动作组
MOVE_DICT = [
            move.GO(1), 
            move.CW(), 
            move.GO(1),
            move.detect.brocast.ID(1),
            move.CCW(),
            move.Distance(20,100,1),
            move.CCW(),
            move.GO(1),
            move.detect.brocast.ID(11),
            move.CW(),
            move.Distance(20,100,1),
            move.detect.brocast.ID(10),
            move.CW(),
            move.GO(1),
            move.detect.brocast.ID(3),
            move.CCW(),
            move.Distance(20,100,1),
            move.detect.brocast.ID(4),
            move.CCW(),
            move.GO(1),
            move.detect.brocast.ID(9),
            move.CW(),
            move.GO(1),
            move.detect.brocast.ID(8),
            move.CW(),
            move.GO(1),
            move.detect.brocast.ID(5),
            move.CW(),
            move.GO(1),
            move.detect.brocast.ID(2),
            move.CW(),
            move.Distance(20,100,1),
            move.CW(),
            move.GO(1),
            move.detect.brocast.ID(6),
            move.CCW(),
            move.GO(1),
            move.CCW(),
            move.Distance(20,200,1),
            move.Turn(),
            move.GO(1),
            move.CW(),
            move.Distance(20,100,1),
            move.detect.brocast.ID(7),
            move.CW(),
            move.GO(1),
            move.detect.brocast.ID(12),
            move.CCW(),
            move.Distance(20,50,0),
            move.CW(),
            move.Distance(20,20,0),
]
