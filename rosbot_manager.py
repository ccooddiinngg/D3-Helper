"""
ROS-BOT 运行与启动管理模块
提供检测和以管理员权限启动ROS-BOT的能力
"""

import time
import ctypes
import logging
from config import ROS_BOT_PROCESS_NAME, ROS_BOT_EXE_PATH, ROS_BOT_START_DELAY
from process_manager import is_process_running

logger = logging.getLogger()


def is_rosbot_running():
    """检测ROS-BOT是否运行中"""
    return is_process_running(ROS_BOT_PROCESS_NAME)


def launch_rosbot_admin():
    """以管理员权限启动ROS-BOT"""
    if is_rosbot_running():
        logger.info("ROS-BOT 已在运行。")
        return True
    try:
        logger.info("ROS-BOT 未运行，尝试以管理员权限启动...")
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", ROS_BOT_EXE_PATH, "", None, 1
        )
        time.sleep(ROS_BOT_START_DELAY)
        if is_rosbot_running():
            logger.info("ROS-BOT 启动成功。")
            return True
        else:
            logger.warning("ROS-BOT 启动后进程未检测到。")
            return False
    except Exception as e:
        logger.error(f"启动 ROS-BOT 时出错: {e}")
        return False
