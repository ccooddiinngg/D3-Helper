"""
Windows窗口管理模块
提供GUI窗口来管理应用程序
"""

import os
import threading
import logging
import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from config import (
    WINDOW_TITLE,
    WINDOW_SIZE,
    LOG_DISPLAY_LINES,
    LOG_REFRESH_INTERVAL,
    LOG_DIR,
)
from utils import show_console_window, hide_console_window

logger = logging.getLogger()


class WindowManager:
    """Windows窗口管理器"""

    def __init__(
        self, on_quit_callback=None, on_show_console=None, on_hide_console=None
    ):
        """
        初始化窗口管理器

        参数:
            on_quit_callback: 退出回调函数
            on_show_console: 显示控制台回调函数
            on_hide_console: 隐藏控制台回调函数
        """
        self.on_quit = on_quit_callback
        self.on_show_console = on_show_console
        self.on_hide_console = on_hide_console
        self.root = None
        self.console_visible = False
        self.log_text = None
        self.runtime_label = None
        self.start_time = time.time()

    def show_console(self):
        """显示控制台窗口"""
        if self.on_show_console:
            self.on_show_console()
        else:
            show_console_window()
        self.console_visible = True
        logger.info("控制台窗口已显示")
        self.update_console_button()

    def hide_console(self):
        """隐藏控制台窗口"""
        if self.on_hide_console:
            self.on_hide_console()
        else:
            hide_console_window()
        self.console_visible = False
        logger.info("控制台窗口已隐藏")
        self.update_console_button()

    def toggle_console(self):
        """切换控制台显示/隐藏"""
        if self.console_visible:
            self.hide_console()
        else:
            self.show_console()

    def open_log_folder(self):
        """打开日志文件夹"""
        try:
            log_dir = os.path.abspath(LOG_DIR)
            if os.path.exists(log_dir):
                os.startfile(log_dir)
                logger.info(f"已打开日志文件夹: {log_dir}")
            else:
                messagebox.showwarning("警告", "日志文件夹不存在")
                logger.warning("日志文件夹不存在")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开日志文件夹: {e}")
            logger.error(f"无法打开日志文件夹: {e}")

    def open_latest_log(self):
        """打开最新的日志文件"""
        try:
            log_dir = os.path.abspath(LOG_DIR)
            if not os.path.exists(log_dir):
                messagebox.showwarning("警告", "日志文件夹不存在")
                return

            # 获取所有日志文件
            log_files = [
                f
                for f in os.listdir(log_dir)
                if f.endswith(".log") and os.path.isfile(os.path.join(log_dir, f))
            ]

            if not log_files:
                messagebox.showinfo("信息", "没有找到日志文件")
                return

            # 按修改时间排序，获取最新的
            log_files.sort(
                key=lambda x: os.path.getmtime(os.path.join(log_dir, x)), reverse=True
            )
            latest_log = os.path.join(log_dir, log_files[0])
            os.startfile(latest_log)
            logger.info(f"已打开最新日志文件: {latest_log}")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开日志文件: {e}")
            logger.error(f"无法打开日志文件: {e}")

    def refresh_log_display(self):
        """刷新日志显示"""
        if not self.log_text:
            return

        try:
            log_dir = os.path.abspath(LOG_DIR)
            if not os.path.exists(log_dir):
                return

            # 获取最新的日志文件
            log_files = [
                f
                for f in os.listdir(log_dir)
                if f.endswith(".log") and os.path.isfile(os.path.join(log_dir, f))
            ]

            if not log_files:
                return

            # 按修改时间排序，获取最新的
            log_files.sort(
                key=lambda x: os.path.getmtime(os.path.join(log_dir, x)), reverse=True
            )
            latest_log = os.path.join(log_dir, log_files[0])

            # 读取最后N行日志
            try:
                with open(latest_log, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    # 只显示最后N行
                    recent_lines = (
                        lines[-LOG_DISPLAY_LINES:]
                        if len(lines) > LOG_DISPLAY_LINES
                        else lines
                    )
                    content = "".join(recent_lines)
                    self.log_text.delete(1.0, tk.END)
                    self.log_text.insert(1.0, content)
                    # 滚动到底部
                    self.log_text.see(tk.END)
            except Exception as e:
                logger.error(f"读取日志文件失败: {e}")
        except Exception as e:
            logger.error(f"刷新日志显示失败: {e}")

    def quit_app(self):
        """退出应用程序"""
        if messagebox.askyesno("确认", "确定要退出程序吗？"):
            logger.info("从窗口管理器退出程序")
            if self.on_quit:
                self.on_quit()
            if self.root:
                self.root.quit()
                self.root.destroy()

    def update_console_button(self):
        """更新控制台按钮文本"""
        if hasattr(self, "console_button"):
            if self.console_visible:
                self.console_button.config(text="隐藏控制台")
            else:
                self.console_button.config(text="显示控制台")

    def create_window(self):
        """创建管理窗口"""
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(True, True)

        # 设置窗口图标（如果有的话）
        try:
            # 可以设置自定义图标
            pass
        except:
            pass

        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # 标题
        title_label = ttk.Label(
            main_frame, text="Diablo III 自动启动器", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 10))

        # 控制按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)

        # 控制台按钮
        self.console_button = ttk.Button(
            button_frame, text="显示控制台", command=self.toggle_console
        )
        self.console_button.grid(row=0, column=0, padx=5, sticky=tk.W)

        # 退出按钮
        quit_btn = ttk.Button(button_frame, text="退出程序", command=self.quit_app)
        quit_btn.grid(row=0, column=1, padx=5, sticky=tk.E)

        # 日志显示区域
        log_frame = ttk.LabelFrame(
            main_frame, text=f"最新日志（最后{LOG_DISPLAY_LINES}行）", padding="5"
        )
        log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(
            log_frame, wrap=tk.WORD, width=70, height=20, font=("Consolas", 9)
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 状态栏
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(1, weight=0)

        status_label = ttk.Label(
            status_frame,
            text="程序正在后台运行，监控Diablo III进程",
            foreground="green",
        )
        status_label.grid(row=0, column=0, sticky=tk.W)

        self.runtime_label = ttk.Label(
            status_frame,
            text="运行时间: 00:00:00",
            foreground="blue",
        )
        self.runtime_label.grid(row=0, column=1, sticky=tk.E)

        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 初始化控制台按钮状态
        self.update_console_button()

        # 初始加载日志
        self.refresh_log_display()

        # 定期刷新日志（每30秒）
        self.schedule_log_refresh()

        # 启动运行时间刷新
        self.update_runtime_label()

    def on_closing(self):
        """窗口关闭事件处理"""
        # 最小化到系统托盘而不是关闭
        self.root.iconify()

    def schedule_log_refresh(self):
        """安排定期刷新日志"""
        self.refresh_log_display()
        # 定期刷新
        if self.root:
            self.root.after(LOG_REFRESH_INTERVAL * 1000, self.schedule_log_refresh)

    def show_window(self):
        """显示窗口"""
        if self.root:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()

    def hide_window(self):
        """隐藏窗口"""
        if self.root:
            self.root.withdraw()

    def start(self):
        """启动窗口管理器"""
        try:
            # 在单独的线程中运行GUI
            def run_gui():
                self.create_window()
                self.root.mainloop()

            gui_thread = threading.Thread(target=run_gui, daemon=True)
            gui_thread.start()

            # 等待窗口创建
            timeout = 5
            elapsed = 0
            while self.root is None and elapsed < timeout:
                time.sleep(0.1)
                elapsed += 0.1

            if self.root:
                logger.info("管理窗口已启动")
                return True
            else:
                logger.warning("管理窗口启动超时")
                return False
        except Exception as e:
            logger.error(f"无法启动管理窗口: {e}")
            return False

    def stop(self):
        """停止窗口管理器"""
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
                logger.info("管理窗口已关闭")
            except Exception:
                pass

    def update_runtime_label(self):
        """更新运行时间显示"""
        if not self.runtime_label:
            return

        elapsed = int(time.time() - self.start_time)
        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.runtime_label.config(
            text=f"运行时间: {hours:02d}:{minutes:02d}:{seconds:02d}"
        )

        if self.root:
            self.root.after(1000, self.update_runtime_label)
