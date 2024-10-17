# 小猿口算PK
# 1. 读取屏幕上的题目
# 2. 识别题目
# 3. 计算题目
# 4. 键盘模拟输出答案

from get_number import get_number
from solve import Solve
import cv2
import pytesseract
import os

# 获取当前脚本所在的目录路径
base_dir = os.path.dirname(os.path.abspath(__file__))

# 构造相对路径指向 Tesseract 可执行文件
tesseract_cmd = os.path.join(base_dir, '..', 'Tesseract-OCR', 'tesseract.exe')

# 设置 pytesseract 的 tesseract_cmd
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

if __name__ == "__main__":
    solve = Solve()
    while True:
        left_number_img, right_number_img, window = get_number()
        if window.isActive:
            solve.solve(left_number_img, right_number_img, window)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
