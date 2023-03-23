# import opencv
import cv2
# import hyperlpr3
import hyperlpr3 as lpr3

# pc4 pip install hyperlpr3
# Instantiate object
catcher = lpr3.LicensePlateCatcher()
# load image
image = cv2.imread("testImg/xx2.jpeg")
# print result
print(catcher(image))
