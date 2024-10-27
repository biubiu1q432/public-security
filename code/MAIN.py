
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
        self.err = -1
        self.targrt_Stop = 125
        self.threold = 7

        #微调距离
        self.adjust = 45
        #微调角度
        self.adjust_angle = 17

    #mode1:k2l0,done mode0:done
    def GO(self,val,mode):
        global MOVE_SERIAL,K2L0_SERIAL
        #发
        arr = "@|1|" + str(val) + "|" + str(60) + "|" + str(55) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("GO")
        MOVE_SERIAL.flushInput()
        K2L0_SERIAL.flushInput()
        
        #收
        while True:       
            
            #底盘
            if MOVE_SERIAL.in_waiting > 0:
                data = MOVE_SERIAL.readline().decode('utf-8')
                
                #DONE
                if data[0] == '@':
                    print("DONE")
                    break

                #侦察任务
                if data == '$':
                    
                    #等待底盘走到正中心-》@
                    self.Wait_Center()
                    self.CCW()
                    
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
                        
                        #NO 二次判定白板，防止judge_center出错
                        if self.detect.Detect():    
                            print("judge_center出错")
                            
                            #微调归位
                            if turn_flag == -1:
                                self.Turn(self.adjust_angle)
                            elif turn_flag == 1:
                                self.Turn(-self.adjust_angle) 
                            
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
                            
                            #识别
                            self.detect.Detect()
                            
                            #整体归位
                            if turn_flag == -1:
                                self.Turn(abs(self.adjust_angle-90))
                                self.GO(20,1)
                                return
                            elif turn_flag == 1:
                                self.Turn(abs(self.adjust_angle+90))
                                self.GO(20,1)
                                return
                            elif turn_flag == 0:
                                self.CCW()
                                self.GO(20,1)
                                return

                        #YES
                        else:
                            print("猜对")
                            #整体归位        
                            if turn_flag == -1:
                                self.Turn(abs(90+self.adjust_angle))
                                self.GO(20,1)
                                return
                            elif turn_flag == 1:
                                self.Turn(abs(90-self.adjust_angle))
                                self.GO(20,1)
                                return
                            elif turn_flag == 0:
                                self.CW()
                                self.GO(20,1)
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
                        self.detect.Detect()
                        
                        #整体归位
                        if turn_flag == -1:
                            self.Turn(-abs(self.adjust_angle-90))
                            self.GO(20,1)
                            return
                        elif turn_flag == 1:
                            self.Turn(-abs(self.adjust_angle+90))
                            self.GO(20,1)
                            return
                        elif turn_flag == 0:
                            self.CCW()
                            self.GO(20,1)
                            return
               
    #mode1:k2l0,done,dis mode0:done 
    def Distance(self,val,dis,mode):
        global MOVE_SERIAL,K2L0_SERIAL
        #发
        arr = "@|6|" + str(val) + "|" + str(dis) + "|" + str(55) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("Distance")
        
        # int(dis)
        # rest_dis=0
        
        MOVE_SERIAL.flushInput()
        K2L0_SERIAL.flushInput()

        #收
        while True:             
        
            #底盘
            if MOVE_SERIAL.in_waiting > 0:
                data = MOVE_SERIAL.readline().decode('utf-8')
                # print("move:",data)
                
                #DONE
                if data[0] == '@':
                    break
                
                # #dis
                # if data[0] == '$'and mode == 1:
                #     now_dis=self.read.read_DIS(data)
                #     int(now_dis)
                #     rest_dis_ = (dis - now_dis)
                #     int(rest_dis_)
            
            #K210            
            if K2L0_SERIAL.in_waiting > 0 and mode == 1:
                k2l0 = int(K2L0_SERIAL.readline().decode('utf-8'))
                print(k2l0)
                if  k2l0 >= self.targrt_Stop :
                        
                        self.STOP()                        

                        #补偿距离
                        ahead = self.fliter(self.threold)
                        ahead += 1.11
                        print("准备走：",ahead)
                        
                        # rest_dis = rest_dis_ - ahead - self.err  #剩余距离
                        # print("剩余距离:",rest_dis)
                        
                        self.Distance(15,ahead,0)
                        self.CCW()
                        self.Mini_Adjust(self.adjust)
                        
                        #正式识别
                        ret,judge_center = self.detect.judge_center()
                        #YES
                        if ret:    
                            turn_flag = 0
                            
                            #微调
                            if judge_center == 2:#左转一点
                                self.Turn(-self.adjust_angle)
                                turn_flag = -1
                            elif judge_center == 3:#右转一点
                                self.Turn(self.adjust_angle) 
                                turn_flag = 1
                            
                            #NO 二次判定白板，防止judge_center出错
                            if self.detect.Detect():    
                                print("judge_center出错")
                                
                                #微调归位
                                if turn_flag == -1:
                                    self.Turn(self.adjust_angle)
                                elif turn_flag == 1:
                                    self.Turn(-self.adjust_angle) 
                                
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
                                
                                #识别
                                self.detect.Detect()
                                
                                #整体归位
                                if turn_flag == -1:
                                    self.Turn(abs(self.adjust_angle-90))
                                    self.go_Cross(20)
                                    return
                                elif turn_flag == 1:
                                    self.Turn(abs(self.adjust_angle+90))
                                    self.go_Cross(20)
                                    return
                                elif turn_flag == 0:
                                    self.CCW()
                                    self.go_Cross(20)
                                    return

                            #YES
                            else:
                                print("猜对")
                                #整体归位        
                                if turn_flag == -1:
                                    self.Turn(abs(90+self.adjust_angle))
                                    self.go_Cross(20)
                                    return
                                elif turn_flag == 1:
                                    self.Turn(abs(90-self.adjust_angle))
                                    self.go_Cross(20)
                                    return
                                elif turn_flag == 0:
                                    self.CW()
                                    self.go_Cross(20)
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
                            self.detect.Detect()
                            
                            #整体归位
                            if turn_flag == -1:
                                self.Turn(-abs(self.adjust_angle-90))
                                self.go_Cross(20)
                                return
                            elif turn_flag == 1:
                                self.Turn(-abs(self.adjust_angle+90))
                                self.go_Cross(20)
                                return
                            elif turn_flag == 0:
                                self.CCW()
                                self.go_Cross(20)
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
            messages = MOVE_SERIAL.readline().decode('utf-8')
            print(messages)

            #DONE
            if messages[0] == '@':
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
        
        MOVE_SERIAL.flushInput()

        #收
        while True:
            messages = MOVE_SERIAL.readline().decode('utf-8')
            print(messages)

            #DONE
            if messages[0] == '@':
                break

    #微调，调整中心
    def Mini_Adjust(self,dis):
        global MOVE_SERIAL
        #发
        arr = "@|1|" + str(15) + "|" + str(dis) + "|" + str(55) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8')) 

        #收
        while True:
            messages = MOVE_SERIAL.readline().decode('utf-8')
            print(messages)
          
            #DONE
            if messages[0] == '@':
                break
    
    #急停
    def STOP(self):
        global MOVE_SERIAL
        arr = "@|5|" + str(0) + "|" + str(0) + "|" + str(0) + "#"
        MOVE_SERIAL.write(arr.encode("ascii"))
        print("STOP")
                #收
        while True:
            messages = MOVE_SERIAL.readline().decode('utf-8')
            print(messages)

            #DONE
            if messages[0] == '@':
                break
    
    #侦察任务后的十字路口
    def go_Cross(self,val):
        global MOVE_SERIAL
        #发
        arr = "@|7|" + str(val) + "|" + str(90) + "|" + str(55) + "#"
        MOVE_SERIAL.write(arr.encode('utf-8'))
        print("go_Cross")
        
        MOVE_SERIAL.flushInput()
   
        #收
        while True:
            messages = MOVE_SERIAL.readline().decode('utf-8')
            print(messages)            
            #DONE
            if messages[0] == '@':
                break
    
    #阻塞，等待底盘走到中心
    def Wait_Center(self):
        global MOVE_SERIAL
        while True:
            messages = MOVE_SERIAL.readline().decode('utf-8')
            print(messages)
            #DONE
            if messages[0] == '@':
                break
    
    #滤波
    def fliter(self,threold):
        sum = 0
        buff = [0,0,0,0,0]
        
        for i in range(1,100):
            data = int(K2L0_SERIAL.readline().decode('utf-8'))

            if i >=5:            #数据已稳定    
                if(abs(data - sum) <= threold):
                    best_data =data
                    dis = best_data*(-0.102) + 33.9
                    return dis
            
            for j in range(0,4):
                buff[j] = buff[j + 1]
            
            buff[4] = data

            print(buff)
            sum = (buff[0] + buff[1] + buff[2] + buff[3] + buff[4])/5

    
