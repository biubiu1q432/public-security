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
        
        self.H_floor = 33
        self.S_floor = 79
        self.L_floor= 32
        
        self.H_color1= 9
        self.S_color1= 89
        self.L_color1= 35
        
        self.H_color2= 28
        self.S_color2= 113
        self.L_color2= 32
        
        self.allow_err= 32

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
        
        if num == 2:
            for i in range(30):
                messages = MY_SERIAL.readline().decode('utf-8')
                if read.messages_config(messages):
                    continue 
                index = messages.find('|')
                index2 = messages.find('|',index+1)
                index3 = messages.find('|',index2+1)
                h = int(messages[1:index])
                s = int(messages[index+1:index2])
                l = int(messages[index2+1:index3])   
                print(h,s,l)

                h_list= []
                s_list = []
                l_list = []
                h_list.append(h)
                s_list.append(s)
                l_list.append(l)
        
            print("颜色2： "+str(int(sum(h_list)/len(h_list))),str(int(sum(s_list)/len(s_list))),str(int(sum(l_list)/len(l_list))))
        
        elif num == 1:
            
            for i in range(30):
                messages = MY_SERIAL.readline().decode('utf-8')
                if read.messages_config(messages):
                    continue 
                index = messages.find('|')
                index2 = messages.find('|',index+1)
                index3 = messages.find('|',index2+1)
                h = int(messages[1:index])
                s = int(messages[index+1:index2])
                l = int(messages[index2+1:index3])   
                print(h,s,l)

                h_list= []
                s_list = []
                l_list = []
                h_list.append(h)
                s_list.append(s)
                l_list.append(l)            
        
            print("颜色1： "+str(int(sum(h_list)/len(h_list))),str(int(sum(s_list)/len(s_list))),str(int(sum(l_list)/len(l_list)) ))
                 
        elif num == 4:
            #计算允许误差
            err1 = int(abs(self.H_color1 - self.H_floor) + abs(self.S_color1 - self.S_floor) + abs(self.L_color1 - self.L_floor))#颜色1
            err2 = int(abs(self.H_color2 - self.H_floor) + abs(self.S_color2 - self.S_floor) + abs(self.L_color2 - self.L_floor))#颜色2
            #小的一项赋值
            print(str(min(err1,err2)))
            
        elif num == 3: 
        
            arr = "@|1|" + str(25) + "|" + str(60) + "|" + str(75) + "#"
            MY_SERIAL.write(arr.encode('utf-8'))
            
            while True:

                messages = MY_SERIAL.readline().decode('utf-8')
                if read.messages_config(messages):
                    continue
                if messages[0] == '@':
                    break

                index = messages.find('|')
                index2 = messages.find('|',index+1)
                index3 = messages.find('|',index2+1)
                h = int(messages[1:index])
                s = int(messages[index+1:index2])
                l = int(messages[index2+1:index3])   
                print(h,s,l)

                h_list= []
                s_list = []
                l_list = []
                h_list.append(h)
                s_list.append(s)
                l_list.append(l)
            
            #赋值
            print("地板颜色："+str(int(sum(h_list)/len(h_list))),str(int(sum(s_list)/len(s_list))),str(int(sum(l_list)/len(l_list))))
         
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

    
