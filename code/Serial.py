'''

1.用于测试串口封装
2.实现把消息解析为（颜色COLOR_FLAG，运动状态MOVE_FLAG，点号POINT_ID）

'''

import serial

#全局变量
MOVE_DICT = None
MOVE_FLAG = None  # 空闲/未完成：0   完成：1
POINT_ID = None # 点号
MY_SERIAL = serial.Serial("COM3", 9600)

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

    #DONE
    def read_MOVE(self,messages):
        pass

    #ID
    def read_ID(self,messages):
        pass

    
