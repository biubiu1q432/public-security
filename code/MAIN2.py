
import cv2
import serial
import Serial
import Detect
import time
import threading

#全局变量
MOVE_SERIAL = serial.Serial(port="/dev/tty_move",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)

#运动
class MOVE:
    
    def __init__(self):
        self.detect = Detect.Detect()
        self.read = Serial.Read_Serial()

        self.readflag = 0

        self.rfid = 0
        self.lastrfid = -1

        #微调距离
        self.adjust = 45
        #微调角度
        self.adjust_angle = 17

        #全图速度
        self.val = 25

    #侦察：1 不侦察：0
    def GO(self,val,mode,show = -1):
        global MOVE_SERIAL
        
        if mode == 1:
            num = 1
        elif mode == 0:
            num = 11
        #发
        arr = "@|"+str(num)+"|" + str(val) + "|" + str(60) + "|" + str(55) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("GO")
        
        #显示
        if show != -1:#默认值
            self.detect.brocast.Show_worlds(show)

        #收
        while True:       
                       
            #底盘
            # if MOVE_SERIAL.in_waiting > 0:
                # data = MOVE_SERIAL.readline().decode('utf-8')
                # print("move：",data)
                
                #DONE
                # if data[0] == '@':
                if self.readflag == 1:
                    self.readflag= 0
                    print("DONE")
                    # time.sleep(0.5)
                    break
                
                #侦察任务
                # if data[0] == '$':
                if self.readflag == 2:
                    self.readflag= 0
                    print("侦察任务")
                    #等待底盘走到正中心-》阻塞等待接收@
                    self.Wait_Center()
                    self.CCW()
                    #对正
                    self.Mini_Adjust(self.adjust)

                    #正式识别
                    ret,judge_center = self.detect.judge_center()                        
                    turn_flag = 0

                    #YES
                    if ret:    
                        
                        #微调
                        if judge_center == 2:#左转一点
                            self.Turn(-self.adjust_angle)
                            turn_flag = -1
                        elif judge_center == 3:#右转一点
                            self.Turn(self.adjust_angle) 
                            turn_flag = 1
                        
                        #一次识别
                        ret,result=self.detect.Detect()
                        
                        #NO 二次判定白板，防止judge_center出错     
                        if ret:    
                            print("judge_center出错")
                            
                            #微调归位
                            if turn_flag == -1:
                                self.Turn(self.adjust_angle)
                            elif turn_flag == 1:
                                self.Turn(-self.adjust_angle) 
                            turn_flag = 0

                            #另一头
                            self.Turn(180)      
                            #再来
                            ret,judge_center = self.detect.judge_center()
                            #微调
                            if judge_center == 2:#右转一点
                                self.Turn(-self.adjust_angle)
                                turn_flag = -1
                            elif judge_center == 3:#左转一点
                                self.Turn(self.adjust_angle) 
                                turn_flag = 1
                            elif judge_center == 1:#正中
                                turn_flag = 0
                            
                            #识别
                            ret,result=self.detect.Detect()
                            
                            #整体归位
                            if turn_flag == -1:
                                self.Turn(self.adjust_angle)
                                self.CCW()
                                self.GO(self.val,1,result)                            
                                return
                            elif turn_flag == 1:
                                self.Turn(-self.adjust_angle)
                                self.CCW()
                                self.GO(self.val,1,result)                            
                                return
                            elif turn_flag == 0:
                                self.CCW()
                                self.GO(self.val,1,result)                            
                                return

                        #YES
                        else:
                            print("猜对")
                            #整体归位        
                            if turn_flag == -1:
                                self.Turn(abs(90+self.adjust_angle))
                                self.GO(self.val,1,result)                            
                                return
                            elif turn_flag == 1:
                                self.Turn(abs(90-self.adjust_angle))
                                self.GO(self.val,1,result)                            
                                return
                            elif turn_flag == 0:
                                self.CW()
                                self.GO(self.val,1,result)                            
                                return
                    #NO
                    else:
                        print("猜错了")
                        self.Turn(180)      
                        ret,judge_center = self.detect.judge_center()
                        turn_flag = 0
                        #微调
                        if judge_center == 2:#左转一点
                            self.Turn(-self.adjust_angle)
                            turn_flag = -1
                        elif judge_center == 3:#右转一点
                            self.Turn(self.adjust_angle) 
                            turn_flag = 1
                        
                        #识别
                        ret,result=self.detect.Detect()
                        
                        #整体归位
                        if turn_flag == -1:
                            self.Turn(-abs(self.adjust_angle-90))
                            self.GO(self.val,1,result)                            
                            return
                        elif turn_flag == 1:
                            self.Turn(-abs(self.adjust_angle+90))
                            self.GO(self.val,1,result)                            
                            return
                        elif turn_flag == 0:
                            self.CCW()
                            self.GO(self.val,1,result)                            
                            return
            
    #侦察：1 不侦察：0(底盘错误)
    def Distance(self,val,dis,mode):
        global MOVE_SERIAL
        
        #发
        if mode == 1:
            num = 6
        elif mode == 0:
            num = 16
        arr = "@|"+str(num)+"|" + str(val) + "|" + str(dis) + "|" + str(55) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        # time.sleep(0.1)
        # MOVE_SERIAL.write(arr.encode('utf-8'))

        print("Distance")

        #收
        while True:             
        
            #底盘
            # if MOVE_SERIAL.in_waiting > 0:
                # data = MOVE_SERIAL.readline().decode('utf-8')
                # print("move:",data)
                
                #DONE
                # if data[0] == '@':
                if self.readflag == 1:
                    self.readflag= 0
                    time.sleep(0.5)
                    break
                            
                #侦察任务
                # if data[0] == '$':
                if self.readflag == 2:
                    self.readflag= 0
                    
                    print("侦察任务")
                    #等待底盘走到正中心-》阻塞等待接收@
                    self.Wait_Center()
                    self.CCW()
                    #对正
                    self.Mini_Adjust(self.adjust)

                    #正式识别
                    ret,judge_center = self.detect.judge_center()                        
                    turn_flag = 0

                    #YES
                    if ret:    
                        #微调
                        if judge_center == 2:#左转一点
                            self.Turn(-self.adjust_angle)
                            turn_flag = -1
                        elif judge_center == 3:#右转一点
                            self.Turn(self.adjust_angle) 
                            turn_flag = 1
                        
                        #一次识别
                        ret,result=self.detect.Detect()
                        
                        #NO 二次判定白板，防止judge_center出错     
                        if ret:    
                            print("judge_center出错")
                            
                            #微调归位
                            if turn_flag == -1:
                                self.Turn(self.adjust_angle)
                            elif turn_flag == 1:
                                self.Turn(-self.adjust_angle) 
                            turn_flag=0
                            #另一头
                            self.Turn(180)      
                            #再来
                            ret,judge_center = self.detect.judge_center()
                            #微调
                            if judge_center == 2:#右转一点
                                self.Turn(-self.adjust_angle)
                                turn_flag = -1
                            elif judge_center == 3:#左转一点
                                self.Turn(self.adjust_angle) 
                                turn_flag = 1
                            elif judge_center == 1:#正中
                                turn_flag = 0
                            
                            #识别
                            ret,result=self.detect.Detect()
                            
                            #整体归位
                            if turn_flag == -1:
                                self.Turn(self.adjust_angle)
                                self.CCW()
                                self.go_Cross(result)                            
                                return
                            elif turn_flag == 1:
                                self.Turn(-self.adjust_angle)
                                self.CCW()
                                self.go_Cross(result)                            
                                return
                            elif turn_flag == 0:
                                self.CCW()
                                self.go_Cross(result)                            
                                return

                        #YES
                        else:
                            print("猜对")
                            #整体归位        
                            if turn_flag == -1:
                                self.Turn(abs(90+self.adjust_angle))
                                self.go_Cross(result)                            
                                return
                            elif turn_flag == 1:
                                self.Turn(abs(90-self.adjust_angle))
                                self.go_Cross(result)                            
                                return
                            elif turn_flag == 0:
                                self.CW()
                                self.go_Cross(result)                            
                                return
                    #NO
                    else:
                        print("猜错了")
                        self.Turn(180)      
                        ret,judge_center = self.detect.judge_center()
                        turn_flag = 0
                        #微调
                        if judge_center == 2:#左转一点
                            self.Turn(-self.adjust_angle)
                            turn_flag = -1
                        elif judge_center == 3:#右转一点
                            self.Turn(self.adjust_angle) 
                            turn_flag = 1
                        
                        #识别
                        ret,result=self.detect.Detect()
                        
                        #整体归位
                        if turn_flag == -1:
                            self.Turn(-abs(self.adjust_angle-90))
                            self.go_Cross(result)                            
                            return
                        elif turn_flag == 1:
                            self.Turn(-abs(self.adjust_angle+90))
                            self.go_Cross(result)                            
                            return
                        elif turn_flag == 0:
                            self.CCW()
                            self.go_Cross(result)                            
                            return
                 
    #顺时针
    def CW(self):
        global MOVE_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(90) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("CW")
             
        flag =  0
        start_time = time.time()
    
        #收
        while True:

            # 结束计时
            end_time = time.time()
            #print(f"CW执行时间：{end_time - start_time}秒")

            if (end_time-start_time)>= 20 and flag == 0 :
                print("err")
                flag = 1
                self.STOP()
                self.CW()   

            # messages = MOVE_SERIAL.readline().decode('utf-8')
            # print(messages)
            

            #DONE
            # if messages[0] == '@':
            if self.readflag == 1:
                self.readflag= 0
                # time.sleep(0.5)
                break
    
    #逆时针
    def CCW(self):
        global MOVE_SERIAL
        #发
        arr = "@|2|" + str(1) + "|" + str(-90) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("CCW")
        flag =  0
        start_time = time.time()
    
        #收
        while True:

            # 结束计时
            end_time = time.time()
            #print(f"CCW执行时间：{end_time - start_time}秒")

            if (end_time-start_time)>= 20 and flag == 0 :
                print("err")
                flag = 1
                self.STOP()
                self.CW()            
            
            
            # messages = MOVE_SERIAL.readline().decode('utf-8')
            # print(messages)
   
            #DONE
            # if messages[0] == '@':
            if self.readflag == 1:
                self.readflag= 0
                # time.sleep(0.5)
                break
    
            # #ID  
            # if messages[0] == '!' and flag_id == True:
            #     flag_id = False
            #     id=self.read.read_ID(messages)
            #     self.detect.boardcast.ID(id)
    
    #指定角度
    def Turn(self,seta):
        global MOVE_SERIAL

        #发
        arr = "@|2|" + str(1) + "|" + str(seta) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("Turn:",seta)
        
        flag =  0
        start_time = time.time()
    
        #收
        while True:

            # 结束计时
            end_time = time.time()
            #print(f"TURN执行时间：{end_time - start_time}秒")

            if (end_time-start_time)>= 20 and flag == 0 :
                print("err")
                flag = 1
                self.STOP()
                self.Turn(seta)   

            # messages = MOVE_SERIAL.readline().decode('utf-8')
            # print(messages)

            #DONE
            # if messages[0] == '@':
            if self.readflag == 1:
                self.readflag= 0
                # time.sleep(0.5)
                break

    #微调，调整中心
    def Mini_Adjust(self,dis):
        global MOVE_SERIAL
        
        print("开始对正")
        #发
        arr = "@|11|" + str(15) + "|" + str(dis) + "|" + str(55) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8')) 

        #收
        while True:
            # messages = MOVE_SERIAL.readline().decode('utf-8')
            # print(messages)
          
            #DONE
            # if messages[0] == '@':
            if self.readflag == 1:
                self.readflag= 0
                # time.sleep(0.5)
                break
    
    #阻塞，等待底盘走到中心
    def Wait_Center(self):
        global MOVE_SERIAL
        while True:
            # messages = MOVE_SERIAL.readline().decode('utf-8')
            # print(messages)
            #DONE
            # if messages[0] == '@':
            if self.readflag == 1:
                self.readflag= 0
                print("已经走到正中心")
                # time.sleep(0.5)
                break

    #急停
    def STOP(self):
        global MOVE_SERIAL
        arr = "@|5|" + str(0) + "|" + str(0) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode("ascii"))
        print("STOP")
                #收
        while True:
            # messages = MOVE_SERIAL.readline().decode('utf-8')
            # print(messages)

            #DONE
            # if messages[0] == '@':
            if self.readflag == 1:
                self.readflag= 0
                # time.sleep(0.5)
                break
    
    #侦察任务后的十字路口
    def go_Cross(self,show = -1):
        global MOVE_SERIAL
        
        #发
        arr = "@|7|" + str(20) + "|" + str(90) + "|" + str(55) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("go_Cross")
        
        #显示
        if show != -1:#默认值
            self.detect.brocast.Show_worlds(show)

        #收
        while True:

            # messages = MOVE_SERIAL.readline().decode('utf-8')
            # print(messages)            
            #DONE
            # if messages[0] == '@':
            if self.readflag == 1:
                self.readflag= 0
                # time.sleep(0.5)
                break
    
    #修正
    def mpu_adjust(self):
        
        global MOVE_SERIAL
        #发
        arr = "@|3|" + str(0) + "|" + str(0) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("mpu_adjust")
    
        #收
        while True:

            # messages = MOVE_SERIAL.readline().decode('utf-8')
            # print(messages)
   
            #DONE
            # if messages[0] == '@':
            if self.readflag == 1:
                self.readflag= 0
                # time.sleep(0.5)
                break
    
    def run_thread(self):
        car_receive_thread = threading.Thread(target=self.Car_Receiver, daemon=True)
        car_anouncer_thread = threading.Thread(target=self.anouncer, daemon=True)
        car_anouncer_thread.start()
        car_receive_thread.start()

    def anouncer(self):
        while True:
            if self.rfid != self.lastrfid and self.rfid > 0:
                self.lastrfid = self.rfid
                self.detect.brocast.ID(self.rfid)
            time.sleep(0.01)

    def Receiver(self):
        global MOVE_SERIAL
        try:
            if MOVE_SERIAL.in_waiting > 0:
                message = MOVE_SERIAL.readline().decode("UTF-8")
                print("move:",message)
                if message:
                    # if message[0] == '@':
                    if "@" in message:
                        self.readflag = 1
                    # if message[0] == '$':
                    if "$" in message:
                        self.readflag = 2
                    if "!" in message:
                        index = message.find('|')
                        #找到第二个'|'
                        index2 = message.find('|',index+1)
                        #拿到两个|之间的数据
                        self.rfid = int(message[index+1:index2])
                        print("self.rfid:",self.rfid)


        except:
            pass

    def Car_Receiver(self):
        while True:
            self.Receiver()



