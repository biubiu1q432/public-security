'''

1.用于测试串口封装
2.实现把消息解析为（颜色COLOR_FLAG，运动状态MOVE_FLAG，点号POINT_ID）

'''

import serial

#全局变量
MY_SERIAL = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)

#串口（下位机）
class Read_Serial:
    #构造函数
    def __init__(self):
        
        self.H_floor = 79
        self.S_floor = 54
        self.L_floor = 30
        
        self.H_color1= 66
        self.S_color1= 87
        self.L_color1= 29
        
        self.H_color2= 418
        self.S_color2= 429
        self.L_color2= 193
        
    #消息认证
    def messages_config(self,messages):
        if messages[0] != '@' and messages[0] != '#' and  messages[0] != '!':
            return True
        else:
            return False

    #读HSL:#@|1|20|60|
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
        # print(h,s,l)
        
        #计算hsv和HSV的差距
        judge_err_f = [abs(self.H_floor-h),abs(self.S_floor-s),abs(self.L_floor-l)]
        judge_err_f = sum(judge_err_f)

        judge_err_c1 = [abs(self.H_color1-h),abs(self.S_color1-s),abs(self.L_color1-l)]
        judge_err_c1 = sum(judge_err_c1)

        judge_err_c2 = [abs(self.H_color2-h),abs(self.S_color2-s),abs(self.L_color2-l)]
        judge_err_c2 = sum(judge_err_c2)        
        
        judge_err = min(judge_err_f,judge_err_c1,judge_err_c2)

        
        print("地板 "+str(judge_err_f))
        print("颜色1 "+str(judge_err_c1))
        print("颜色2 "+str(judge_err_c2))


        #急停判定
        if judge_err == judge_err_f:
            return False
        else:
            return True

    #HSL参数自界定
    def HSL_test(self,num):
        read = Read_Serial()
        h_list= []
        s_list = []
        l_list = []
        
        if num == 1:        
            arr = "@|1|" + str(20) + "|" + str(60) + "|" + str(75) + "#"
            MY_SERIAL.write(arr.encode('utf-8'))
            print("GO")
            
            for i in range(50):
                try:
                    messages = MY_SERIAL.readline().decode('utf-8')
                except:
                    continue
                if messages[0] != '#' or self.messages_config(messages):
                    continue 
                
                index = messages.find('|')
                index2 = messages.find('|',index+1)
                index3 = messages.find('|',index2+1)
                h = int(messages[1:index])
                s = int(messages[index+1:index2])
                l = int(messages[index2+1:index3])   
                print(h,s,l)

                h_list.append(h)
                s_list.append(s)
                l_list.append(l)
        
            print("颜色： "+str(int(sum(h_list)/len(h_list))),str(int(sum(s_list)/len(s_list))),str(int(sum(l_list)/len(l_list))))
                           
        elif num == 2:                    
            for i in range(50):
                try:
                    messages = MY_SERIAL.readline().decode('utf-8')
                except:
                    continue                
                if read.messages_config(messages):
                    continue 
                index = messages.find('|')
                index2 = messages.find('|',index+1)
                index3 = messages.find('|',index2+1)
                h = int(messages[1:index])
                s = int(messages[index+1:index2])
                l = int(messages[index2+1:index3])   

                h_list.append(h)
                s_list.append(s)
                l_list.append(l)
                print(h,s,l)
        
            print("颜色： "+str(int(sum(h_list)/len(h_list))),str(int(sum(s_list)/len(s_list))),str(int(sum(l_list)/len(l_list))))
        
        elif num == 3:
            #计算允许误差
            err1 = int(abs(self.H_color1 - self.H_floor) + abs(self.S_color1 - self.S_floor) + abs(self.L_color1 - self.L_floor))#颜色1
            err2 = int(abs(self.H_color2 - self.H_floor) + abs(self.S_color2 - self.S_floor) + abs(self.L_color2 - self.L_floor))#颜色2
            #小的一项赋值
            print(str(min(err1,err2)))
                    
    #ID:$|12|
    def read_ID(self,messages):
        #找到第一个'|'
        index = messages.find('|')
        #找到第二个'|'
        index2 = messages.find('|',index+1)
        #拿到两个|之间的数据
        id = int(messages[index+1:index2])
        return id

    #DIS:&|20|
    def read_DIS(self,messages):
        #找到第一个'|'
        index1 = messages.find('|')
        #找到第二个'|'
        index2 = messages.find('|',index1+1)

        #拿到两个|之间的数据
        dis = int(messages[index1+1:index2])
        return dis

# read_serial =  Read_Serial()
# read_serial.HSL_test(2)


# while True:
#     messages = MY_SERIAL.readline().decode('utf-8')
#     print(messages)




