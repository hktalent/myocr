szFileNmae = "/Users/51pwn/MyWork/mybugbounty/ai/i1.jpg"

from matplotlib import pyplot as plt
import cv2
import numpy as np


def show_img(name, img):
    plt.subplot(1,1,1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(name, fontdict={'fontsize':16, 'color':'b'})
    plt.show()


img = cv2.imread(szFileNmae)
img_h, img_w, _ = img.shape

# 这里调整，颜色范围局域的单个
lower = (10, 0, 0)
upper = (200, 255, 255)

blurred = cv2.GaussianBlur(img, (5, 5), 0)

hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

# inRange的作用是根据阈值进行二值化:阈值内的像素设置为白色(255)，阈值外的设置为黑色(0)
mask = cv2.inRange(hsv, lower, upper)

mask = cv2.erode(mask, None, iterations=2)

mask = cv2.dilate(mask, None, iterations=2)

contours, _hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

max_i = 0
for i,cnt in enumerate(contours):
    if cv2.contourArea(cnt) > cv2.contourArea(contours[max_i]):
        max_i = i

peri = cv2.arcLength(contours[max_i], True)
approx = cv2.approxPolyDP(contours[max_i], 0.02 * peri, True)

# cv2.drawContours(img,[contours[max_i]],0,(255,0,0),10)

# 这四个点为原始图片上数独的位置
pts_o = np.float32([approx[0][0], approx[1][0],  approx[2][0], approx[3][0]])
# 这是变换之后的图上四个点的位置
pts_d = np.float32([[img_w, 0], [0, 0], [0, img_h], [img_w, img_h]])

M = cv2.getPerspectiveTransform(pts_o, pts_d)

dst = cv2.warpPerspective(img, M, (img_w, img_h)) 
    
# show_img("src", img)
show_img("dst", dst)