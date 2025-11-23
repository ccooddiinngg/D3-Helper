"""
进程管理模块
处理进程检测和窗口操作
"""

import ctypes
import logging
import time

import psutil
import win32con
import win32gui
import win32process

logger = logging.getLogger()
ASFW_ANY = -1


def _iter_process_infos(process_name):
    """枚举与给定名称匹配的所有进程信息"""
    target_name = process_name.lower()
    for proc in psutil.process_iter(["pid", "name", "exe"]):
        try:
            name = proc.info.get("name")
            if name and name.lower() == target_name:
                yield proc.info
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue


def _get_process_info(process_name):
    """获取匹配的第一个进程信息"""
    return next(_iter_process_infos(process_name), None)


def is_process_running(process_name):
    """
    检查指定进程是否正在运行

    参数:
        process_name: 进程名称（如 "Diablo III64.exe"）

    返回:
        bool: 进程正在运行返回True，否则返回False
    """
    try:
        return _get_process_info(process_name) is not None
    except Exception as e:
        logger.error(f"检查进程 {process_name} 时出错: {e}")
        return False


def _find_window_for_pid(pid, title_hint=None):
    """在窗口列表中查找指定PID的窗口"""
    matches = []
    title_hint_lower = title_hint.lower() if title_hint else None

    def enum_callback(hwnd, matched_hwnds):
        try:
            if not win32gui.IsWindowVisible(hwnd):
                return
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid != pid:
                return
            title = win32gui.GetWindowText(hwnd)
            if title_hint_lower and title_hint_lower not in title.lower():
                return
            matched_hwnds.append(hwnd)
        except Exception:
            pass

    win32gui.EnumWindows(enum_callback, matches)
    return matches[0] if matches else None


def _set_foreground_window(hwnd):
    """将窗口恢复并置于前台"""
    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        else:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    except Exception:
        pass

    try:
        ctypes.windll.user32.AllowSetForegroundWindow(ASFW_ANY)
    except Exception:
        pass

    try:
        win32gui.SetForegroundWindow(hwnd)
        return
    except Exception:
        pass

    try:
        foreground = win32gui.GetForegroundWindow()
        if foreground:
            target_thread, _ = win32process.GetWindowThreadProcessId(hwnd)
            foreground_thread, _ = win32process.GetWindowThreadProcessId(foreground)
            user32 = ctypes.windll.user32
            if target_thread != foreground_thread:
                user32.AttachThreadInput(target_thread, foreground_thread, True)
                win32gui.SetForegroundWindow(hwnd)
                user32.AttachThreadInput(target_thread, foreground_thread, False)
    except Exception:
        pass


def find_window_by_title(part_title, process_name=None):
    """
    根据标题查找窗口，并尽可能关联指定进程

    参数:
        part_title: 窗口标题的一部分（不区分大小写）
        process_name: 可选，进程名称，用于限定窗口所属进程

    返回:
        tuple: (left, top, width, height) 或 None
    """
    try:
        title_filter = part_title.lower() if part_title else None
        hwnd = None
        if process_name:
            process_found = False
            for process_info in _iter_process_infos(process_name):
                process_found = True
                hwnd = _find_window_for_pid(process_info["pid"], part_title)
                if hwnd:
                    break
            if not process_found:
                return None

        if hwnd is None:
            results = []

            def enum_callback(hwnd, results):
                try:
                    if not win32gui.IsWindowVisible(hwnd):
                        return
                    title = win32gui.GetWindowText(hwnd)
                    if title_filter is None:
                        results.append(hwnd)
                        return
                    if title and title_filter in title.lower():
                        results.append(hwnd)
                except Exception:
                    pass

            win32gui.EnumWindows(enum_callback, results)
            if not results:
                return None
            hwnd = results[0]

        _set_foreground_window(hwnd)
        time.sleep(0.2)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        return (left, top, right - left, bottom - top)
    except Exception as e:
        logger.error(f"查找窗口 {part_title} 时出错: {e}")
        return None


def focus_process_window(process_name, title_hint=None):
    """
    查找并激活指定进程所属窗口

    参数:
        process_name: 进程名称
        title_hint: 可选窗口标题关键字

    返回:
        tuple: (left, top, width, height) 或 None
    """
    try:
        for process_info in _iter_process_infos(process_name):
            hwnd = _find_window_for_pid(process_info["pid"], title_hint)
            if hwnd:
                break
        else:
            return None

        _set_foreground_window(hwnd)
        time.sleep(0.2)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        return (left, top, right - left, bottom - top)
    except Exception as e:
        logger.error(f"激活进程 {process_name} 窗口时出错: {e}")
        return None


def terminate_process(process_name, wait_timeout=5):
    """
    终止指定名称的所有进程

    参数:
        process_name: 进程名称
        wait_timeout: 终止后等待退出的秒数

    返回:
        bool: 成功请求终止返回True，否则返回False
    """
    processes = []
    target_name = process_name.lower()
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            name = proc.info.get("name")
            if name and name.lower() == target_name:
                processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not processes:
        return False

    success = True
    for proc in processes:
        try:
            proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
            logger.warning(f"终止进程 {process_name} ({proc.pid}) 失败: {exc}")
            success = False

    gone, alive = psutil.wait_procs(processes, timeout=wait_timeout)
    for proc in alive:
        try:
            proc.kill()
            proc.wait(timeout=wait_timeout)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        except psutil.TimeoutExpired:
            logger.error(f"强制结束进程 {process_name} ({proc.pid}) 超时")
            success = False

    return success
