"""
停止后台服务的辅助脚本
运行此脚本可以安全地停止Diablo III自动启动器
"""

import os
import sys


def stop_service():
    """创建停止文件来停止后台服务"""
    stop_file = "stop_service.txt"

    # 创建停止文件
    try:
        with open(stop_file, "w") as f:
            f.write("stop")
        print(f"已创建停止文件: {stop_file}")
        print("后台服务将在下次检查时停止（最多等待10秒）")
        print("如果服务没有停止，请检查任务管理器中的进程")
    except Exception as e:
        print(f"无法创建停止文件: {e}")
        sys.exit(1)


if __name__ == "__main__":
    stop_service()
