# myocr


# How use
## OCR
```
ln -s $PWD/whl $HOME/.paddleocr/whl

paddleocr=$HOME/anaconda3/envs/paddle_env/bin/paddleocr
paddleocr --image_dir realesrgan-ncnn-vulkan-20220424-macos/input3.jpg --use_angle_cls true --use_gpu false
paddleocr --image_dir testImg/xx31.jpg --use_angle_cls true --use_gpu false
paddleocr --image_dir testImg/xx2.jpeg --use_angle_cls true --use_gpu false
paddleocr --image_dir testImg/xx1.jpeg --use_angle_cls true --use_gpu false
paddleocr --image_dir "/Users/51pwn/MyWork/mybugbounty/ai/i1.jpg" --ocr_version PP-OCRv3 --use_angle_cls true --use_gpu false
paddleocr --image_dir "/Users/51pwn/MyWork/mybugbounty/ai/i1.jpg" --use_angle_cls true --use_gpu false --det_db_box_thresh 0.5 --det_db_unclip_ratio 1.5 --use_space_char true

pc4 pip install paddleocr

```
## 车牌ORV
```
py3 chepai3.py
```

