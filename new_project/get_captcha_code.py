# !/usr/bin/python3
# -*- coding:utf-8 -*-
import base64
import time
import traceback

from lxml import etree
import uuid
from common.common_utils import async_client_proxy, handle_headers
import asyncio
import random
from common.tools import headersChange

cookie = {
    "Hm_lvt_0a2c428cbb4ffc8d6b830fcaf9c5757b": "1682670500",
    "Hm_lpvt_0a2c428cbb4ffc8d6b830fcaf9c5757b": "1682671101"
}

async def get_captcha_img():
    headers = headersChange(f'''Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Host: www.vziliao.com
Pragma: no-cache
Referer: http://www.vziliao.com/Account/Login?ReturnUrl=%2F
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(98, 114)}.0.0.0 Safari/537.36
X-Requested-With: XMLHttpRequest
''')
    url = f"http://www.vziliao.com/Account/Captcha?{str(int(time.time() * 1e3))}"
    try:
        async with asyncio.Semaphore(30):
            resp = await async_client_proxy.get(url, headers=handle_headers(headers), cookies=cookie)
            if resp.status_code in [200, 201]:
                for k, v in resp.cookies.items():
                    cookie[k] = v
                captcha_encrypt = resp.json()["data"]["captchaEncryption"]
                print("captcha_encrypt", captcha_encrypt)
                base64_str = resp.json()["data"]["imgBase64"]
                img_data = base64.urlsafe_b64decode(base64_str)
                with open(fr"../static/img/captcha{uuid.uuid4()}.png", "wb") as f:
                    f.write(img_data)
                    print("图片保存成功")
            else:
                raise Exception(f"status code err {resp.status_code}")
    except Exception as e:
        print(e)

async def async_get_captcha_img_main():
    tasks = [get_captcha_img() for i in range(30)]
    await asyncio.gather(*tasks)

def get_captcha_img_main():
    for j in range(3):
        asyncio.get_event_loop().run_until_complete(async_get_captcha_img_main())

if __name__ == '__main__':
    get_captcha_img_main()