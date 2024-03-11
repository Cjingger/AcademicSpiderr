# !/usr/bin/python3
# -*- coding:utf-8 -*-
import configparser
import argparse
from typing import Union

class Singleton:

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            # 创建新的实例
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, proj, cs: Union[int, int]):
        self.proj = proj
        self.cs = cs
