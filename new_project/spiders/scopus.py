# !/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import time
import traceback
from datetime import datetime
from ast import literal_eval
from urllib.parse import *
import openpyxl
from httpx import TransportError

from common.common_utils import batch_rpop, client, handle_headers, async_client_proxy
from spiders import async_sql_util
from utils import aioRedisUtil, redisUtil
from common.tools import *
from utils.aioSqlUtil import sqlAlchemyUtil
import httpx
from lxml import etree
from common.logs import Logs
from hashlib import md5
from common._filter import filterD
from aredis import pipeline
import csv
import asyncio
from functools import wraps

log = Logs()
# redis = RedisUtil()
aio_redis = aioRedisUtil.AioRedisUtil()
_redis = redisUtil.RedisUtil()
sem = asyncio.Semaphore(50)

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


class Scopus():

    def __init__(self, journal, start_year):
        self.journal = journal
        self.start_year = start_year
        self.host = "www.scopus.com"
        self.headers = headersChange(f'''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
origin: https://{self.host}
content-type: application/x-www-form-urlencoded
Pragma: no-cache
referer: https://{self.host}/search/form.uri?display=advanced
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(106, 111)}.0.0.0 Safari/537.36
''')
        self.coo_dict = literal_eval(bytes.decode(_redis.redis_db.srandmember("scopus_cookie"), encoding="utf8"))
        self.ct = "China"
    async def product_do_search(self):
        url = f"https://{self.host}/search/submit/advanced.uri"
        # 先只检索国内期刊
        form_data = {
            "origin": "searchadvanced",
            "authorSelectionPageURL": "/search/form/selectionpage.uri?renderType=authorRenderType",
            "affilSelectionPageURL": "/search/form/selectionpage.uri?renderType=affilRenderType",
            "popupComplete": "1",
            "clickedLink": "",
            "editSaveSearch": "",
            "src": "s",
            "edit": "",
            "authorTab": "",
            "basicTab": "",
            "affiliationTab": "",
            "searchfield": 'SRCTITLE(%s)  AND ( LIMIT-TO ( AFFILCOUNTRY , "{%s}" ) ) AND PUBYEAR > {%s}' % (self.journal, self.ct, str(self.start_year))
        }
        try:
            async with sem:
                resp = await async_client_proxy.post(url, data=form_data, headers=handle_headers(self.headers), follow_redirects=False, cookies=self.coo_dict)
                if resp.status_code in [200, 201, 301, 302]:
                    if "error" in resp.text:
                        with open(r"./err_page/err_scopus_search.html", "w", encoding="utf8") as f:
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
                        self.headers["referer"] = resp.headers["location"]

                        return {"sid": sid,
                                "txGid": txGid}
                    else:
                        log.error("resp url err")
                        return
                else:
                    with open(r"./err_page/err_scopus_search.html", "w", encoding="utf8") as f:
                        f.write(resp.text)
                    raise Exception(f"err_status_code {resp.status_code}")
        except Exception as e:
            # log.error(str(e))
            traceback.print_exc()
            return

    async def product_result_list(self, page, search_data):
        '''
        根据条件检索结果列表
        :return:
        '''

        log.info(f"page {page}")
        if not search_data:
            raise Exception("cookie invalid")
        offset = (page - 1) * 200 + 1
        # url = f"https://{self.host}/results/results.uri"
        # params = {
        #     "sort": "plf-f",
        #     "src": "s",
        #     # "st1": self.journal,
        #     "sid": search_data["sid"],
        #     "sot": "a",
        #     "sdt": "a",
        #     # "cluster": f'scoaffilctry,"{self.ct}",t',
        #     "sl": "40",
        #     "s": f"SRCTITLE({self.journal}) AND PUBYEAR &gt; {str(self.start_year)}",
        #     # "cl": "t",
        #     # "offset": str(offset),
        #     "origin": "searchadvanced",
        #     # "origin": "resultslist",
        #     # "ss": "plf-f",
        #     # "ws": "r-f",
        #     # "ps": "r-f",
        #     # "cs": "r-f",
        #     # "cc": "10",
        #     "editSaveSearch":"",
        #     "txGid": search_data["txGid"]
        # }

        url = "https://www.scopus.com/api/documents/search"
        form_data = {
    "documentClassificationEnum": "primary",
    "query": f"SRCTITLE({self.journal}) AND PUBYEAR &gt; {str(self.start_year)}",
    "sort": "plf-f",
    "itemcount": 200,
    "offset": offset,
    "showAbstract": True
}
        header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    # "Content-Length": "153",
    "Content-Type": "application/json",
    # "Cookie": "scopus.machineID=25243E53106C2093B987BC98D77774C9.i-0814adc94e84aa4fb; Scopus-usage-key=enable-logging; AT_CONTENT_COOKIE=\"FEATURE_DOCUMENT_RESULT_MICRO_UI:0,\"; at_check=true; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; scopus_key=vVahIFdq1OCP8Tmgc5pkbtkH; SCSessionID=FB8EC44E3D7BFF4C70E7C9D34955FE49.i-0303190e939c95411; scopusSessionUUID=1a31b703-e88f-4808-a; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB1266C57D290062E8BE6AF6EA23F771B56B4860156BA94A00B00B67AAB671BCEB28278FC278415EC1A7924B82E83258A304DD5E65C6811DF8D35751647B4EB8AF4; _cfuvid=ZzE2kSZ6By9vLsa90CqtcTQhkfDnG.Y6JnEBQAC1uIM-1695776136280-0-604800000; __cfruid=b2b6728e5660b50a41a2ca42925f68b36e4a0092-1695776139; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=-2121179033%7CMCIDTS%7C19628%7CMCMID%7C34680833624956583821395009355630351846%7CMCAAMLH-1696380950%7C9%7CMCAAMB-1696380950%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1695783350s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.3.0%7CMCCIDH%7C-709609818; SCOPUS_JWT=eyJraWQiOiJjYTUwODRlNi03M2Y5LTQ0NTUtOWI3Zi1kMjk1M2VkMmRiYmMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyMTM5NzY1NjAiLCJkZXBhcnRtZW50SWQiOiI3NTA4OSIsImlzcyI6IlNjb3B1cyIsImluc3RfYWNjdF9pZCI6IjUzMTk1IiwicGF0aF9jaG9pY2UiOmZhbHNlLCJpbmR2X2lkZW50aXR5IjoiUkVHIiwiZXhwIjoxNjk1NzgxNDg3LCJpYXQiOjE2OTU3ODA1ODcsImFuYWx5dGljc19pbmZvIjp7ImFjY291bnRJZCI6IjUzMTk1IiwidXNlcklkIjoiYWU6MjEzOTc2NTYwIiwiYWNjZXNzVHlwZSI6ImFlOlJFRzpTSElCQk9MRVRIOklOU1Q6U0hJQkJPTEVUSCIsImFjY291bnROYW1lIjoiRnVkYW4gVW5pdmVyc2l0eSJ9LCJkZXBhcnRtZW50TmFtZSI6IklQX0Z1ZGFuIFVuaXZlcnNpdHkiLCJpbnN0X2FjY3RfbmFtZSI6IkZ1ZGFuIFVuaXZlcnNpdHkiLCJzdWJzY3JpYmVyIjp0cnVlLCJ3ZWJVc2VySWQiOiIyMTM5NzY1NjAiLCJpbnN0X2Fzc29jX21ldGhvZCI6IlNISUJCT0xFVEgiLCJnaXZlbl9uYW1lIjoiQ2h1biIsImFjY291bnROdW1iZXIiOiJDMDAwMDUzMTk1IiwiYXVkIjoiU2NvcHVzIiwibmJmIjoxNjk1NzgwNTg3LCJmZW5jZXMiOltdLCJpbmR2X2lkZW50aXR5X21ldGhvZCI6IiIsImluc3RfYXNzb2MiOiJJTlNUIiwibmFtZSI6IkNXIiwidXNhZ2VQYXRoSW5mbyI6IigyODk0ODQzMSxVfDc1MDg5LER8NTMxOTUsQXwxMTgyLFN8NSxQfDEsUEwpKFNDT1BVUyxDT058ZDI2OWExZTc2ZDZlYTA0NjllNWFiYTI1NTg0YzM5MjA4N2ZiZ3hycWEsU1NPfFJFR19TSElCQk9MRVRILEFDQ0VTU19UWVBFKSIsInByaW1hcnlBZG1pblJvbGVzIjpbXSwiYXV0aF90b2tlbiI6ImQyNjlhMWU3NmQ2ZWEwNDY5ZTVhYmEyNTU4NGMzOTIwODdmYmd4cnFhIiwiZmFtaWx5X25hbWUiOiJXYW5nIn0.sCaDY2I2oq3E5QA1p82gzsJp9zkfvM-fbltX1-cBskcQKF2LLnXwXlUVvffQ2MD068wCTgD4lQlnALaMoE_bC6Mz0END_KEljnZ-5Zs5wJ-v8QPm1FkD0EK1WytUFwOYUyjRJMUOJrJ-tIR6Afy_OwAcWrm9ASXO22FcX9rQEeOr2dXAidkJk9ZpD37nwH6SPEKtVG5YujHY2Aw-IkhAnWqNvDCNwQA67Tua9f8gRcSHoYcRn8Wy4gOppHw-XTgGfXBKSQvy7__zGmhUzHFWJcNchRm4v5RWurcZSG1pnApX2ie-px0Thw19EG1SwW8ZJD_FM2XOwdxeMll0A6JUFQ; __cf_bm=2ns.286FlJ30m6844mVt2nX3yJ_MlSa1XYZK2pz4Vks-1695780589-0-AYr+zvdj2YEHAvGVjeNsw6qBfYFCB2xIJwBE+/LXHOYIV0nEyqHU9dzVQtBg0sdgwZfQCh71FkwizjdWnQTdcWw=; mbox=PC#7d9013e9a2d44f5a8424c63462963dbb.32_0#1759025435|session#3693bac658704a7e849bb12bbe55230b#1695782495; JSESSIONID=9A0B6CE37DB5F17FCFBDA36A9E546A3D; s_sess=%20s_cpc%3D0%3B%20c7%3Dcountry%253Dchina%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dsc%25253Aresults%25253Adocuments%252C7%252C7%252C2003%252C726%252C931%252C1920%252C1080%252C1%252CL%3B%20s_sq%3D%3B%20s_ppv%3Dsc%25253Aresults%25253Adocuments%252C100%252C6%252C35190%252C1055%252C931%252C1920%252C1080%252C1%252CP%3B%20c21%3Dsrctitle%2528computer%2529%2520and%2520pubyear%2520%2526gt%253B%25202018%3B%20e13%3D%253A7%3B%20c13%3Ddate%2520%2528newest%2529%3B%20e41%3D1%3B; s_pers=%20v8%3D1695780819016%7C1790388819016%3B%20v8_s%3DMore%2520than%252030%2520days%7C1695782619016%3B%20c19%3Dsc%253Aresults%253Adocuments%7C1695782619018%3B%20v68%3D1695780661419%7C1695782619023%3B",
    "Origin": "https://www.scopus.com",
    "Pragma": "no-cache",
    "Referer": "https://www.scopus.com/results/results.uri?sort=plf-f&src=s&sid=83fef8f5654ef79296e36f957ccc7e02&sot=a&sdt=a&sl=40&s=SRCTITLE%28computer%29+AND+PUBYEAR+%26gt%3B+2018&origin=searchadvanced&editSaveSearch=&txGid=63b9c3b179c02b3110dff45279b1c799&sessionSearchId=83fef8f5654ef79296e36f957ccc7e02&limit=200",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
        try:
            try:
                self.headers.pop("origin")
                self.headers.pop("content-type")
            except:
                pass
            async with sem:
                resp = await async_client_proxy.post(url, json=form_data, headers=handle_headers(header), follow_redirects=True,
                                              cookies=self.coo_dict)


                if resp.status_code in [200, 201]:
                    try:
                        trs = resp.json()["items"]
                    except:
                        with open(r"./err_page/err_scopus_req_list_200.html", "w", encoding="utf8") as f:
                            f.write(resp.text)
                        raise Exception("獲取數據失敗")
                    try:
                        result_count = resp.json()["metadata"]["totalCount"]
                        _page = filterD(data_from="scopus", result_count=result_count)
                    except:
                        pass
                    for tr in trs:
                        article = tr["title"]
                        params = {
                                    "eid":tr["eid"],
                                    "origin":"resultslist",
                                    "sort":"plf-f",
                                    "src":"s",
                                    "sid":search_data["sid"],
                                    "sot":"a",
                                    "sdt":"a",
                                    "s":f"SRCTITLE({self.journal}) AND PUBYEAR &gt; {str(self.start_year)}",
                                    "sl":"40",
                                    "sessionSearchId":search_data["sid"]
                                }
                        link = "https://www.scopus.com/record/display.uri?" + urlencode(params)
                        try:
                            journal = self.journal
                        except:
                            journal = self.journal
                        publish_year = tr["pubYear"]
                        try:
                            author = tr["authors"][0]["preferredName"]

                        except:
                            # 无作者信息 略过此条数据
                            log.debug("no author")
                            continue
                        # log.info(f"{article} {link} {journal} {publish_year}")
                        msg = {
                            "article": article,
                            "link": link,
                            "journal": journal,
                            "publish_year": publish_year
                        }
                        await aio_redis.aredis_db.lpush(f"scopus:{self.journal}", json.dumps(msg))
                        log.info("redis add success")
                else:
                    with open(r"./err_page/err_scopus_req_list.html", "w", encoding="utf8") as f:
                        f.write(resp.text)
                    raise Exception(f"err_status_code {resp.status_code}")
        except Exception as err:
            traceback.print_exc()
            pass

    async def async_product_main(self):
        # 最多浏览2k条数据 10页

        # await self.product_get_cookie()
        log.debug(f"collecting {self.journal}")
        # search_data = await self.product_do_search()
        s = f"{random.randint(1, 9)}{random.randint(1, 9)}{random.randint(1, 9)}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{random.randint(1, 9)}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}"[
            0::random.randint(2, 8)]
        m = md5()
        m.update(s.encode("utf8"))
        sid = m.hexdigest()
        search_data = {
            "sid": sid,
            "txGid": f"234d4224abae15f639dcb44ba90f8932"}
        if not search_data:
            raise Exception("cookie invalid")
        tasks = [self.product_result_list(p + 1, search_data) for p in range(10)]
        await asyncio.gather(*tasks)
        # self.product_get_detail(search_data)

    async def __consumer(self, _data):
        try:
            # 替换sid
            url = _data["link"]
            # log.info(f"target_url {url}")
            try:
                self.headers.pop("cookie")
                self.headers.pop("referer")
            except:
                pass
            async with sem:
                resp = await async_client_proxy.get(url, headers=handle_headers(self.headers), cookies=self.coo_dict)
                if resp.status_code in [200, 201]:
                    # print(resp.text)
                    # update cookie
                    for k, v in resp.cookies.items():
                        self.coo_dict[k] = v
                    html = etree.HTML(resp.text)
                    try:
                        author = html.xpath('//*[@id="profileleftinside"]/div[2]/div/p/text()')[1].split("; ")[
                            0].strip()
                    except:
                        log.debug("no author")
                        return
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
                    classify = ""
                    discipline = ""
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
            pass
        except TransportError as err:
            # traceback.print_exc()
            log.error(f"httpx err {str(err)}")
            msg = {
                "article": _data["article"],
                "link": _data["link"],
                "journal": _data["journal"],
                "publish_year": _data["publish_year"]
            }
            await aio_redis.aredis_db.lpush(f"scopus:{self.journal}", json.dumps(msg))
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
            self.headers["Host"] = "api-scopus-com-s.bjmu.ilibs.cn"
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

    async def load_index_data_redis(self):
        pass

    async def async_consumer_main(self):
        # await self.product_get_cookie()
        keys = await aio_redis.aredis_db.keys(pattern='*scopus:*')
        if len(keys) == 0:
            raise Exception("生产者队列已取完")
        keys = [bytes.decode(_).replace("scopus:", "") for _ in keys]
        for k in keys:
            log.debug(f"pop key {k}")
            self.journal = k
            # search_data = await self.product_do_search()
            # if not search_data:
            #     raise Exception("cookie invalid")
            p = await aio_redis.aredis_db.pipeline()
            try:
                _datas = await batch_rpop(p, f"scopus:{k}", random.randint(7, 10))
                _datas = _datas[1]
                # log.info(f"datas {_datas}")
                if len(_datas) != 0:
                    _tasks = [self.__consumer(literal_eval(bytes.decode(_data))) for _data in _datas]
                    await asyncio.gather(*_tasks)
                    # time.sleep(random.randint(1, 2))
                else:
                    log.info("生产者队列已取完")
                    return
            except:
                raise Exception()
            finally:
                p.pipeline().close()

    @staticmethod
    def consumer_main():
        global s
        try:
            while True:
                s = Scopus("", 1)
                asyncio.get_event_loop().run_until_complete(s.async_consumer_main())
                del s
        except:
            traceback.print_exc()
            sys.exit(1)

    # @counter()
    def product_main(self):
        try:
            if sys.platform == "win32":
                # asyncio.wait()
                asyncio.get_event_loop().run_until_complete(self.async_product_main())
        except Exception as e:
            raise Exception(e)

def scopus_product_main():
    name = "journals:scopus"
    while True:
        journal = bytes.decode(_redis.redis_db.lpop(name))
        try:
            start_year = 2018
            scopus = Scopus(journal, start_year)
            scopus.product_main()
            del scopus
            time.sleep(random.randint(2, 4))
        except:
            traceback.print_exc()
            _redis.redis_db.rpush(name, journal)
            sys.exit(1)


