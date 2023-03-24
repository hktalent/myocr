import cv2
import numpy as np
import pytesseract

# 读取图像
img = cv2.imread("/Users/51pwn/MyWork/mybugbounty/ai/i1.jpg")

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
text = pytesseract.image_to_string(img, lang='chi_sim')

# 打印结果
print(text)

