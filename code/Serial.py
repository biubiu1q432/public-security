
import threading
import serial
import time

class Read_Serial:

    def __init__(self):
        self.targrt_Stop = 120
        self.allow_err = 7
    
    #消息认证
    def messages_config(self,messages):
        if messages[0] != '@' and messages[0] != '#' and  messages[0] != '!' and messages[0] != '$':
            return True
        else:
            return False
                   
    #ID:$|12|
    def read_ID(self,messages):
        #找到第一个'|'
        index = messages.find('|')
        #找到第二个'|'
        index2 = messages.find('|',index+1)
        #拿到两个|之间的数据
        id = int(messages[index+1:index2])
        return id

    #DIS:$|20|
    def read_DIS(self,messages):
        #找到第一个'|'
        index1 = messages.find('|')
        #找到第二个'|'
        index2 = messages.find('|',index1+1)

        #拿到两个|之间的数据
        dis = int(messages[index1+1:index2])
        return dis
    
    def read_k2l0(self,data):
        data = int(data)
        #急停判定
        if abs(data - self.targrt_Stop) <= self.allow_err :
            return True
        else:
            return False




# K2L0_SERIAL = serial.Serial(port="/dev/tty_k2l0",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)
# while  True:
#     data = K2L0_SERIAL.readline()
#     data = data.decode('utf-8')
#     print(data)