move = MOVE()

#等待下位机信号
while True:
    messages = MOVE_SERIAL.readline().decode('utf-8')
    print(messages)
    if messages[0] == '^':
        print("已经收到下位机信号")
        time.sleep(0.5)
        break

move.run_thread()






#跑图动作组
MOVE_DICT = [
                move.GO(25,0),              ############不检测#############
                move.CW(), 
                move.GO(25,0),              ############不检测#############

                # move.detect.brocast.ID(1),
                move.CCW(),
                move.Distance(move.val,100,1),
                move.CCW(),
                move.GO(move.val,1),
                # move.detect.brocast.ID(11),
                move.CW(),
                move.Distance(move.val,100,1),
                # move.detect.brocast.ID(10),
                move.CW(),
                move.GO(move.val,1),
                # move.detect.brocast.ID(3),
                move.CCW(),
                move.Distance(move.val,100,1),
                # move.detect.brocast.ID(4),
                move.CCW(),
                move.GO(move.val,1),
                # move.detect.brocast.ID(9),
                move.CW(),
                move.GO(move.val,1),
                # move.detect.brocast.ID(8),

                move.Turn(-2),                    ############手动补偿################
               
                move.CW(),
                move.GO(move.val,1),

                move.Turn(-3),                    ############手动补偿################

                # move.detect.brocast.ID(5),
                move.CW(),

                move.Distance(move.val,100,1),    ############重复，不检测#############
                move.Distance(move.val,100,0),
                move.Distance(move.val,100,1),    ############重复，不检测#############

                # move.detect.brocast.ID(2),
                move.CW(),
                move.Distance(move.val,100,1),
                move.CW(),
                move.GO(move.val,1),
                # move.detect.brocast.ID(6),
                move.CCW(),
                move.GO(move.val,0),              ############重复，不检测#############
                move.CCW(),
                move.Distance(move.val,100,0),    ############重复，不检测#############
                move.Distance(move.val,100,1),
                move.Turn(180),
                move.GO(move.val,0),              ############重复，不检测#############
                move.CW(),
                move.Distance(move.val,100,0),   ############重复，不检测#############
                # move.detect.brocast.ID(7),
                move.CW(),
                move.GO(move.val,1),
                # move.detect.brocast.ID(12),
                move.CCW(),
                move.Distance(move.val,54,0),      ############不检测#############
                move.CW(),
                move.Distance(move.val,20,0),     ############不检测#############
]

