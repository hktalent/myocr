import pytesseract
from PIL import Image
import cv2


def Corver_Gray(image_path):
    # 读取模板图像
    img = cv2.imread(image_path)

    # 转换为灰度图 也可读取时直接转换
    ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 二值图像
    ref = cv2.threshold(ref, 60, 255, cv2.THRESH_BINARY_INV)[1]

    return ref


def Read_Img(img_path):
    image = Corver_Gray(img_path)
    image = cv2.imwrite("test.png", image)
    return image


for x in ['xx1.jpg','xx2.jpg','xx3.jpg','xxx.jpg']:
	print(x)
	# 打开图片并进行预处理
	img = Image.open(x)
	# img = Read_Img(x)
	# 进行其他预处理操作，如缩放、旋转，以便更好地识别

	# 执行OCR识别
	result = pytesseract.image_to_string(img, lang='chi_sim')

	# 输出结果
	print(result)

