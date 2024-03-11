# !/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import time
import traceback
from datetime import datetime
from ast import literal_eval
import openpyxl
from common.common_utils import batch_rpop, client, async_client, handle_headers
from spiders import async_sql_util
from utils import aioRedisUtil, redisUtil
from common.tools import *
from utils.aioSqlUtil import sqlAlchemyUtil
import httpx
from lxml import etree
from common.logs import Logs
from hashlib import md5
from aredis import pipeline
import csv
import asyncio
from functools import wraps

log = Logs()
# redis = RedisUtil()
aio_redis = aioRedisUtil.AioRedisUtil()
_redis = redisUtil.RedisUtil()
sem = asyncio.Semaphore(12)

def counter():
    def _counter(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            co = 0
            ret = func(*args, **kwargs)
            co += 1
            return ret

        return wrapper

    return _counter


class ScopusBuaa():

    def __init__(self, journal, start_year):
        self.journal = journal
        self.start_year = start_year
        self.host = "www-scopus-com-443.buaa.ilibs.cn"
        self.headers = headersChange(f'''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
origin: http://{self.host}
content-type: application/x-www-form-urlencoded
host: {self.host}
Pragma: no-cache
Referer: http://{self.host}/search/form.uri?display=advanced
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(106, 111)}.0.0.0 Safari/537.36
''')
        # self.coo_dict = literal_eval(bytes.decode(_redis.redis_db.srandmember("scopus_buaa_cookie"), encoding="utf8"))
        self.coo_dict = {
    "scopus.machineID": "A20466A44DC2EEDA5CB415FC81CA9C9C.i-04472da4219fdf484",
    "s_ecid": "MCMID%7C55361425866728196619070173904931477911",
    "s_vi": "[CS]v1|31884F19C91130C3-40001AE857F00723[CE]",
    "scopus_key": "dE9YZfuvojKuHg9j58d26waZ",
    "Hm_lvt_51a9e35dd82f93728da517d1f4c2e76c": "1682391435,1683181527",
    "Scopus-usage-key": "enable-logging",
    "AT_CONTENT_COOKIE": "\"FEATURE_DOCUMENT_RESULT_MICRO_UI:1,\"",
    "at_check": "true",
    "AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg": "1",
    "XKToken": "JlBp8vSBMtBYIGDA3xLgLQ==",
    "SCSessionID": "A4FC97C065B9E122861598670D1FD004.i-07ddb05fd878bd213",
    "scopusSessionUUID": "28dde530-293e-4eab-a",
    "AWSELB": "CB9317D502BF07938DE10C841E762B7A33C19AADB1E9818582EE83AA73A5966FD8DBE1EBC34742E673FD4BA56052D3F217CF3ACAD72CFBB76ECCEBE0946FCCE2B9E27272A30B8407F5CD70EAB18DA5F6B8CBCC96C8",
    "mbox": "PC#ef7991411ae046e284b6ffc3fd626485.32_0#1746850304|session#90ade477db584b6e946d8ce4ab6c3e19#1683625363",
    "s_pers": "%20v8%3D1683623520104%7C1778231520104%3B%20v8_s%3DLess%2520than%25201%2520day%7C1683625320104%3B%20c19%3Dsc%253Asearch%253Adocument%2520results%7C1683625320110%3B%20v68%3D1683623492854%7C1683625320121%3B",
    "s_sess": "%20s_cpc%3D0%3B%20e78%3Dsearchword1%2520%253F%2520ky%2520contains%2520analyst%3B%20s_ppvl%3Dev%25253Ainit%25253Aload%252C100%252C100%252C968%252C920%252C968%252C1920%252C1080%252C1%252CL%3B%20s_sq%3D%3B%20s_ppv%3Dev%25253Ainit%25253Aload%252C95%252C21%252C4307%252C557%252C968%252C1920%252C1080%252C1%252CL%3B%20c21%3Dtitle-abs-key%2528analytical%2520chemistry%2529%3B%20e13%3Dtitle-abs-key%2528analytical%2520chemistry%2529%253A1%3B%20c13%3Ddate%2520%2528newest%2529%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B",
    "AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg": "-1033042250%7CMCIDTS%7C19487%7CMCMID%7C33209082601175792228185959192814920841%7CMCAID%7CNONE%7CMCOPTOUT-1683630723s%7CNONE%7CvVersion%7C5.3.0%7CMCAAMLH-1683623439.051%7C11%7CMCAAMB-1683623519%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCSYNCSOP%7C411-19494",
    "__cf_bm": "IrYpUCyg0Ql6oOXNhHrXsexSWMYZZyjpaSRdwJNVhDU-1683624980-0-AcNUcrv+nKNgyAzIpWWLbZHZRLgBchXarrw4YV2BVN7Qz7znkBAiCOTwlkA91PgDoNrhWR33EBjc1l4kHhIcyIY=",
    "__cfruid": "01891d586da6f124809cfd047b512358e5434a99-1683624980",
    "SCOPUS_JWT": "eyJraWQiOiJjYTUwODRlNi03M2Y5LTQ0NTUtOWI3Zi1kMjk1M2VkMmRiYmMiLCJhbGciOiJSUzI1NiJ9.eyJhbmFseXRpY3NfaW5mbyI6eyJhY2NvdW50SWQiOiI1NjgzNyIsImFjY291bnROYW1lIjoiQmVpaGFuZyBVbml2ZXJzaXR5IiwiYWNjZXNzVHlwZSI6ImFlOkFOT046OklOU1Q6SVAiLCJ1c2VySWQiOiJhZToyMjk3ODAwIn0sImRlcGFydG1lbnROYW1lIjoiSVBfQmVpaGFuZyBVbml2ZXJzaXR5Iiwic3ViIjoiMjI5NzgwMCIsImluc3RfYWNjdF9uYW1lIjoiQmVpaGFuZyBVbml2ZXJzaXR5Iiwic3Vic2NyaWJlciI6dHJ1ZSwiZGVwYXJ0bWVudElkIjoiODAxNzIiLCJpc3MiOiJTY29wdXMiLCJpbnN0X2FjY3RfaWQiOiI1NjgzNyIsImluc3RfYXNzb2NfbWV0aG9kIjoiSVAiLCJwYXRoX2Nob2ljZSI6ZmFsc2UsImF1ZCI6IlNjb3B1cyIsIm5iZiI6MTY4MzYyNDk4MCwiZmVuY2VzIjpbXSwiaW5kdl9pZGVudGl0eV9tZXRob2QiOiIiLCJpbnN0X2Fzc29jIjoiSU5TVCIsImluZHZfaWRlbnRpdHkiOiJBTk9OIiwidXNhZ2VQYXRoSW5mbyI6IigyMjk3ODAwLFV8ODAxNzIsRHw1NjgzNyxBfDExODIsU3w1LFB8MSxQTCkoU0NPUFVTLENPTnxmOTg1NTIxZDM4NzU0NzQ1YjM1YWIxNTRhMDkwMWE3NDZmOGNneHJxYSxTU098QU5PTl9JUCxBQ0NFU1NfVFlQRSkiLCJleHAiOjE2ODM2MjU4ODAsImF1dGhfdG9rZW4iOiJmOTg1NTIxZDM4NzU0NzQ1YjM1YWIxNTRhMDkwMWE3NDZmOGNneHJxYSIsImlhdCI6MTY4MzYyNDk4MH0.Ey_rE2ppbeO_PXyI75ZZa8RA4t5QPP59eENtaFuAVwkdxuTSqK37loSO7a19FFnGyuLdrZ0Q3IlxC2GrxJjlVJE1bCd9sUIYIGX9Fl8m2IxnvJY7XzebzcXX1x3viYP6dHoC93CTAzI3eg7u8NiAyizm8i2NxkK7FnTZlpiKEINQhg9PD6Qwa4ODmaDftcZpkHQGpEtziCekBHSZz0WCKpqlTzaVo72nlf-qdI1Jwev0vnchnh1NcRHQ409TuQhRTWRV3CwPxtHt20wzqFejwyqqAF40lX9WkJ4-RCTzYrLbrRMU49FJ0qrca2-V39Nbi7PoANykshSv9OZTZ6oIJQ"
}
    async def product_do_search(self):
        url = f"http://{self.host}/search/submit/advanced.uri"
        form_data = {
            "origin": "searchadvanced",
            "authorSelectionPageURL": "/search/form/selectionpage.uri?renderType=authorRenderType",
            "affilSelectionPageURL": "/search/form/selectionpage.uri?renderType=affilRenderType",
            "popupComplete": "1",
            "clickedLink": "",
            "editSaveSearch": "",
            "src": "",
            "edit": "",
            "authorTab": "",
            "basicTab": "",
            "affiliationTab": "",
            "searchfield": "SRCTITLE(%s) AND PUBYEAR > {%s}" % (self.journal, str(self.start_year))
        }
        try:
            async with sem:
                resp = await async_client.post(url, data=form_data, headers=handle_headers(self.headers), follow_redirects=False, cookies=self.coo_dict)
                if resp.status_code in [200, 201, 301, 302]:
                    if "error" in resp.text:
                        with open(r"./err_page/err_buaa_search.html", "w", encoding="utf8") as f:
                            f.write(resp.text)
                        raise Exception(f"resp error {resp.status_code}")
                    if "超时" or "timeout" or "time out" in resp.text:
                        log.error("使用超时 请重新打开")
                        return
                    if "txGid=" in resp.headers["location"]:
                        # txGid = re.findall(r'<input type="hidden" id="txGid" value="(.*?).i.*?', resp.text, re.M)[0]
                        txGid = re.findall(r"^.*?txGid=(.*?)$", resp.headers["location"], re.M)[0]
                        s = f"{random.randint(1, 9)}{random.randint(1, 9)}{random.randint(1, 9)}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{random.randint(1, 9)}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}"[
                            0::random.randint(2, 8)]
                        m = md5()
                        m.update(s.encode("utf8"))
                        sid = m.hexdigest()
                        self.headers["Referer"] = resp.headers["location"]
                        for k, v in resp.cookies.items():
                            self.coo_dict[k] = v
                        return {"sid": sid,
                                "txGid": txGid}
                    else:
                        log.error(f"resp url err {resp.status_code}")
                        return
                else:
                    with open(r"./err_page/err_buaa_search.html", "w", encoding="utf8") as f:
                        f.write(resp.text)
                    raise Exception(f"err_status_code {resp.status_code}")
        except Exception as e:
            # traceback.print_exc()
            log.error(str(e))
            return

    async def product_result_list(self, page, search_data):
        '''
        根据条件检索结果列表
        :return:
        '''

        log.info(f"page {page}")
        offset = (page - 1) * 200 + 1
        url = f"http://{self.host}/results/results.uri"
        params = {
            "sort": "plf-f",
            "src": "s",
            "st1": self.journal,
            # "sid": "606658e370bd9c92e19beab2ef33063b",
            "sid": search_data["sid"],
            "sot": "a",
            "sdt": "a",
            "sl": "51",
            "s": f"SRCTITLE({self.journal}) AND PUBYEAR > {str(self.start_year)}",
            "cl": "t",
            "offset": str(offset),
            "origin": "resultslist",
            "ss": "plf-f",
            "ws": "r-f",
            "ps": "r-f",
            "cs": "r-f",
            "cc": "10",
            "txGid": search_data["txGid"]
        }
        try:
            try:
                self.headers.pop("origin")
                self.headers.pop("content-type")
            except:
                pass
            # print("req_header", self.headers)
            async with sem:
                resp = await async_client.get(url, params=params, headers=handle_headers(self.headers), follow_redirects=True,
                                              cookies=self.coo_dict)
                if resp.status_code in [200, 201]:
                    html = etree.HTML(resp.text)
                    trs = html.xpath('//*[@id="srchResultsList"]/tbody/tr[@class="searchArea"]')
                    try:
                        result_count = int(html.xpath('//*[@id="searchResFormId"]/div[1]/div/header/h1/span[@class="resultsCount"]')[0].replace(",", ""))
                    except:
                        pass
                    for tr in trs:
                        article = tr.xpath('./td[1]/a/text()')[0]
                        link = tr.xpath('./td[1]/a/@href')[0]
                        journal = tr.xpath('./td[4]/a/text()')[0]
                        publish_year = int(tr.xpath('./td[3]/span/text()')[0])
                        try:
                            author = tr.xpath('./td[2]/span/a[1]/text()')[0]

                        except:
                            # 无作者信息 略过此条数据
                            log.debug("no author")
                            continue
                        log.info(f"{article} {link} {journal} {publish_year}")
                        msg = {
                            "article": article,
                            "link": link,
                            "journal": journal,
                            "publish_year": publish_year
                        }
                        await aio_redis.aredis_db.lpush(f"scopus_buaa:{self.journal}", json.dumps(msg))
                        log.info("redis add success")
                else:
                    with open(r"./err_page/err_buaa_req_list.html", "w", encoding="utf8") as f:
                        f.write(resp.text)
                    raise Exception(f"err_status_code {resp.status_code}")
        except Exception as err:
            log.error(str(err))
            pass

    async def async_product_main(self):
        # 最多浏览2k条数据 10页

        # await self.product_get_cookie()
        log.debug(f"collecting {self.journal}")
        search_data = await self.product_do_search()
        if not search_data:
            raise Exception("cookie invalid")
        tasks = [self.product_result_list(p + 1, search_data) for p in range(10)]
        await asyncio.gather(*tasks)
        # self.product_get_detail(search_data)

    async def __consumer(self, _data):
        try:
            # 替换sid
            url = _data["link"]
            log.info(f"target_url {url}")
            try:
                self.headers.pop("cookie")
                self.headers.pop("Referer")
            except:
                pass
            async with sem:
                resp = await async_client.get(url, headers=handle_headers(self.headers), cookies=self.coo_dict)
                if resp.status_code in [200, 201]:
                    # print(resp.text)
                    for k, v in resp.cookies.items():
                        self.coo_dict[k] = v
                    html = etree.HTML(resp.text)
                    author = html.xpath('//*[@id="profileleftinside"]/div[2]/div/p/text()')[1].split("; ")[
                        0].strip()
                    try:
                        _email = html.xpath('//*[@class="corrAuthSect"]/a[2]/@href')[0].strip()
                        if _email:
                            _email = self.decode_email(_email.replace('/cdn-cgi/l/email-protection#', ''))
                        else:
                            log.debug("no email")
                            return
                    except:
                        log.debug("html no email")
                        return
                    # self.consumer_doc_detail(_data["link"])
                    _is_ch = is_ch(_email)
                    article = _data["article"]
                    publish_year = _data["publish_year"]
                    data_from = "scopus"
                    keyword = ""
                    area = ""
                    classify = "Computer Science"
                    discipline = "Computer Science"
                    subdiscipline = ""
                    conference = ""
                    journal = _data["journal"]
                    is_qikan = 1
                    m = md5()
                    m.update(_data["link"].encode("utf8"))
                    _id = m.hexdigest()
                    data = {
                        "id": _id,
                        "author": author,
                        "time": publish_year,
                        "data_from": data_from,
                        "keyword": keyword,
                        "is_qikan": is_qikan,
                        "article": article,
                        "abstract": "",
                        "email": _email,
                        "area": area,
                        "is_ch": _is_ch,
                        "classify": classify,
                        "url": _data["link"],
                        "discipline": discipline,
                        "subdiscipline": subdiscipline,
                        "conference": conference,
                        "journal": journal,
                        "create_time": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                    }
                    # print(data)
                    print("-" * 50)
                    await async_sql_util.create_table(data_from)
                    await async_sql_util.insert_data(data_from, data)
                elif "denied" in resp.text:
                    log.error("Be denied")
                    sys.exit(1)
                else:
                    with open(r"./err_page/err_scopus_detail.html", "w", encoding="utf8") as f:
                        f.write(resp.text)
                    raise Exception(f"err_status_code {resp.status_code}")
        except TypeError as e:
            log.error(str(e))
            pass
        except Exception as err:
            traceback.print_exc()
            # log.error(str(err))
            msg = {
                "article": _data["article"],
                "link": _data["link"],
                "journal": _data["journal"],
                "publish_year": _data["publish_year"]
            }
            await aio_redis.aredis_db.lpush(f"scopus_buaa:{self.journal}", json.dumps(msg))
            pass

    def decode_email(self, _code):
        a = self.r(_code, 0)
        o = ""
        for i in range(2, len(_code), 2):
            l = self.r(_code, i) ^ a
            o += chr(l)
        return o

    def r(self, _code, t):
        return parse_int(_code[t:t + 2], 16)

    def consumer_doc_detail(self, link):
        eid = re.findall(r"^.*?eid=(.*?)&.*?$", link, re.I)[0]
        log.info(f"eid {eid}")
        url = f"http://api-scopus-com-s.bjmu.ilibs.cn/doc-details/documents/{eid}"
        try:
            self.headers["Referer"] = link
            self.headers["Origin"] = f"http://{self.host}"
            self.headers["Host"] = "www-scopus-com-443.buaa.ilibs.cn"
            self.headers["Accept"] = "*/*"
            resp = client.get(url, headers=handle_headers(self.headers))
            if resp.status_code in [200, 201]:
                print(resp.json())
            else:
                with open(r"./err_page/err_doc_detail.html", "w", encoding="utf8") as f:
                    f.write(resp.text)
                raise Exception(f"err_status_code {resp.status_code}")
        except:
            traceback.print_exc()
            pass

    async def async_consumer_main(self):
        # await self.product_get_cookie()
        keys = await aio_redis.aredis_db.keys(pattern='*scopus_buaa*')
        keys = [bytes.decode(_).replace("scopus_buaa", "").replace(":", "") for _ in keys]
        for k in keys:
            log.debug(f"pop key {k}")
            self.journal = k
            # search_data = await self.product_do_search()
            # if not search_data:
            #     raise Exception("cookie invalid")
            p = await aio_redis.aredis_db.pipeline()
            try:
                _datas = await batch_rpop(p, f"scopus:{k}", random.randint(6, 10))
                _datas = _datas[1]
                # log.info(f"datas {_datas}")
                if len(_datas) != 0:
                    _tasks = [self.__consumer(literal_eval(bytes.decode(_data))) for _data in _datas]
                    await asyncio.gather(*_tasks)
                else:
                    log.info("生产者队列已取完")
                    return
            except:
                traceback.print_exc()
                raise Exception()
            finally:
                p.pipeline().close()

    @staticmethod
    def consumer_main():
        global s
        try:
            s = ScopusBuaa("", 1)
            while True:
                asyncio.get_event_loop().run_until_complete(s.async_consumer_main())
                # del s
        except:
            traceback.print_exc()
            asyncio.get_event_loop().close()
            sys.exit(1)

    # @counter()
    def product_main(self):
        try:
            if sys.platform == "win32":
                # asyncio.wait()
                asyncio.get_event_loop().run_until_complete(self.async_product_main())
        except Exception as e:
            # traceback.print_exc()
            raise Exception(e)


def scopus_buaa_product_main():
    name = "journals:scopus"
    while True:
        journal = bytes.decode(_redis.redis_db.lpop(name))
        try:
            start_year = 2018
            scopus = ScopusBuaa(journal, start_year)
            scopus.product_main()
            del scopus
            time.sleep(random.randint(2, 4))
        except:
            traceback.print_exc()
            _redis.redis_db.rpush(name, journal)
            sys.exit(1)

