"""
游戏启动器模块
处理Diablo III和Battle.net的启动逻辑
"""

import subprocess
import time
import logging
from config import (
    D3_PROCESS_NAME,
    BATTLE_NET_PROCESS_NAME,
    BATTLE_NET_EXE_PATH,
    PLAY_BUTTON_IMAGE,
    RADIO_BUTTON_IMAGE,
    OK_BUTTON_IMAGE,
    CONFIRM_BUTTON_IMAGE,
    OK_BROWSER_BUTTON_IMAGE,
    BATTLE_NET_START_DELAY,
)
from process_manager import is_process_running, find_window_by_title
from image_finder import find_and_click_image

logger = logging.getLogger()


def launch_battle_net():
    """启动Battle.net客户端"""
    if is_process_running(BATTLE_NET_PROCESS_NAME):
        logger.info("Battle.net 正在运行...")
        return True

    logger.info("正在启动 Battle.net...")
    try:
        subprocess.Popen(BATTLE_NET_EXE_PATH)
        logger.info("Battle.net 正在加载...")
        time.sleep(BATTLE_NET_START_DELAY)

        # 处理启动时的弹窗
        _handle_battle_net_popups()

        if is_process_running(BATTLE_NET_PROCESS_NAME):
            logger.info("Battle.net 启动成功")
            return True
        else:
            logger.warning("Battle.net 启动后进程未找到")
            return False
    except Exception as e:
        logger.error(f"启动 Battle.net 时出错: {e}")
        return False


def _handle_battle_net_popups():
    """处理Battle.net启动时的弹窗"""
    # 点击单选按钮
    find_and_click_image(RADIO_BUTTON_IMAGE, description="单选按钮", check_file=False)

    # 点击确认按钮
    find_and_click_image(
        [OK_BUTTON_IMAGE, CONFIRM_BUTTON_IMAGE],
        description="确认按钮",
        check_file=False,
    )

    # 点击浏览器中的确定按钮
    find_and_click_image(
        OK_BROWSER_BUTTON_IMAGE,
        description="浏览器中的'确定'按钮",
        check_file=False,
    )


def launch_diablo_iii():
    """启动Diablo III游戏"""
    # 确保Battle.net正在运行
    if not launch_battle_net():
        logger.error("无法启动 Battle.net，无法继续启动游戏")
        return False

    # 查找Battle.net窗口
    battle_net_window = find_window_by_title("Battle.net")
    if not battle_net_window:
        logger.warning("未找到 Battle.net 窗口")
        return False

    logger.info(f"找到 Battle.net 窗口，位置: {battle_net_window}")

    # 点击Play按钮
    if find_and_click_image(PLAY_BUTTON_IMAGE, description="Play按钮"):
        logger.info("已点击 Play 按钮，游戏正在启动...")
        return True
    else:
        logger.warning("未能找到并点击 Play 按钮")
        return False


def is_diablo_iii_running():
    """检查Diablo III是否正在运行"""
    return is_process_running(D3_PROCESS_NAME)
