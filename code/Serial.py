

class Read_Serial:

    #消息认证
    def messages_config(self,messages):
        if messages[0] != '@' and messages[0] != '#' and  messages[0] != '!':
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

    #DIS:&|20|
    def read_DIS(self,messages):
        #找到第一个'|'
        index1 = messages.find('|')
        #找到第二个'|'
        index2 = messages.find('|',index1+1)

        #拿到两个|之间的数据
        dis = int(messages[index1+1:index2])
        return dis


# while True:
#     messages = MY_SERIAL.readline().decode('utf-8')
#     print(messages)




