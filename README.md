# myocr


# How use
## OCR
```
ln -s $PWD/whl $HOME/.paddleocr/whl

paddleocr --image_dir realesrgan-ncnn-vulkan-20220424-macos/input3.jpg --use_angle_cls true --use_gpu false
paddleocr --image_dir testImg/xx31.jpg --use_angle_cls true --use_gpu false
paddleocr --image_dir testImg/xx2.jpeg --use_angle_cls true --use_gpu false
paddleocr --image_dir testImg/xx1.jpeg --use_angle_cls true --use_gpu false

```
## 车牌ORV
```
py3 chepai3.py
```

