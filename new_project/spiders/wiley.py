# !/usr/bin/python3
# -*- coding:utf-8 -*-
import random

from _spider import _Spider
from common.common_utils import async_client_proxy, handle_headers
from common.logs import Logs
from common.tools import headersChange

log = Logs()

class Wiley(_Spider):

    def __init__(self, journal: str, start_year: int):
        super().__init__(journal, start_year)
        self.host = "onlinelibrary.wiley.com"
        self.headers = headersChange(f'''accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
cache-control: no-cache
pragma: no-cache
referer: https://{self.host}/
sec-ch-ua: "Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(106, 113)}.0.0.0 Safari/537.36
''')
        self.cookies = {
    "lit_osano": "v1",
    "userRandomGroup": "54",
    "rskxRunCookie": "0",
    "rCookie": "3spph27v8w6f0unwgpcc07lhzpkqnh",
    "SERVER": "WZ6myaEXBLHQFyoOjAxmIQ==",
    "__cf_bm": "m2qqmszEXMKr_0XjkoO4.juimtIlHrkeOPzYYo4aXk4-1684815340-0-AWALruLBbo6+d3GlfDXkQWn4kobJnP/aqWseB/WMkh5VJEM/Sv1o11uUtb9ugyHm9DmaNDOX5F0sI72TzKMBLqKUQLEyHAyB9MFdCb4/NFid3EFj1xGCsq333BoyHkqI0/ye7XgsThDwMS6IDhl7nZeZED+zeS+4YsEU+ZvAjNBx",
    "MACHINE_LAST_SEEN": "2023-05-22T21%3A17%3A47.881-07%3A00",
    "JSESSIONID": "64052CAF7A2D697033BA8E0707A76F10",
    "AUTO_SIGNIN": "PJFFcTcBPaFwxHBgsgi4po+1Kx8oo3zBtpnxlFLLIEqUToFtr/jLpOZUSWF3k4xVPOVcFLQDO7EiBOJaAUBu9Nk1D7GfPXiqdhQ687Rr8/8WJO7SVSMMcT5lq3r12eifs6/ctaQowDD1ux8MJwTAcg==",
    "PLUID": "aJMmpZnTQXuS4CsQXa/72PSQBh0=",
    "MAID": "vOLwrABCGQ+nS9d3Mi6AeQ==",
    "MAID_DISC": "8055666546",
    "_ga_9C4T5P6PP6": "GS1.1.1684815470.1.0.1684815470.60.0.0",
    "lastRskxRun": "1684815471730"
}

    async def do_advanced(self):
        advanced_url = f"https://onlinelibrary.wiley.com/search/advanced"
        try:
            resp = await async_client_proxy.get(advanced_url, headers=handle_headers(self.headers), cookies=self.cookies)
            if resp.status_code in [200, 201]:
                for k, v in resp.cookies.items():
                    self.cookies[k] = v

        except Exception as e:
            log.error(str(e))
            return


    async def do_search(self, *args):
        search_url = "https://onlinelibrary.wiley.com/action/doSearch"
