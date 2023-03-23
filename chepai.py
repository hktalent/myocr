#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests as requestsSs
import easyocr,urllib3


# pip uninstall opencv-python
# pip uninstall opencv-contrib-python
# pip uninstall opencv-contrib-python-headless
# pc4 pip3 install opencv-contrib-python==4.7.0.72 opencv-python==4.7.0.72 opencv-contrib-python-headless==4.7.0.72

# pc4 pip3 install opencv-python==4.5.4.60 opencv-contrib-python-headless==4.5.4.60 opencv-contrib-python==4.5.4.60 
# 查看,版本要一直
# pip list|grep opencv
# opencv-contrib-python                             4.5.4.60
# opencv-contrib-python-headless                    4.5.4.60
# opencv-python                                     4.5.4.60
# opencv-python-headless                            4.5.4.60

# pip3 install  PyWavelets Pillow imageio networkx scikit-image kiwisolver cycler matplotlib imgaug
# pc4 pip3 install torch torchvision>=0.5 opencv-python-headless<=4.5.4.60 scipy numpy Pillow scikit-image python-bidi PyYAML Shapely pyclipper ninja

urllib3.disable_warnings()
requestsSs.packages.urllib3.disable_warnings()

# easyocr -l ch_sim en -f testImg/xx1.jpg --detail=1 --gpu=False
# ,CUDA=None,detail=0,,recognition='Transformer'
# ：easyocr 默认的 OCR 引擎为 Tesseract，尝试切换到其他引擎，例如 Kraken、CuneiForm 等，可能会得到更好的识别结果。
reader = easyocr.Reader(['ch_sim','en'],gpu=False,detector=True,model_storage_directory="/Users/51pwn/MyWork/mybugbounty/ai/modle") # this needs to run only once to load the model into memory
result = reader.readtext('testImg/xxx.jpg', detail=0)
print(result)

