# !/usr/bin/python3
# -*- coding:utf-8 -*-
import types, typing
from httpx._exceptions import HTTPError
import typing

class _exception(HTTPError):
    def __init__(self, mssg: str, *, request: typing.Optional["Request"]=None) -> None:
        self.request = request
