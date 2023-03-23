import cv2
import numpy as np
from matplotlib import pyplot as plt

# 加载待处理图像，将其转换为灰度图像
img = cv2.imread("/Users/51pwn/MyWork/mybugbounty/ai/i1.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 对灰度图像进行阈值分割，得到二值图像
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# 对二值图像进行形态学操作，去除噪声
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

# 进行轮廓检测，获取包含文本区域的矩形框
contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
rectangles = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    rectangles.append([x, y, x+w, y+h])
rectangles = np.array(rectangles)

# 根据文本区域的矩形框，进行透视变换和裁剪
if len(rectangles) > 0:
    top_left = np.amin(rectangles, axis=0)[:2]
    bottom_right = np.amax(rectangles, axis=0)[2:]
    img = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    gray = gray[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

# 根据文本区域的矩形框，获取梯形的四个角点
edges = cv2.Canny(gray, 50, 200, None, 3)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
points = []
for line in lines:
    x1, y1, x2, y2 = line[0]
    points.append((x1, y1))
    points.append((x2, y2))
points = np.array(list(set(points)))
if len(points) > 0:
    rect = cv2.minAreaRect(points)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # 根据梯形的四个角点，进行透视变换和裁剪，将梯形转换为正方形
    width = max(np.linalg.norm(box[0] - box[1]), np.linalg.norm(box[2] - box[3]))
    height = max(np.linalg.norm(box[0] - box[3]), np.linalg.norm(box[1] - box[2]))
    dst_pts = np.array([[0, 0], [width, 0], [0, height], [width, height]], dtype=np.float32)
    src_pts = np.array(box, dtype=np.float32)
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    img = cv2.warpPerspective(img, M, (int(width), int(height)))

    # 根据需要对矫正后的图像进行裁剪，并输出裁剪后的图像
    h, w = img.shape[:2]
    crop_top = int(h * 0.1)
    crop_bottom = int(h * 0.1)
    crop_left = int(w * 0.1)
    crop_right = int(w * 0.1)
    img_cropped = img[crop_top:h-crop_bottom, crop_left:w-crop_right]

    # 显示和保存结果
    plt.imshow(img_cropped[:, :, [2, 1, 0]])
    plt.show()
    cv2.imwrite("output.jpg", img_cropped)
else:
    print("No quadrangle found in the image")