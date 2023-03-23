import cv2
import pytesseract

img = cv2.imread('testImg/xx1.jpeg')

# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 进行边缘检测
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# 检测轮廓
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 遍历轮廓
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    area = w * h
    if area > 1000 and area < 5000:
        # 裁剪出车牌
        plate_img = img[y:y+h, x:x+w]
        # 进行 OCR 识别
        text = pytesseract.image_to_string(plate_img, lang='chi_sim')
        if 6<=len(text):
            print(text)
            # 在原图上绘制车牌区域
            cv2.rectangle(img, (x,y), (x+w,y+h), (0, 0, 255), 2)

# 显示结果
cv2.imshow('result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
