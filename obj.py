#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 创建分类器对象
"""
OpenCV 中提供了多种分类器用于目标检测，包括以下四种：

1. haarcascades： 基于 Haar 特征的分类器，适用于人脸、眼睛等目标的检测。
2. haarcascades_cuda：基于 Haar 特征的 GPU 加速分类器，可用于实时应用程序。
3. hogcascades： 基于 HOG（方向梯度直方图）特征的分类器，适用于行人检测等目标。
4. lbpcascades： 基于 LBP（局部二值模式）特征的分类器，同样适用于人脸等目标的检测。通常比 Haar 特征的分类器更快和准确。

如果你需要一个快速的人脸检测器，可以使用 lbpcascades 分类器，如果需要适用于复杂环境下的人脸检测，则可以使用 haarcascades 分类器。如果需要实时应用程序可以使用 haarcascades_cuda 分类器，hogcascades 分类器可以被用于行人捕捉以及其它物体的检测。

总之，不同的分类器拥有不同的特点和用途，根据你的实际需求选择相应的分类器会有更好的效果。
"""

import cv2,os
import numpy as np
import concurrent.futures

# 读取图片
img = cv2.imread("/Users/51pwn/MyWork/mybugbounty/ai/i1.jpg")

# xml文件目录
XML_DIR = os.getcwd() + "/xml"

# 查找xml文件
def search_xml_files(directory):
    xml_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".xml"):
                xml_files.append(os.path.join(root, file))
    return xml_files


# 并行加载cascade文件
def load_cascade(cascade_path):
    # print(f"Loading cascade from {cascade_path}")
    # cascade = cv2.CascadeClassifier(cascade_path)
    cascade = cv2.CascadeClassifier(cascade_path)
    return cascade

# 获取所有cascade分类器
def get_all_cascades():
    xml_files = search_xml_files(XML_DIR)
    cascades = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(load_cascade, f) for f in xml_files]
        for f in concurrent.futures.as_completed(results):
            cascade = f.result()
            cascades.append(cascade)
    return cascades

# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cascades = get_all_cascades()
print("cascades: "+str(len(cascades)))
# cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# 对灰度图像进行识别
faces=[]
for c in cascades:
    x=c.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    if len(x) == 4:
        faces.append(x)

# 标记物体
for face in faces:
    if len(face) != 4:
        continue
    (x, y, w, h) = face
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# 显示结果
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()