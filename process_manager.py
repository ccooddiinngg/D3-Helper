"""
进程管理模块
处理进程检测和窗口操作
"""

import psutil
import logging
import win32gui
import win32con
import time

logger = logging.getLogger()


def is_process_running(process_name):
    """
    检查指定进程是否正在运行

    参数:
        process_name: 进程名称（如 "Diablo III64.exe"）

    返回:
        bool: 进程正在运行返回True，否则返回False
    """
    try:
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] == process_name:
                return True
        return False
    except Exception as e:
        logger.error(f"检查进程 {process_name} 时出错: {e}")
        return False


def find_window_by_title(part_title):
    """
    根据标题查找窗口

    参数:
        part_title: 窗口标题的一部分（不区分大小写）

    返回:
        tuple: (left, top, width, height) 或 None
    """
    results = []

    def enum_callback(hwnd, results):
        """窗口枚举回调函数"""
        try:
            title = win32gui.GetWindowText(hwnd)
            if (
                title
                and part_title.lower() in title.lower()
                and win32gui.IsWindowVisible(hwnd)
            ):
                results.append(hwnd)
        except Exception:
            pass

    try:
        win32gui.EnumWindows(enum_callback, results)
        if not results:
            return None

        hwnd = results[0]
        try:
            # 恢复最小化的窗口
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass

        time.sleep(0.2)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        return (left, top, right - left, bottom - top)
    except Exception as e:
        logger.error(f"查找窗口 {part_title} 时出错: {e}")
        return None