move = MOVE()


# move.Distance(20,100,1)


#跑图动作组
MOVE_DICT = [
            move.GO(20,1), 
            move.CW(), 
            move.GO(20,1),
            move.detect.brocast.ID(1),
            move.CCW(),
            move.Distance(20,100,1),
            move.CCW(),
            move.GO(20,1),
            move.detect.brocast.ID(11),
            move.CW(),
            move.Distance(20,100,1),
            move.detect.brocast.ID(10),
            move.CW(),
            move.GO(20,1),
            move.detect.brocast.ID(3),
            move.CCW(),
            move.Distance(20,100,1),
            move.detect.brocast.ID(4),
            move.CCW(),
            move.GO(20,1),
            move.detect.brocast.ID(9),
            move.CW(),
            move.GO(20,1),
            move.detect.brocast.ID(8),
            move.CW(),
            move.GO(20,1),
            move.detect.brocast.ID(5),
            move.CW(),
            move.GO(20,1),
            move.detect.brocast.ID(2),
            move.CW(),
            move.Distance(20,100,1),
            move.CW(),
            move.GO(20,1),
            move.detect.brocast.ID(6),
            move.CCW(),
            move.GO(20,0),
            move.CCW(),
            move.Distance(20,200,0),
            move.Turn(180),
            move.GO(20,0),
            move.CW(),
            move.Distance(20,100,0),
            move.detect.brocast.ID(7),
            move.CW(),
            move.GO(20,1),
            move.detect.brocast.ID(12),
            move.CCW(),
            move.Distance(20,50,0),
            move.CW(),
            move.Distance(20,20,0),
]
