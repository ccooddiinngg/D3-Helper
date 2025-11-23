"""
服务重启模块
封装 Battle.net、Diablo III 与 ROS-BOT 的重启逻辑
"""

import logging
from game_launcher import launch_battle_net, launch_diablo_iii
from rosbot_manager import launch_rosbot_admin

logger = logging.getLogger()


def restart_diablo_iii():
    logger.info("Diablo III 未运行，正在尝试启动...")
    return launch_diablo_iii()


def restart_battle_net():
    logger.info("Battle.net 未运行，正在尝试启动...")
    return launch_battle_net()


def restart_rosbot():
    logger.info("ROS-BOT 未运行，正在尝试以管理员权限启动...")
    return launch_rosbot_admin()

