szFileNmae = "/Users/51pwn/MyWork/mybugbounty/ai/i1.jpg"

import numpy as np 
import cv2 
from matplotlib import pyplot as plt 
  
  
# read the image 
img = cv2.imread(szFileNmae) 
  
# convert image to gray scale image 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  
# detect corners with the goodFeaturesToTrack function. 
corners = cv2.goodFeaturesToTrack(gray, 27, 0.01, 10) 
corners = np.int0(corners) 
  
# we iterate through each corner,  
# making a circle at each point that we think is a corner. 
for i in corners: 
    x, y = i.ravel() 
    cv2.circle(img, (x, y), 3, 255, -1)

(h,w) = img.shape[:2]

pts1=np.float32([[0,0],[0,h],[w,0],[w,h]])
pts2=np.float32([(7.17803, 6.05628),(67.6975,198.332),(209.54, 50.1851),(231.604, 226.7)])

m = cv2.getPerspectiveTransform(pts2,pts1)
img = cv2.warpPerspective(img,m,(w,h))

cv2.imshow('Perspective', img)
plt.imshow(img), plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()


# from matplotlib import pyplot as plt
# import cv2
# import numpy as np


# def show_img(name, img):
#     plt.subplot(1,1,1)
#     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     plt.title(name, fontdict={'fontsize':16, 'color':'b'})
#     plt.show()


# img = cv2.imread(szFileNmae)
# img_h, img_w, _ = img.shape

# # 这里调整，颜色范围局域的单个
# lower = (10, 0, 0)
# upper = (200, 255, 255)

# blurred = cv2.GaussianBlur(img, (5, 5), 0)

# hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

# # inRange的作用是根据阈值进行二值化:阈值内的像素设置为白色(255)，阈值外的设置为黑色(0)
# mask = cv2.inRange(hsv, lower, upper)

# mask = cv2.erode(mask, None, iterations=2)

# mask = cv2.dilate(mask, None, iterations=2)

# contours, _hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# max_i = 0
# for i,cnt in enumerate(contours):
#     if cv2.contourArea(cnt) > cv2.contourArea(contours[max_i]):
#         max_i = i

# peri = cv2.arcLength(contours[max_i], True)
# approx = cv2.approxPolyDP(contours[max_i], 0.02 * peri, True)

# # cv2.drawContours(img,[contours[max_i]],0,(255,0,0),10)

# # 这四个点为原始图片上数独的位置
# pts_o = np.float32([approx[0][0], approx[1][0],  approx[2][0], approx[3][0]])
# # 这是变换之后的图上四个点的位置
# pts_d = np.float32([[img_w, 0], [0, 0], [0, img_h], [img_w, img_h]])

# M = cv2.getPerspectiveTransform(pts_o, pts_d)

# dst = cv2.warpPerspective(img, M, (img_w, img_h)) 
    
# # show_img("src", img)
# show_img("dst", dst)