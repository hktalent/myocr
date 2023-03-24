import easyocr
from PIL import Image

# 加载图像
img = Image.open("/Users/51pwn/MyWork/mybugbounty/ai/i1.jpg")

# 对图像进行矫正并保存
reader = easyocr.Reader(['ch_sim'])
corrected = reader.readtext(img, detail=0, paragraph=True)
img.save('/Users/51pwn/MyWork/mybugbounty/ai/i1_corrected.jpg')

# 进行OCR识别
result = reader.readtext('/Users/51pwn/MyWork/mybugbounty/ai/i1_corrected.jpg', detail=0, paragraph=True)

# 输出识别结果
print(result)