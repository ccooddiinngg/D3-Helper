"""
日志配置模块
提供日志系统的初始化和配置功能
"""

import logging
import os
import sys
from datetime import datetime, timedelta
from config import (
    LOG_DIR,
    LOG_FILE_PREFIX,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
    LOG_RETENTION_DAYS,
)


def _get_log_file_path():
    """构建固定日志文件路径"""
    return os.path.join(LOG_DIR, f"{LOG_FILE_PREFIX}.log")


def _prune_old_entries(log_path):
    """仅保留最近LOG_RETENTION_DAYS天的日志"""
    if not os.path.exists(log_path):
        return

    cutoff = datetime.now() - timedelta(days=LOG_RETENTION_DAYS)
    retained_lines = []

    try:
        with open(log_path, "r", encoding="utf-8") as log_file:
            for line in log_file:
                timestamp_str = line.split(" - ", 1)[0].strip()
                try:
                    entry_time = datetime.strptime(timestamp_str, LOG_DATE_FORMAT)
                    if entry_time >= cutoff:
                        retained_lines.append(line)
                except ValueError:
                    # 如果无法解析时间戳，保留该行以避免丢失关键信息
                    retained_lines.append(line)
    except (OSError, UnicodeDecodeError):
        # 如果读取失败，保留原日志文件
        return

    try:
        with open(log_path, "w", encoding="utf-8") as log_file:
            log_file.writelines(retained_lines)
    except OSError:
        pass


def setup_logging():
    """配置日志系统，同时输出到控制台和文件"""
    # 创建logs目录（如果不存在）
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_filename = _get_log_file_path()
    _prune_old_entries(log_filename)

    # 配置日志格式
    log_format = LOG_FORMAT
    date_format = LOG_DATE_FORMAT

    # 配置根日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 清除现有的处理器
    logger.handlers.clear()

    # 文件处理器（保存到文件）
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(log_format, date_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # 控制台处理器（输出到控制台，保留彩色输出）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    # 控制台格式不包含时间戳（因为代码中已经手动添加了）
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger, log_filename


def get_logger():
    """获取配置好的日志记录器"""
    logger = logging.getLogger()
    if not logger.handlers:
        # 如果日志记录器还没有配置，则进行初始化
        logger, _ = setup_logging()
    return logger
