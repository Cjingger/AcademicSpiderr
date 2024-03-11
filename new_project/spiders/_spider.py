# !/usr/bin/python3
# -*- coding:utf-8 -*-
import asyncio
import sys
import traceback


class _Spider(object):

    def __init__(self, journal: str, start_year: int):
        self.journal = journal
        self.start_year = start_year
        self.host = ""

    async def do_search(self, *args):
        pass

    async def do_search_page(self):
        pass

    async def result_list(self, *args):
        pass

    async def async_product_main(self):
        pass

    def product_main(self):
        try:
            asyncio.get_event_loop().run_until_complete(self.async_product_main())
        except Exception as e:
            raise Exception(e)

    async def __consumer(self, **kwargs):
        pass

    async def async_consumer_main(self):
        pass

    @staticmethod
    def consumer_main():
        try:
            while True:
                s = _Spider("", 1)
                asyncio.get_event_loop().run_until_complete(s.async_consumer_main())
                del s
        except:
            traceback.print_exc()
            sys.exit(1)
