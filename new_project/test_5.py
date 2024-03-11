#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/26 17:37
# @Author  : LIU
# @Site    :
# @File    : tes.py
# @Software: PyCharm

# #Desc:
import random
import vthread
import requests

def _easy_json_to_http_form_data(data=None):
    result = ""
    for i in data.keys():
        # print(type(k), k, type(v), v)
        result += f"{i}={data.get(i)}&"
    return result[:-1]

def getCookie():
    # " a=A{random.randint(1, 99)}qwdwdwdww;"
    return f"_bee=p7NVIc3OH5RR4QUCNbzzzBxG551gTapg"
    # return f"a=A{random.randint(1, 99)}qwdwdwdww"


@vthread.pool(10)
def tex():
    api = "http://localhost:8080/fetch"
    url = "https://www.temu.com/g-601099517312310.html"
    # url = "https://www.baidu.com"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="118", "Not;A=Brand";v="8", "Chromium";v="118"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Cookie': getCookie(),
    }

    params = {
        # "top_gallery_url": "https://img.kwcdn.com/product/open/2023-05-10/1683700298370-4a739692d832453c891b4b9e2935fee4-goods.jpeg",
        # "spec_gallery_id": "2000208342",
        # "refer_page_sn": "10005",
        # "refer_source": "0",
        # "freesia_scene": "1",
        # "_oak_freesia_scene": "1",
        # "_oak_rec_ext_1": "Mjc5",
        # "r_idx": "2",
        # "refer_page_el_sn": "200024",
        # "refer_page_name": "home",
        "refer_page_id": "10005_1697076344943_g56k9f8azx",
        # "_x_sessn_id": "tftr16dorg"
    }

    # _res = requests.get(url=api + '?url=https://tls.peet.ws/api/all', headers=headers)
    _res = requests.get(url="https://www.temu.com/g-601099517312310.html?refer_page_id=10005_1697076344943_g56k9f8azx", params=params, headers=headers)
    # _res = requests.get(url=api + '?url=https://www.baidu.com/', headers=headers)
    # print(_res.text)
    print(len(_res.text))
    if "rawData" in _res.text and len(_res.text) > 1000000:
        print("success")
        with open("demo.html", "w", encoding="utf8") as f:
            f.write(_res.text)
    else:
        print("fail")
    # print(_res.status_code)
    # print(_res.text)

if __name__ == '__main__':
    for i in range(10):
        tex()

















