"""
日志配置模块
提供日志系统的初始化和配置功能
"""

import logging
import os
import sys
from datetime import datetime
from config import (
    LOG_DIR,
    LOG_FILE_PREFIX,
    LOG_FORMAT,
    LOG_DATE_FORMAT,
)


def setup_logging():
    """配置日志系统，同时输出到控制台和文件"""
    # 创建logs目录（如果不存在）
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # 生成日志文件名（带时间戳）
    log_filename = os.path.join(
        LOG_DIR,
        f"{LOG_FILE_PREFIX}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    )

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
