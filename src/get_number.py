import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import config


def get_number():
    window = gw.getWindowsWithTitle("MuMu模拟器12")[0]

    # 获取窗口的截图
    window_screenshot = pyautogui.screenshot(
        region=(window.left, window.top, window.width, window.height)
    )

    def find_question(window_screenshot):
        img = cv2.cvtColor(np.array(window_screenshot), cv2.COLOR_RGB2BGR)

        # 使用配置文件中的固定坐标，并添加偏移量
        left_offset_x = 450  # 左边数字X方向偏移量
        left_offset_y = -40 # 左边数字Y方向偏移量

        right_offset_x = 470  # 右边数字X方向偏移量
        right_offset_y = -40 # 右边数字Y方向偏移量

        left_number_x1 = config.LEFT_NUMBER_X1 + left_offset_x
        left_number_x2 = config.LEFT_NUMBER_X2 + left_offset_x
        left_number_y1 = config.LEFT_NUMBER_Y1 + left_offset_y
        left_number_y2 = config.LEFT_NUMBER_Y2 + left_offset_y

        right_number_x1 = config.RIGHT_NUMBER_X1 + right_offset_x
        right_number_x2 = config.RIGHT_NUMBER_X2 + right_offset_x
        right_number_y1 = config.RIGHT_NUMBER_Y1 + right_offset_y
        right_number_y2 = config.RIGHT_NUMBER_Y2 + right_offset_y

        # 在 img 中画出左边数字的候选框
        cv2.rectangle(
            img,
            (left_number_x1, left_number_y1),
            (left_number_x2, left_number_y2),
            (0, 255, 0),
            2,
        )

        # 在 img 中画出右边数字的候选框
        cv2.rectangle(
            img,
            (right_number_x1, right_number_y1),
            (right_number_x2, right_number_y2),
            (0, 255, 0),
            2,
        )

        # 显示带有候选框的原始图像（img）
        cv2.imshow("Bounding Boxes in Original Image", img)

        # 提取左边和右边的数字区域
        left_number = img[left_number_y1:left_number_y2, left_number_x1:left_number_x2]
        right_number = img[
            right_number_y1:right_number_y2, right_number_x1:right_number_x2
        ]
        return left_number, right_number, img

    left_number = np.zeros(
        (
            (config.LEFT_NUMBER_Y2 - config.LEFT_NUMBER_Y1),
            (config.LEFT_NUMBER_X2 - config.LEFT_NUMBER_X1),
            3,
        )
    )
    right_number = np.zeros(
        (
            (config.RIGHT_NUMBER_Y2 - config.RIGHT_NUMBER_Y1),
            (config.RIGHT_NUMBER_X2 - config.RIGHT_NUMBER_X1),
            3,
        )
    )

    if window.isActive:
        left_number, right_number, _ = find_question(window_screenshot)

    # 在返回之前检查图像大小的有效性
    if left_number.size > 0 and right_number.size > 0:
        return left_number, right_number, window
    else:
        return (
            np.zeros(
                (
                    (config.LEFT_NUMBER_Y2 - config.LEFT_NUMBER_Y1),
                    (config.LEFT_NUMBER_X2 - config.LEFT_NUMBER_X1),
                    3,
                )
            ),
            np.zeros(
                (
                    (config.RIGHT_NUMBER_Y2 - config.RIGHT_NUMBER_Y1),
                    (config.RIGHT_NUMBER_X2 - config.RIGHT_NUMBER_X1),
                    3,
                )
            ),
            window,
        )
