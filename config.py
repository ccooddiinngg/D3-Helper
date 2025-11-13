"""
配置模块
集中管理所有配置项
"""

import os

# 应用程序配置
APP_NAME = "Diablo III 自动启动器"
APP_VERSION = "1.0.0"

# 进程名称配置
D3_PROCESS_NAME = "Diablo III64.exe"
BATTLE_NET_PROCESS_NAME = "Battle.net.exe"
BATTLE_NET_EXE_PATH = r"C:\Program Files (x86)\Battle.net\Battle.net.exe"

# ROS-BOT
ROS_BOT_PROCESS_NAME = "v1BSlRxgGd3cMhoZ1XsXjC4.exe"
ROS_BOT_EXE_PATH = r"C:\Users\kang_\Downloads\111\Ros-Bot\v1BSlRxgGd3cMhoZ1XsXjC4.exe"  # 请根据实际安装路径修改
ROS_BOT_START_DELAY = 15  # 秒

# 图片文件配置
PLAY_BUTTON_IMAGE = "play.png"
PLAYING_NOW_BUTTON_IMAGE = "playingNow.png"
RADIO_BUTTON_IMAGE = "radiobutton.png"
OK_BUTTON_IMAGE = "ok.png"
CONFIRM_BUTTON_IMAGE = "confirm.png"
OK_BROWSER_BUTTON_IMAGE = "ok_browser.png"

# 图片查找配置
IMAGE_SEARCH_MAX_ATTEMPTS = 10
IMAGE_SEARCH_CONFIDENCE = 0.8
IMAGE_SEARCH_RETRY_DELAY = 0.5

# 监控配置
MONITOR_CHECK_INTERVAL = 10  # 秒
MONITOR_THREAD_CHECK_INTERVAL = 5  # 秒

# 窗口配置
WINDOW_TITLE = f"{APP_NAME} - 管理窗口"
WINDOW_SIZE = "600x500"
LOG_DISPLAY_LINES = 50
LOG_REFRESH_INTERVAL = 30  # 秒

# 日志配置
LOG_DIR = "logs"
LOG_FILE_PREFIX = "diablo3_launcher"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_RETENTION_DAYS = 7

# PyAutoGUI配置
PYAUTOGUI_FAILSAFE = True
PYAUTOGUI_PAUSE = 0.1

# 窗口操作延迟
WINDOW_OPERATION_DELAY = 0.2
CLICK_DELAY = 0.5
BATTLE_NET_START_DELAY = 5  # 秒

# 停止文件
STOP_FILE = "stop_service.txt"

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
