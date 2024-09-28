import serial
import threading

# MY_SERIAL = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)


#GO
# arr = "@|1|" + str(10) + "|" + str(100) + "|" + str(75) + "#"
# car_port.write(arr.encode("ascii"))
# print(arr)





#READ
#ID: !_ _
#DONE: @ 
#HSV: #_ _ _

# class Read_Serial:

#     #读一行数据
#     def Read(self):
#         if MY_SERIAL.in_waiting > 0:    
#             message = MY_SERIAL.readline()
#             if message:



# message = "!12"
# if message[0] == '!':
#     ID_POINT = message[1:3]
#     print("ID: " + ID_POINT)

# HSV = [233,211,35]

# while True:
#     if MY_SERIAL.in_waiting > 0:
#                 message = MY_SERIAL.readline()                  
#                 #读到一行数据
#                 if message:
#                     #id卡号
#                     if message[0] == '!':
#                         point_id = message[1:3]
#                         print("ID: " + message[1:3])
#                         #播报
                    
#                     #色块
#                     elif message[0] == '#':
#                         #把message[2:5]放入一个矩阵
#                         hsv = message[2:5]
#                         #计算hsv和HSV的差距
#                         judge = HSV - hsv

                    

#                     #Done
#                     elif message[0] == '@':
#                         print("DONE")
#                         break

                    



#HSV: #_ _ _
#HSV test
message = "#13|2|113|"

H=10
S=23
L=36

if message:
    #HSV
    if message[0] == '#':
        #找到第一个'|'
        index = message.find('|')
        #找到第二个'|'
        index2 = message.find('|',index+1)
        #找到第三个'|'
        index3 = message.find('|',index2+1)
        #H
        h = int(message[1:index])
        #把index2和index2+1之间的字符串赋值给S
        s = int(message[index+1:index2])
        #把index2+3和index2+5之间的字符串赋值给L
        l = int(message[index2+1:index3])
        print(h,s,l)
        
        #计算hsv和HSV的差距
        judge = [abs(H-h),abs(S-s),abs(L-l)]
        judge = sum(judge)
        print(judge)
    
        

