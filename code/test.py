import cv2


# messages = "$|5|"

# #找到第一个'|'
# index = messages.find('|')
# #找到第二个'|'
# index2 = messages.find('|',index+1)
# #拿到两个|之间的数据
# data = int(messages[index+1:index2])

# print(data)


#录像
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
