from matplotlib import pyplot as plt
import cv2
import numpy as np

# 对扫描件的处理

szFileNmae="/Users/51pwn/MyWork/mybugbounty/ai/i1.jpg"

def show_img(name, img):
    plt.subplot(1,1,1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(name, fontdict={'fontsize':16, 'color':'b'})
    plt.show()

def find_corners(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for cnt in cnts:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4:
            return approx.reshape(4, 2)

def order_points(pts):
    rect = np.zeros((4, 2), dtype=np.float32)
    if pts is None or len(pts) < 4:# 如果 pts 为空或长度不足 4，返回一个空矩阵
        return rect
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def perspective_transform(img, rect):
    rect = order_points(rect)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
    return warped

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    img = cv2.dilate(img, np.ones((3, 3), np.uint8), iterations=1)
    img = cv2.bitwise_not(img)
    return img

def find_digits(img):
    digits = []
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        area = w*h
        if area > 1000 and area < 4000 and w < 100 and h < 100:
            digit = img[y:y+h, x:x+w]
            digit = cv2.resize(digit, (28, 28))
            digits.append(digit)
    return digits

def recognize_digit(digit):
    # TODO: digit recognition using machine learning model
    return "?" # for now, return a question mark for unrecognized digit

def solve_sudoku(img):
    corners = find_corners(img)
    warped = perspective_transform(img, corners)
    processed = preprocess(warped)
    digits = find_digits(processed)
    board = np.zeros((9, 9), dtype=np.int32)
    for i, digit in enumerate(digits):
        row, col = divmod(i, 9)
        board[row, col] = recognize_digit(digit)
    # TODO: solve sudoku and return solution

img = cv2.imread(szFileNmae)

image_copy = np.copy(img)
image_copy = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
lower_blue = np.array([0,0,230])  
upper_blue = np.array([250,250,255])
mask = cv2.inRange(image_copy, lower_blue, upper_blue)
masked_image = np.copy(image_copy)
masked_image[mask != 0] = [0, 0, 0]
# plt.imshow(masked_image)
show_img("dst", masked_image)

# img1=solve_sudoku(img)
# if img1 != None:
#     img=img1
# img_h, img_w, _ = img.shape

# # 这里调整，颜色范围局域的单个
# lower = (35, 0, 0)
# upper = (120, 255, 255)

# blurred = cv2.GaussianBlur(img, (5, 5), 0)

# hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

# # inRange的作用是根据阈值进行二值化:阈值内的像素设置为白色(255)，阈值外的设置为黑色(0)
# mask = cv2.inRange(hsv, lower, upper)

# mask = cv2.erode(mask, None, iterations=2)

# mask = cv2.dilate(mask, None, iterations=2)

# contours, _hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# max_i = 0
# for i,cnt in enumerate(contours):
#     if cv2.contourArea(cnt) > cv2.contourArea(contours[max_i]):
#         max_i = i

# peri = cv2.arcLength(contours[max_i], True)
# approx = cv2.approxPolyDP(contours[max_i], 0.02 * peri, True)

# # cv2.drawContours(img,[contours[max_i]],0,(255,0,0),10)

# # 这四个点为原始图片上数独的位置
# pts_o = np.float32([approx[0][0], approx[1][0],  approx[2][0], approx[3][0]])
# # 这是变换之后的图上四个点的位置
# pts_d = np.float32([[img_w, 0], [0, 0], [0, img_h], [img_w, img_h]])

# M = cv2.getPerspectiveTransform(pts_o, pts_d)

# dst = cv2.warpPerspective(img, M, (img_w, img_h)) 
    
# show_img("dst", dst)