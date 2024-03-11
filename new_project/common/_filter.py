# !/usr/bin/python3
# -*- coding:utf-8 -*-
from math import floor
from typing import Union


def filterD(**kwargs) -> Union[int, dict]:
    result_count = kwargs["result_count"]
    if kwargs["data_from"] == "scopus":
        if result_count <= 200:
            return 1
        #仅可查看前2000记录
        elif result_count > 2000:
            return 10
        else:
            page = (result_count // 200) + 1
            return {
                "page": page,
                "result_count": result_count
            }
    elif kwargs["data_from"] == "EI":
        if result_count <= 100:
            return 1
        else:
            page = floor(result_count / 100) + 1
            return {
                "page": page,
                "result_count": result_count
            }