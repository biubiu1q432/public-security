'''

1.用于测试串口封装
2.实现把消息解析为（颜色COLOR_FLAG，运动状态MOVE_FLAG，点号POINT_ID）

'''

import serial

#全局变量
MOVE_DICT = None #移动字典
POINT_ID = None # 点号
MY_SERIAL = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)
COLOR_FLAG = None 

#串口（下位机）
class Read_Serial:
    #构造函数
    def __init__(self):
        
        self.H_floor = 31
        self.S_floor = 72
        self.L_floor= 33
        
        self.H_color1= 10
        self.S_color1= 85
        self.L_color1= 36
        
        self.H_color2= 28
        self.S_color2= 115
        self.L_color2= 33
        
        self.allow_err= 0

    #消息认证
    def messages_config(self,messages):
        if messages[0] != '@' and messages[0] != '#' and  messages[0] != '!':
            return True
        else:
            return False

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
        judge_err = [abs(self.H_floor-h),abs(self.S_floor-s),abs(self.L_floor-l)]
        judge_err = sum(judge_err)
        #print(judge_err)

    #HSL参数自界定
    def HSL_test(self,num):
        
        #读20次hsl分别取平均
        for i in range(20):

            messages = MY_SERIAL.readline().decode('utf-8')
            if read.messages_config(messages):
                continue
            index = messages.find('|')
            index2 = messages.find('|',index+1)
            index3 = messages.find('|',index2+1)
            h = int(messages[1:index])
            s = int(messages[index+1:index2])
            l = int(messages[index2+1:index3])   
            
            h_list= []
            s_list = []
            l_list = []

            h_list.append(h)
            s_list.append(s)
            l_list.append(l)
        
        #赋值
        if num == 1:
            self.H_color1 = int(sum(h_list)/len(h_list))
            self.S_color1 = int(sum(s_list)/len(s_list))
            self.L_color1 = int(sum(l_list)/len(l_list))        
            print("颜色1： "+str(self.H_color1),str(self.S_color1),str(self.L_color1))
        elif num == 2:
            self.H_color2 = int(sum(h_list)/len(h_list))
            self.S_color2 = int(sum(s_list)/len(s_list))
            self.L_color2 = int(sum(l_list)/len(l_list))
            print("颜色2： "+str(self.H_color2),str(self.S_color2),str(self.L_color2))
        elif num == 3:
            self.H_floor = int(sum(h_list)/len(h_list))
            self.S_floor = int(sum(s_list)/len(s_list))
            self.L_floor = int(sum(l_list)/len(l_list))
            print("地板颜色："+str(self.H_floor),str(self.S_floor),str(self.L_floor))
        
        if num == 4:
            #计算允许误差
            err1 = int(abs(self.H_color1 - self.H_floor) + abs(self.S_color1 - self.S_floor) + abs(self.L_color1 - self.L_floor))#颜色1
            err2 = int(abs(self.H_color2 - self.H_floor) + abs(self.S_color2 - self.S_floor) + abs(self.L_color2 - self.L_floor))#颜色2
            #大的一项赋值
            self.allow_err = max(err1,err2)
            print(str(self.allow_err))
      
    #ID
    def read_ID(self,messages):
        pass

    
read =Read_Serial()

read.HSL_test(4)


# while True:
#     messages = MY_SERIAL.readline().decode('utf-8')
#     if read.messages_config(messages):
#         continue
#     read.read_HSL(messages)

    
