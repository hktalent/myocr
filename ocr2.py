import kraken
import numpy as np
import cv2

# 读取图像
img = cv2.imread('/Users/51pwn/MyWork/mybugbounty/ai/i1.jpg')

# 灰度化
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 二值化
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 倾斜矫正
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]
if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle
(h, w) = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# 保存矫正后的图像
cv2.imwrite('scan_corrected.jpg', img)

# OCR识别
with open("scan_corrected.jpg", 'rb') as f:
    im_bytes = f.read()

# 定义模型及其参数
model = kraken.models.load_any("kraken://pe/BaseOCR17.mlmodel")

# 进行识别
binarized = kraken.image.imread(im_bytes).asarray()
preds = kraken.rpred.recognize(binarized, model)

# 输出结果
print(preds) 
