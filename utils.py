"""
工具函数模块
提供通用的工具函数
"""

import sys
import ctypes
import logging
import win32gui
import win32con

logger = logging.getLogger()


def is_admin():
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    """以管理员权限重新运行程序"""
    if is_admin():
        return True
    else:
        try:
            # 重新以管理员权限运行程序
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            return False
        except Exception as e:
            logger.error(f"无法以管理员权限运行: {e}")
            return False


def enable_ansi_support():
    """启用Windows ANSI转义码支持（用于彩色输出）"""
    if sys.platform == "win32":
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception as e:
            logger.warning(f"无法启用ANSI支持: {e}")


def get_console_window_handle():
    """获取控制台窗口句柄"""
    if sys.platform == "win32":
        try:
            kernel32 = ctypes.windll.kernel32
            return kernel32.GetConsoleWindow()
        except Exception:
            return None
    return None


def show_console_window():
    """显示控制台窗口"""
    hwnd = get_console_window_handle()
    if hwnd:
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(hwnd)
            return True
        except Exception as e:
            logger.error(f"无法显示控制台窗口: {e}")
            return False
    return False


def hide_console_window():
    """隐藏控制台窗口"""
    hwnd = get_console_window_handle()
    if hwnd:
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            return True
        except Exception as e:
            logger.warning(f"无法隐藏控制台窗口: {e}")
            return False
    return False
