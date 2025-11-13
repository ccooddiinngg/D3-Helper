"""
图片查找模块
处理图片识别和点击操作
"""

import os
import time
import pyautogui
import logging
from config import (
    IMAGE_SEARCH_MAX_ATTEMPTS,
    IMAGE_SEARCH_CONFIDENCE,
    IMAGE_SEARCH_RETRY_DELAY,
    CLICK_DELAY,
)

logger = logging.getLogger()


def find_and_click_image(
    image_paths,
    max_attempts=IMAGE_SEARCH_MAX_ATTEMPTS,
    confidence=IMAGE_SEARCH_CONFIDENCE,
    description="",
    check_file=True,
):
    """
    查找图片并点击

    参数:
        image_paths: 图片路径，可以是字符串（单个图片）或列表（多个图片，按顺序尝试）
        max_attempts: 最大尝试次数，默认10次
        confidence: 匹配置信度，默认0.8
        description: 描述信息，用于日志输出
        check_file: 是否检查文件是否存在，默认True

    返回:
        bool: 成功找到并点击返回True，否则返回False
    """
    # 将单个字符串转换为列表
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    # 检查图片文件是否存在
    if check_file:
        for img_path in image_paths:
            if not os.path.exists(img_path):
                if description:
                    logger.warning(
                        f"警告: {description} 的图片文件 {img_path} 不存在！"
                    )
                return False

    # 记录鼠标初始位置
    original_pos = pyautogui.position()

    # 尝试查找并点击图片
    for img_path in image_paths:
        if description:
            logger.info(f"正在查找{description}...")

        for attempt in range(max_attempts):
            try:
                found_image = pyautogui.locateOnScreen(img_path, confidence=confidence)
                if found_image:
                    x, y = pyautogui.center(found_image)
                    pyautogui.moveTo(x, y, duration=0.3)
                    pyautogui.click()
                    time.sleep(CLICK_DELAY)
                    if description:
                        logger.info(f"已点击{description}。")
                    # 鼠标返回原始位置
                    pyautogui.moveTo(original_pos)
                    return True
            except pyautogui.ImageNotFoundException:
                pass
            except Exception as e:
                if description:
                    logger.error(f"查找{description}时出错: {e}")
            time.sleep(IMAGE_SEARCH_RETRY_DELAY)

    # 所有尝试都失败
    if description:
        logger.warning(f"未能找到并点击{description}。")
    return False
