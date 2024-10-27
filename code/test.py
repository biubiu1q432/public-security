



import cv2

img = cv2.imread("/home/king/public security/code/1.png")
a = cv2.copyMakeBorder(img,20,20,20,20,cv2.BORDER_CONSTANT,value=[255,255,255])
cv2.imshow("a",a)

cv2.waitKey(0)
cv2.destroyAllWindows()


