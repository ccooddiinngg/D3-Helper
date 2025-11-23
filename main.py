"""
Diablo III 自动启动器主程序
"""

import os
import sys
import threading
import atexit
import pyautogui
import logging

from config import (
    APP_NAME,
    PYAUTOGUI_FAILSAFE,
    PYAUTOGUI_PAUSE,
    MONITOR_CHECK_INTERVAL,
    MONITOR_THREAD_CHECK_INTERVAL,
    STOP_FILE,
)
from logger_config import setup_logging
from utils import (
    enable_ansi_support,
    is_admin,
    run_as_admin,
    show_console_window,
    hide_console_window,
)
from window_manager import WindowManager
from game_launcher import is_diablo_iii_running, is_battle_net_running
from rosbot_manager import is_rosbot_running
from service_monitor import ServiceMonitor
from service_rebooter import (
    restart_diablo_iii,
    restart_battle_net,
    restart_rosbot,
)

# 启用Windows ANSI转义码支持（用于彩色输出）
enable_ansi_support()

# 初始化日志
logger, log_file = setup_logging()
logger.info(f"日志文件已创建: {log_file}")

# 全局标志，用于控制后台循环
_running = True
_stop_event = threading.Event()
_window_manager = None
_service_monitors = []

# 检查并请求管理员权限
if not is_admin():
    logger.info("请求管理员权限...")
    if not run_as_admin():
        sys.exit(0)
    else:
        logger.info("已获得管理员权限")

# 配置pyautogui
pyautogui.FAILSAFE = PYAUTOGUI_FAILSAFE
pyautogui.PAUSE = PYAUTOGUI_PAUSE


def start_service_monitors():
    """初始化并启动各服务的后台监控线程"""
    global _service_monitors
    _service_monitors = [
        ServiceMonitor(
            "Diablo III",
            is_diablo_iii_running,
            restart_diablo_iii,
            MONITOR_CHECK_INTERVAL,
            _stop_event,
        ),
        ServiceMonitor(
            "Battle.net",
            is_battle_net_running,
            restart_battle_net,
            MONITOR_CHECK_INTERVAL,
            _stop_event,
        ),
        ServiceMonitor(
            "ROS-BOT",
            is_rosbot_running,
            restart_rosbot,
            MONITOR_CHECK_INTERVAL,
            _stop_event,
        ),
    ]
    for monitor in _service_monitors:
        monitor.start()


def stop_file_watcher():
    """监控停止文件，触发安全退出"""
    global _window_manager
    while _running and not _stop_event.is_set():
        if os.path.exists(STOP_FILE):
            logger.info("检测到停止文件，正在退出...")
            try:
                os.remove(STOP_FILE)
            except Exception as e:
                logger.warning(f"删除停止文件失败: {e}")

            stop_background()
            if _window_manager:
                _window_manager.stop()
            break

        if _stop_event.wait(MONITOR_THREAD_CHECK_INTERVAL):
            break


def stop_background():
    """停止后台运行"""
    global _running
    if not _running:
        return
    _running = False
    _stop_event.set()
    for monitor in _service_monitors:
        monitor.stop()
    logger.info("正在停止后台服务...")


def cleanup():
    """程序退出时的清理函数"""
    global _window_manager
    stop_background()
    if _window_manager:
        _window_manager.stop()
    logger.info("Diablo III 自动启动器已停止。")


# 注册退出时的清理函数
atexit.register(cleanup)


def main():
    """主函数"""
    global _window_manager

    logger.info(f"{APP_NAME} 已启动")
    logger.info("程序将在后台运行，所有日志将保存到日志文件中")

    # 初始化窗口管理器
    _window_manager = WindowManager(
        on_quit_callback=stop_background,
        on_show_console=show_console_window,
        on_hide_console=hide_console_window,
    )

    # 启动后台监控
    start_service_monitors()

    # 启动停止文件监控
    stop_file_thread = threading.Thread(target=stop_file_watcher, daemon=True)
    stop_file_thread.start()

    # 隐藏控制台窗口
    if hide_console_window():
        logger.info("控制台窗口已隐藏，程序在后台运行")

    try:
        if _window_manager.start():
            logger.info("管理窗口已关闭，程序将退出")
        else:
            logger.warning("管理窗口启动失败，程序将在后台运行")
    except KeyboardInterrupt:
        logger.info("\n收到退出信号，正在安全退出...")
    except Exception as e:
        logger.error(f"\n发生未预期的错误: {e}", exc_info=True)
    finally:
        stop_background()
        if _window_manager:
            _window_manager.stop()
        # 等待线程结束
        stop_file_thread.join(timeout=5)
        logger.info("程序已退出")


if __name__ == "__main__":
    main()
