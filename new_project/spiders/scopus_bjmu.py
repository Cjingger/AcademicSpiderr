# !/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import time
import traceback
from datetime import datetime
from ast import literal_eval

from common.common_utils import batch_rpop, client, async_client_proxy
from spiders import async_sql_util
from utils import aioRedisUtil, redisUtil
from common.tools import *
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


class ScopusBjmu():

    def __init__(self, journal, start_year, loop):
        self.journal = journal
        self.start_year = start_year
        self.host = "http://www-scopus-com-443.bjmu.ilibs.cn"
        self.loop = loop
        self.headers = headersChange(f'''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
origin: {self.host}
content-type: application/x-www-form-urlencoded
Host: {self.host.replace('http://', '')}
Pragma: no-cache
referer: {self.host}/search/form.uri?display=advanced
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(106, 111)}.0.0.0 Safari/537.36
''')
        self.coo_dict = literal_eval(bytes.decode(_redis.redis_db.get("scopus_bjmu_cookie"), encoding="utf8"))

    async def product_do_search(self):
        url = "http://www-scopus-com-443.bjmu.ilibs.cn/search/submit/advanced.uri"
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
                resp = await async_client_proxy.post(url, data=form_data, headers=self.headers, follow_redirects=False, cookies=self.coo_dict)
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
                        self.headers["referer"] = resp.headers["location"]
                        # for k, v in resp.cookies.items():
                        #     self.cookies = v
                        return {"sid": sid,
                                "txGid": txGid}
                    else:
                        log.error("resp url err")
                        pass
                else:
                    with open(r"./err_page/err_bjmu_search.html", "w", encoding="utf8") as f:
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
        if not search_data:
            raise Exception("cookie invalid")
        offset = (page - 1) * 200 + 1
        url = f"{self.host}/results/results.uri"
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
            async with sem:
                resp = await async_client_proxy.get(url, params=params, headers=self.headers, follow_redirects=True,
                                              cookies=self.coo_dict)
                if resp.status_code in [200, 201]:
                    # print(resp.text)
                    html = etree.HTML(resp.text)
                    trs = html.xpath('//*[@id="srchResultsList"]/tbody/tr[@class="searchArea"]')
                    result_count = ""
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
                        await aio_redis.aredis_db.lpush(f"scopus:{self.journal}", json.dumps(msg))
                        log.info("redis add success")
                else:
                    with open(r"./err_page/err_bjmu_req_list.html", "w", encoding="utf8") as f:
                        print(resp.text)
                        f.write(resp.text)
                    raise Exception(f"err_status_code {resp.status_code}")
        except Exception as err:
            traceback.print_exc()
            # log.error(str(err))
            pass

    async def async_product_main(self):
        # 最多浏览2k条数据 10页

        # await self.product_get_cookie()
        log.debug(f"collecting {self.journal}")
        search_data = await self.product_do_search()
        if not search_data:
            raise Exception("cookie invalid")
            # sys.exit(1)
        tasks = [self.product_result_list(p + 1, search_data) for p in range(15)]
        await asyncio.gather(*tasks)
        # self.product_get_detail(search_data)

    async def __consumer(self, _data, search_data):
        try:
            # 替换sid
            url = _data["link"]
            log.info(f"target_url {url}")
            try:
                self.headers.pop("cookie")
                self.headers.pop("referer")
            except:
                pass
            async with sem:
                resp = await async_client_proxy.get(url, headers=self.headers, cookies=self.coo_dict)
                if resp.status_code in [200, 201]:
                    # print(resp.text)
                    with open(fr"./err_page/scopus_detail.html", "w", encoding="utf8") as f:
                        f.write(resp.text)
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
            log.error(str(err))
            msg = {
                "article": _data["article"],
                "link": _data["link"],
                "journal": journal,
                "publish_year": publish_year
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
            self.headers["Host"] = "www-scopus-com-443.bjmu.ilibs.cn"
            self.headers["Accept"] = "*/*"
            resp = client.get(url, headers=self.headers)
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
        keys = [bytes.decode(_).replace("scopus:", "") for _ in keys]
        for k in keys:
            log.debug(f"pop key {k}")
            self.journal = k
            search_data = await self.product_do_search()
            p = await aio_redis.aredis_db.pipeline()
            try:
                _datas = await batch_rpop(p, f"scopus:{k}", random.randint(4, 6))
                _datas = _datas[1]
                # log.info(f"datas {_datas}")
                if len(_datas) != 0:
                    _tasks = [self.__consumer(literal_eval(bytes.decode(_data)), search_data) for _data in _datas]
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
            s = ScopusBjmu("", 1, None)
            while True:
                asyncio.get_event_loop().run_until_complete(s.async_consumer_main())
                # del s
        except:
            traceback.print_exc()
            pass

    # @counter()
    def product_main(self):
        try:
            if sys.platform == "win32":
                # asyncio.wait()
                asyncio.get_event_loop().run_until_complete(self.async_product_main())

        except:
            traceback.print_exc()
            sys.exit(1)

def scopus_bjmu_product_main(name):
    while True:
        journal = bytes.decode(_redis.redis_db.lpop(name))
        try:
            start_year = 2018
            scopus = ScopusBjmu(journal, start_year, None)
            scopus.product_main()
            del scopus
            time.sleep(random.randint(2, 4))
        except:
            traceback.print_exc()
            _redis.redis_db.rpush(name, journal)
            continue

