import cv2
import numpy as np
from PIL import Image
import tensorflow as tf

szFileName="i1.jpg"

# 读取原始图像
img = cv2.imread(szFileName)

# 利用Tensorflow机器学习模型检测图像中需要处理的区域
# 真实的模型可以通过从TensorFlow模型库中下载和训练获得
tensorflow_model = tf.keras.models.load_model("tensorflow_model.h5")
image = Image.open(szFileName)
img_array = np.array(image)
img_tensor = np.expand_dims(img_array, axis=0)
predictions = tensorflow_model.predict(img_tensor)
bounding_box = [int(pred) for pred in predictions[0]]

# 确定需要被处理的区域，并截取其中的图像部分
x = bounding_box[0]
y = bounding_box[1]
w = bounding_box[2]
h = bounding_box[3]
if w > 50 and h > 50:  # 检查是否需要矫正
    img_cropped = img[y:y+h, x:x+w]
else:
    img_cropped = img

# 进行任意角度梯形矫正
height, width = img_cropped.shape[:2]
gray = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
angles = []
if lines is not None:
    for i in range(len(lines)):
        x1, y1, x2, y2 = lines[i][0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        angles.append(angle)
    median_angle = np.median(angles)
    M = cv2.getRotationMatrix2D((width / 2, height / 2), median_angle, 1)
    img_rotated = cv2.warpAffine(img_cropped, M, (width, height), flags=cv2.INTER_CUBIC)
else:
    img_rotated = img_cropped

# 进行任意畸变矫正
img_gray = cv2.cvtColor(img_rotated, cv2.COLOR_BGR2GRAY)
ret, img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
kernel = np.ones((10,10), np.uint8)
closing = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernel)
contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

if len(contours)>0:
    x,y,w,h = cv2.boundingRect(contours[0])
    if w > 50 and h > 50:  # 检查是否需要矫正
        result = img_rotated[y:y+h,x:x+w]
        
        # 进行任意角度倾斜矫正
        gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
        if lines is not None:
            angles = []
            for i in range(len(lines)):
                rho,theta = lines[i][0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                angles.append(angle)
            if len(angles) > 0:
                median_angle = np.median(angles)
                M = cv2.getRotationMatrix2D((result.shape[1]/2,result.shape[0]/2), median_angle, 1)
                result = cv2.warpAffine(result, M, (result.shape[1],result.shape[0]), flags=cv2.INTER_CUBIC)
    
        # 对不清晰的区域进行增强
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)
        result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    else:
        result = img_rotated
else:
    result = img_rotated

# 输出结果
cv2.imwrite('output.jpg', result)