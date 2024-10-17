import cv2
import numpy as np
import pytesseract
from PIL import Image
import pyautogui
import time
import config
from pynput.keyboard import Controller, Key  # 导入 Key

keyboard = Controller()

class Solve:
    def __init__(self):
        self.left_num_last = 0
        self.right_num_last = 0
        self.error_count = 0
        self.isContinue = False
        self.operation_save = ["<", ">", "="]
        self.has_seen_number = False  # 新增标志位
        self.last_seen_time = time.time()  # 用于记录最后一次看到数字的时间
        self.space_pressed = False  # 新增标志位表示是否已经按过空格

    def solve(self, left_number_img, right_number_img, window):
        # 确保输入图像是 uint8 类型
        if left_number_img.dtype != np.uint8:
            left_number_img = (
                255
                * (left_number_img - np.min(left_number_img))
                / np.ptp(left_number_img)
            ).astype(np.uint8)
        if right_number_img.dtype != np.uint8:
            right_number_img = (
                255
                * (right_number_img - np.min(right_number_img))
                / np.ptp(right_number_img)
            ).astype(np.uint8)

        left_gray = cv2.cvtColor(left_number_img, cv2.COLOR_BGR2GRAY)
        right_gray = cv2.cvtColor(right_number_img, cv2.COLOR_BGR2GRAY)

        # 二值化处理
        _, left_number_img = cv2.threshold(left_gray, 127, 255, cv2.THRESH_BINARY)
        _, right_number_img = cv2.threshold(right_gray, 127, 255, cv2.THRESH_BINARY)

        # 将图像数据转换为 PIL 格式
        left_number_img_pil = Image.fromarray(left_number_img)
        right_number_img_pil = Image.fromarray(right_number_img)

        # OCR 识别
        left_num = pytesseract.image_to_string(
            left_number_img_pil, config="--oem 3 --psm 6 outputbase digits"
        )
        right_num = pytesseract.image_to_string(
            right_number_img_pil, config="--oem 3 --psm 6 outputbase digits"
        )

        # converting string to int
        try:
            left_num = int(left_num)
            right_num = int(right_num)
            self.has_seen_number = True  # 如果成功识别数字，设置标志位为 True
            self.last_seen_time = time.time()  # 更新最后看到数字的时间
        except ValueError:
            left_num = 0
            right_num = 0

        def calculate(left_num, right_num):
            operations = ["<", ">", "=", "break"]
            if left_num < right_num:
                return operations[0]
            elif left_num > right_num:
                return operations[1]
            elif left_num == right_num and left_num != 0 and right_num != 0:
                return operations[2]
            else:
                return operations[3]

        operation = calculate(left_num, right_num)

        def press_key(operation):
            if operation == "<":
                keyboard.press('a')
                keyboard.release('a')
            elif operation == ">":
                keyboard.press('d')
                keyboard.release('d')

        if left_num == 0 and right_num == 0:
            # 未识别出任何数字
            if not self.has_seen_number:
                print(
                    "没有找到数字，如果游戏进行中，请调整窗口位置，确保为竖屏，且窗口越大越好，需要确保数字在绿色框中"
                )
            else:
                # 检测时间是否超过4秒且之前看到过数字
                if time.time() - self.last_seen_time > 4 and not self.space_pressed:
                    print("没有找到数字，可能游戏已结束，自动点击继续")
                    for _ in range(4):  # 按四次空格
                        keyboard.press(Key.space)  # 自动按空格
                        keyboard.release(Key.space)
                        time.sleep(0.5)  # 停顿0.5秒
                    self.space_pressed = True  # 设置为已按空格

        else:
            # 识别了数字，清除空格按压标志位
            if left_num != self.left_num_last or right_num != self.right_num_last:
                self.error_count = 0
                press_key(operation)
                print(f"operation: {operation}")
                self.space_pressed = False  # 识别数字后清除空格按压标志位

        if (
            left_num == self.left_num_last
            and right_num == self.right_num_last
            and (left_num != 0 or right_num != 0)
        ):
            self.error_count += 1

        if self.error_count > 5:
            for oper in self.operation_save:
                press_key(oper)
                time.sleep(1)

        self.left_num_last = left_num
        self.right_num_last = right_num
