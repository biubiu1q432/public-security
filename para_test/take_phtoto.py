import cv2

cap = cv2.VideoCapture(0)
cnt = 0
#连续拍照
while True:
    
    
    # 读取摄像头画面
    ret, frame = cap.read()
    
    # 显示画面
#    frame_=cv2.resize(frame,(200,200))
    cv2.imshow("Take Photo", frame) 
    
    if cv2.waitKey(1) & 0xFF == ord(' '):
        cnt +=1
        # 保存图片
        cv2.imwrite("/home/king/public security/photo/"+str(cnt)+".jpg", frame)
        print("图片已保存到： /home/king/public security/photo/",str()+str(cnt)+".jpg")
     