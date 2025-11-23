"""
后台服务监控模块
实现通用的后台监视逻辑，便于对不同服务进行独立的健康检查
"""

import threading
import logging
from typing import Callable, Optional

logger = logging.getLogger()


class ServiceMonitor:
    """用于监控并在需要时触发重启的后台线程"""

    def __init__(
        self,
        name: str,
        check_func: Callable[[], bool],
        restart_func: Callable[[], bool],
        interval: float,
        stop_event: Optional[threading.Event] = None,
    ):
        self.name = name
        self._check_func = check_func
        self._restart_func = restart_func
        self._interval = interval
        self._stop_event = stop_event or threading.Event()
        self._thread = threading.Thread(
            target=self._run, name=f"{name}Monitor", daemon=True
        )
        self._started = False

    def start(self):
        if self._started:
            return
        logger.info(f"{self.name} 监控线程已启动")
        self._thread.start()
        self._started = True

    def stop(self):
        if not self._started:
            return
        self._stop_event.set()
        self._thread.join(timeout=5)
        logger.info(f"{self.name} 监控线程已停止")

    def _run(self):
        while not self._stop_event.is_set():
            try:
                running = self._check_func()
            except Exception as exc:
                logger.error(f"{self.name} 状态检查失败: {exc}", exc_info=True)
                running = True

            if not running:
                logger.warning(f"{self.name} 未运行，正在尝试恢复...")
                self._attempt_restart()

            if self._stop_event.wait(self._interval):
                break

    def _attempt_restart(self):
        try:
            if self._restart_func():
                logger.info(f"{self.name} 恢复成功")
            else:
                logger.error(f"{self.name} 恢复失败，请检查日志获取更多信息")
        except Exception as exc:
            logger.error(f"{self.name} 恢复过程中出错: {exc}", exc_info=True)
