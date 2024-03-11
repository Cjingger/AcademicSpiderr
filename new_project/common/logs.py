# !/usr/bin/ven/python3
# -*- encoding: utf-8 -*-
from loguru import logger
import os, time


class Logs:

    def __init__(self):
        self._basePath = os.path.abspath('')
        self.logPath = os.path.join(self._basePath, '../logs')
        now_time = time.strftime("%Y-%m-%d", time.localtime())
        logger.add(f"logs/runtime{now_time}.log", rotation="200MB", encoding="utf-8", enqueue=True, compression="zip",
                   retention="1 week", level="INFO")

    def setLevel(self, level):
        logger.level(level)

    def info(self, message: str):
        logger.info(message)

    def debug(self, message: str):
        logger.debug(message)

    def error(self, message: str):
        logger.error(message)

    def exception(self, message: str):
        logger.exception(message)