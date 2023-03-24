import paddlehub as hub
import cv2

# 待转换图片的相对地址
picture = './R-C2.jpeg'
# 风格图片的相对地址
style_image = './R-C.jpeg'

# 创建风格转移网络并加载参数
stylepro_artistic = hub.Module(name="stylepro_artistic")

# 读入图片并开始风格转换
result = stylepro_artistic.style_transfer(
                    images=[{'content': cv2.imread(picture),
                             'styles': [cv2.imread(style_image)]}],
                    visualization=True
)
