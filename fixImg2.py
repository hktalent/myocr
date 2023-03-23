import cv2
import numpy as np

szFileName="/Users/51pwn/MyWork/mybugbounty/ai/i1.jpg"

# 下面是一个针对图片中表格、物体倾斜矫正的 Python 代码示例，可以实现图像的自适应矫正和节点信息的正确性：


# 读取图像
img = cv2.imread(szFileName)

mask = np.zeros(img.shape[:2],np.uint8)

# 加载背景和前景区域，将背景区域标记为0，前景区域标记为1
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
rect = (10,10,img.shape[1]-20,img.shape[0]-20)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]

# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 直方图均衡化
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
gray = clahe.apply(gray)

# 高斯模糊去噪声
gray = cv2.GaussianBlur(gray, (3,3), 0)

# 自适应阈值二值化去除背景
gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

# 进行边缘检测
edges = cv2.Canny(gray, 50, 200,apertureSize=3)


# 进行 Hough 直线检测
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=20)
# lines = cv2.HoughLines(edges,1,np.pi/180,0)

# 计算直线的斜率和截距
slopes = []
intercepts = []
print(len(lines))
for line in lines:
    x1, y1, x2, y2 = line[0]
    if x2 - x1 == 0:
        slope = 999.9 
    else:
        slope = (y2 - y1) / (x2 - x1)
    if abs(slope) > 0.5:
        slopes.append(slope)
        intercepts.append(y1 - slope*x1)

# 计算倾斜度的估计值
mean_slope = np.mean(slopes)
mean_intercept = np.mean(intercepts)

# 计算旋转角度
angle = np.arctan(mean_slope) * 180 / np.pi
M = cv2.getRotationMatrix2D((img.shape[1]/2, img.shape[0]/2), angle, 1.0)
rotated = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

# 保存结果
cv2.imwrite('output.jpg', rotated)