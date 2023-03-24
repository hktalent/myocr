import matplotlib.pyplot as plt 
import matplotlib.image as mpimg 
import paddlehub as hub
import os
import cv2

"""
python testId.py 

pip install --upgrade paddlepaddle
修改 ~/.paddlehub/modules/chinese_ocr_db_crnn_mobile/module.py 文件，
将第83行的 config.set_mkldnn_cache_capacity(10) 改为 config.switch_use_feed_fetch_ops(False)
wget -c https://bj.bcebos.com/paddlehub/paddlehub_dev/chinese_text_detection_db_mobile_1.1.0.zip
pip uninstall -y paddlepaddle paddlehub
pc4 pip install paddlepaddle paddlehub
pc4 pip install --upgrade numpy
pip install --upgrade paddlepaddle paddlehub opencv-python

pip uninstall -y numpy
pc4 pip install "Numpy==1.23.5"

对于 paddleocr 命令行中的参数，您可以通过在代码中设置对应的变量来使用。

• --image_dir 参数对应的是图像路径，因此您应该在代码中指定图像的路径。
• --ocr_version 参数对应的是 OCR 版本，目前支持的版本有 PP-OCRv2、PP-OCRv2_det、PP-OCRv3、ch_ppocr_mobile_v2.0_rec_pre、ch_ppocr_server_v2.0_rec_infer 等，因此您可以在代码中指定要使用的 OCR 模型。
• --use_angle_cls 参数对应的是是否使用文本方向分类器，您可以在代码中设置一个布尔值来控制是否使用。
• --use_gpu 参数对应的是是否使用 GPU 进行识别，您可以在代码中设置一个布尔值来控制。

"""

# 加载移动端预训练模型 /Users/51pwn/.paddlehub/modules/chinese_text_detection_db_mobile
# ocr = hub.Module(name="chinese_text_detection_db_mobile")
# 待预测图片
home_dir = os.path.expanduser('~')
test_img_path = [home_dir+"/MyWork/mybugbounty/ai/xx.png",home_dir+"/MyWork/mybugbounty/ai/i1.jpg",home_dir+"/MyWork/mybugbounty/ai/i1_corrected.jpg"]

# # 展示其中广告信息图片 chinese_ocr_db_crnn_server
# ocr = hub.Module(name="chinese_ocr_db_crnn_mobile", enable_mkldnn=False)       # mkldnn加速仅在CPU下有效
# 服务端可以加载大模型，效果更好 
ocr = hub.Module(name="chinese_ocr_db_crnn_server") 
for x in test_img_path:
    results = ocr.recognize_text(#recognize_text
        images=[cv2.imread(x)],         # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
        use_gpu=False,            # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
        visualization=False)          # 识别中文文本置信度的阈值；
        # ,       # 是否将识别结果保存为图片文件；
        # output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
        # box_thresh=0.5,           # 检测文本框置信度的阈值；
        # text_thresh=0.3
    # print(results)
    for result in results:
        data = result['data']
        save_path = result['save_path']
        for infomation in data:
            print('text: ', infomation['text'], '\nconfidence: ', infomation['confidence'])#, '\ntext_box_position: ', infomation['text_box_position']
    print("\n\n")

# ocr_detection = hub.Module(name="chinese_text_detection_db_server")
# ocr_recognition = hub.Module(name="chinese_ocr_db_crnn_server")

# for x in test_img_path:
#     # 文本检测
#     result_detection = ocr_detection.text_detection(images=[cv2.imread(x)])
#     boxes = result_detection[0]['data']

#     # 取出检测框中的文本
#     texts = []
#     for box in boxes:
#         text, *_ = ocr_recognition.recognize_text([cv2.imread(x)], [box])
#         texts.append(text)

#     print(texts)