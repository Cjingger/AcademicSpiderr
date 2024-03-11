# !/usr/bin/python3
# -*- coding:utf-8 -*-
# EI buaa 入口
import asyncio
import base64
import sys
import time
import traceback
import datetime
from ast import literal_eval
from hashlib import md5
from math import floor
from spiders import aio_redis
from spiders import async_sql_util
from common.logs import Logs
from common.tools import *
from common.common_utils import async_client, compile_js, batch_rpop, handle_headers, _random_string, local2utc
from utils import redisUtil


from utils.aioSqlUtil import sqlAlchemyUtil

log = Logs()
_redis = redisUtil.RedisUtil()

sem = asyncio.Semaphore(8)

class EIbuaa(object):

    def __init__(self, journal, start_year, _search_type, search_id):
        self.journal = journal
        self.start_year = start_year
        self._search_type = _search_type
        self.host = "www-engineeringvillage-com-443.buaa.ilibs.cn"
        self.headers = headersChange(f'''accept: application/json, text/javascript, */*; q=0.01
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: no-cache
content-type: application/x-www-form-urlencoded
origin: http://{self.host}
pragma: no-cache
referer: http://{self.host}/search/quick.url
X-Forwarded-Host: 171.43.167.39
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(109, 111)}.0.0.0 Safari/537.36
x-newrelic-id: VQQAUldRCRABUVRbAwAGUlcE
x-requested-with: XMLHttpRequest
''')

        self.search_type_map = {
            "Quick": "quicksearch",
            "Advanced": "advancedsearch"
        }
        self._cookie = literal_eval(bytes.decode(_redis.redis_db.get("ei_buaa_cookie"), encoding="utf8"))
        self.cookie_list = ['CONSENTMGR', 'last-domain', 'user_pref_language', 'user_pref_currency', 'userType', 'mediav', 'user_pref_givenName', 'user_pref_cpSelected', 'ABTasty']
        #    f"Hm_lvt_51a9e35dd82f93728da517d1f4c2e{random.randint(30, 88)}c": str(int(time.time()) - random.randint(100, 500)),
    # f"Hm_lpvt_51a9e35dd82f93728da517d1f4c2e{random.randint(22, 99)}c": str(int(time.time()) - random.randint(100, 500)),
        self.async_sql_util = sqlAlchemyUtil()

    async def search_submit(self):
        submit_url = f"http://{self.host}/search/submit.url"
        # self.headers[
        #     "cookie"] = self._coo
        form_data = {
            "usageOrigin": "searchform",
            "usageZone": self.search_type_map[self._search_type],
            "editSearch": "",
            "isFullJsonResult": True,
            "angularReq": True,
            "CID": "searchSubmit",
            "searchtype": self._search_type,
            "origin": "searchform",
            "category": self.search_type_map[self._search_type],
            "section1": "KY",
            "searchWord1": self.journal,
            # "allDb": "9437217",
            # "database": ["1", "1048576", "8388608"],
            "database": "1",
            "yearselect": "yearrange",
            "startYear": str(self.start_year),
            "endYear": str(datetime.datetime.now().year),
            "updatesNo": "1",
            "doctype": "NO-LIMIT",
            "sort": "relevance",
            "searchStartTimestamp": str(int(time.time() * 1e3))
        }
        try:
            async with sem:
                self.headers["Host"] = self.host
                resp = await async_client.post(submit_url, data=form_data, headers=handle_headers(self.headers), follow_redirects=False, cookies=self._cookie)
                coo = ""
                if resp.status_code in [301, 302]:
                    for k, v in resp.cookies.items():
                        coo += f"{k}={v}; "
                        self._cookie[k] = v
                    # coo = coo.strip("; ")
                    return {
                        "location": resp.headers["location"],
                    }
                else:
                    with open(r".err_page/err_EI_submit.html", "w", encoding="utf8") as f:
                        f.write(resp.text)
                    raise Exception(f"err_status_code {resp.status_code}")
        except Exception as e:
            # log.error(str(e))
            traceback.print_exc()
            return

    async def search_quick_index(self):
        ret = await self.search_submit()
        if not ret:
            raise Exception("search submit err")
        # quick_search_url = "http://" + self.host + ret["location"] if "http" in str(ret["location"]) else ret["location"]
        quick_search_url = ret["location"]
        self.headers["referer"] = f'http://{self.host}/search/quick.url'
        self.headers["x-newrelic-id"] = "VQQAUldRCRAFUFFQBwgCUQ=="
        log.debug(f"quick_search_url {quick_search_url}")
        search_id = re.findall(r"^.*?SEARCHID=(.*?).*?$", str(quick_search_url), re.I)[0]
        try:
            async with sem:
                resp = await async_client.get(quick_search_url, headers=self.headers, follow_redirects=True, cookies=self._cookie)
                if resp.status_code in [200, 201]:
                    if "Warning" in resp.text:
                        raise Exception("response fail")
                    # update cookie
                    for k, v in resp.cookies.items():
                        self._cookie[k] = v
                    resp_data = resp.json()
                    # 判断初始页面是不是每页100展示
                    if int(resp_data["pagenav"]["resultscount"]) > 100 and len(resp_data["results"]) < 100:
                        await self.search_quick_index_max_page(search_id, resp_data["pagenav"]["resultscount"])
                    else:
                        total_page = floor(int(resp_data["pagenav"]["resultscount"]) / 100) + 1
                        for r in resp_data["results"]:
                            try:
                                title = re.findall(r'^.*?</span> (.*?)"$', r["title"], re.I)[0]
                            except:
                                title = r["title"].strip()
                            try:
                                doc_id = r["doc"]["docid"]
                                doc_index = str(r["doc"]["hitindex"])
                                link = f"http://{self.host}/app/doc/?docid={doc_id}&pageSize=100&index={doc_index}&searchId={search_id}&resultsCount={str(resp_data['pagenav']['resultscount'])}&usageZone=resultslist&usageOrigin=searchresults&searchType=Quick"
                                pub_year = int(r["yr"])
                                d = {
                                    "title": title,
                                    "link": link,
                                    "pub_year": pub_year,
                                    "result_count": resp_data["pagenav"]["resultscount"]
                                }
                                await aio_redis.aredis_db.lpush(f"EI:buaa:{self.journal}", json.dumps(d))
                                log.info("redis add success")
                            except:
                                pass
                        # 遍历每页
                        # for p in range(total_page):
                        #     if p == total_page - 1:
                        #         return
                        #     await self.search_quick_page(search_id, resp_data["pagenav"]["resultscount"], p)
                        # tasks = [self.search_quick_page(search_id, resp_data["pagenav"]["resultscount"], p) for p in range(total_page)]
                        # await asyncio.gather(*tasks)
                else:
                    with open(r"./err_page/err_EI_search_quick_index.html", "w", encoding="utf8") as f:
                        f.write(resp.text)
                    raise Exception(f"err_status_code {resp.status_code}")
        except Exception as e:
            traceback.print_exc()
            # log.error(str(e))
            pass

    async def search_quick_index_max_page(self, search_id, result_count):
        url = f"https://www.engineeringvillage.com/search/results/quick.url"
        params = {
            "pageSizeVal": "100",
            "SEARCHID": search_id,
            "sortsort": "relevance",
            "sortdir": "dw",
            "angularReq": "true",
            "isFullJsonResult": "false",
            "usageOrigin": "searchresults",
            "usageZone": "resultsperpagebottom",
            # "_": str(int(time.time()) * 1e3)
        }
        # self.headers["cookie"] = self._coo
        self.headers["referer"] = f'http://{self.host}/search/quick.url'
        self.headers["content-type"] = "application/json"
        self.headers["x-newrelic-id"] = "VQQAUldRCRAFUFFQBwgCUQ=="
        try:
            resp = await async_client.get(url, headers=self.headers, follow_redirects=True, params=params, cookies=self._cookie)
            if resp.status_code in [200, 201]:
                # update cookie
                for k, v in resp.cookies.items():
                    self._cookie[k] = v
                resp_data = resp.json()
                total_page = floor(int(resp_data["pagenav"]["resultscount"]) / 100) + 1
                for r in resp_data["results"]:
                    try:
                        title = re.findall(r'^.*?</span> (.*?)"$', r["title"], re.I)[0]
                        doc_id = resp_data["doc"]["docid"]
                        doc_index = str(resp_data["doc"]["hitindex"])
                        link = f"http://{self.host}/app/doc/?docid={doc_id}&pageSize=100&index={doc_index}&searchId={search_id}&resultsCount={str(resp_data['pagenav']['resultscount'])}&usageZone=resultslist&usageOrigin=searchresults&searchType=Quick"
                        pub_year = int(resp_data["yr"])
                        d = {
                            "title": title,
                            "link": link,
                            "pub_year": pub_year,
                            "result_count": result_count
                        }
                        await aio_redis.aredis_db.lpush(f"EI:buaa:{self.journal}", json.dumps(d))
                        log.info("redis add success")
                    except:
                        pass
                # 遍历每页
                # tasks = [self.search_quick_page(search_id, resp_data["pagenav"]["resultscount"], p) for p in range(total_page)]
                # await asyncio.gather(*tasks)
            else:
                with open(r"./err_page/err_ei_search_quick_max.html", "w", encoding="utf8") as f:
                    f.write(resp.text)
                raise Exception(f"err_status_code {resp.status_code}")
        except Exception as e:
            log.error(str(e))
            pass

    async def search_quick_page(self, search_id, result_count, page: int):
        if page == 0:
            return
        log.debug(f"{self.journal} page {page}")
        count = (page + 1) * 100 + 1
        url = "https://www.engineeringvillage.com/search/results/quick.url"
        if count == 101:
            self.headers["referer"] = f"http://{self.host}/search/quick.url?SEARCHID={search_id}&COUNT={str(count)}&usageOrigin=&usageZone="
        else:
            self.headers["referer"] = f"http://{self.host}/search/quick.url?SEARCHID={search_id}&COUNT={str(count - 100)}&usageOrigin=&usageZone="
        try:
            params = {
                "navigator": "NEXT",
                "SEARCHID": search_id,
                "database": "1",
                "angularReq": "true",
                "isFullJsonResult": "false",
                "usageOrigin": "searchresults",
                "COUNT": str(count),
                "usageZone": "nextpage",
                "_": str(int(time.time()) * 1e3 - random.randint(100, 240) * 1e4)
            }
            self.headers["Host"] = self.host
            self.headers["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
            self.headers["Content-Type"] = "application/json"
            self.headers["Proxy-Connection"] = "keep-alive"
            async with sem:
                resp = await async_client.get(url, headers=handle_headers(self.headers), follow_redirects=True, params=params, cookies=self._cookie)
                if resp.status_code in [200, 201]:
                    # update cookie
                    for k, v in resp.cookies.items():
                        self._cookie[k] = v
                    # with open("err_EI_quick_search_page.html", "w") as f:
                    #     f.write(resp.text)
                    if "System Error" in resp.text:
                        log.error("search error")
                        return
                    log.info(resp.json())
                    resp_data = resp.json()
                    for r in resp_data["results"]:
                        try:
                            title = re.findall(r'^.*?</span> (.*?)"$', r["title"], re.I)[0]
                            doc_id = resp_data["doc"]["docid"]
                            doc_index = str(resp_data["doc"]["hitindex"])
                            link = f"http://{self.host}/app/doc/?docid={doc_id}&pageSize=100&index={doc_index}&searchId={search_id}&resultsCount={str(resp_data['pagenav']['resultscount'])}&usageZone=resultslist&usageOrigin=searchresults&searchType=Quick"
                            pub_year = int(resp_data["yr"])
                            d = {
                                "title": title,
                                "link": link,
                                "pub_year": pub_year,
                                "result_count": result_count
                            }
                            await aio_redis.aredis_db.lpush(f"EI:buaa:{self.journal}", json.dumps(d))
                            log.info("redis add success")
                        except:
                            pass
                else:
                    with open(r"./err_page/err_EI_buaa_search.html", "w", encoding="utf8") as f:
                        f.write(resp.text)
                    raise Exception(f"err_status_code {resp.status_code}")
        except Exception as e:
            traceback.print_exc()
            # log.error(str(e))
            pass

    async def search_advance(self):
        pass

    async def search_get_js(self, **kwargs):
        url = "https://www.engineeringvillage.com/rest/public/newrelic.js"
        try:
            self.headers.pop("x-newrelic-id")
            self.headers.pop("x-requested-with")
        except:
            pass
        _referer = f"http://{self.host}/app/doc/?docid={kwargs['doc_id']}&pageSize=100&index=4&searchId={kwargs['search_id']}&resultsCount={str(kwargs['results_count'])}&usageZone=resultslist&usageOrigin=searchresults&searchType={self._search_type}"
        try:
            resp = await async_client.get(url, headers=self.headers, cookies=self._cookie)
            if resp.status_code in [200, 201]:
                resp_js = resp.content.decode("utf8")
                agent_id = re.findall(r'^.*?agentID:"(.*?)".*?$', resp_js)[0]
                account_id = re.findall(r'^.*?accountID:"(.*?)".*?$', resp_js)[0]
                trust_key = re.findall(r'^.*?trustKey:"(.*?)".*?$', resp_js)[0]
                xpid = re.findall(r'^.*?xpid:"(.*?)".*?$', resp_js)[0]
                license_key = re.findall(r'^.*?licenseKey:"(.*?)".*?$', resp_js)[0]
                application_id = re.findall(r'^.*?applicationID:"(.*?)".*?$', resp_js)[0]
                return {"agent_id": agent_id,
                        "account_id": account_id,
                        "trust_key": trust_key,
                        "xpid": xpid,
                        "license_key": license_key,
                        "application_id": application_id}
            else:
                raise Exception(f"err_status_code {resp.status_code}")

        except:
            # traceback.print_exc()
            return

    async def search_get_script(self, **kwargs):
        span_id = compile_js.call("s", 16)
        trace_id = compile_js.call("s", 32)
        c = int(time.time() * 1e3)
        try:
            trace_parent = compile_js.call("generateTraceContextParentHeader", trace_id, span_id)
            trace_state = compile_js.call("generateTraceContextStateHeader", span_id, c,
                                          kwargs["account_id"], kwargs["agent_id"], kwargs["trust_key"])
            return {
                "trace_id": trace_id,
                "span_id": span_id,
                "trace_parent": trace_parent,
                "trace_state": trace_state,
                "c": c
            }
        except Exception as e:
            log.error(str(e))
            return

    async def search_doc_detail(self, search_id, search_data):
        _url = f"http://{self.host}/rest/doc"
        doc_id = re.findall(r"^.*?docid=(.*?)&.*?$", search_data["link"])[0]
        results_count = re.findall(r"^.*?resultsCount=(\d+)&.*?$", search_data["link"])[0]
        params = {
            "docid": doc_id,
            "pageSize": "100",
            "docIndex": str(93),
            "searchId": search_id,
            "resultsCount": str(results_count),
            "usageZone": "resultslist",
            "usageOrigin": "searchresults",
            "searchType": self._search_type
        }
        result_count_comma = ""
        for i, letter in enumerate(str(search_data["result_count"])):
            _ = f",{letter}" if i == 2 else letter
            result_count_comma += _
        if has_val(self._cookie, "EISESSION"):
            session_id = self._cookie["EISESSION"].split(" ")[0].split("_")[1]
            _datetime = local2utc(datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.000+0000")
            json_data = {"searchId": search_id,
                         "sessionId": session_id,
                         # "userid": "27c5aa2bdc7b4becbb4836ed51e3b5d5",
                         "databasemask": str(random.randint(1, 8)),
                         "searchtype": "Quick",
                         "savedate": _datetime,
                         "accessdate": _datetime,
                         "emailalert": "Off",
                         "saved": "Off",
                         "visible": "On",
                         "resultscount": str(results_count),
                         "language": "NO-LIMIT",
                         "startYear": self.start_year,
                         "endYear": str(datetime.datetime.now().year),
                         "autostem": "on",
                         "sort": "relevance",
                         "sortdir": "dw",
                         "displayquery": f"(({self.journal}) WN AB)",
                         "intermediatequery": f"(({self.journal}) WN AB)",
                         "documenttype": "NO-LIMIT",
                         "treatmentType": "NO-LIMIT",
                         "refinestack": f"all@All@ALL@true@0~(({self.journal}) WN AB)~(({self.journal}) WN AB)QqQ<>",
                         "searchWord1": self.journal,
                         "section1": "AB",
                         "alertLatest": "NO",
                         "userDatabasemask": 0,
                         "pageSize": 0,
                         "fetchNavigator": True,
                         "highlightingEnabled": True,
                         "refineSearch": False,
                         "includeOutputKeys": False,
                         "sortOption": {"display": None,
                                        "name": None,
                                        "value": None,
                                        "selected": False,
                                        "field": "relevance",
                                        "defaultdirection": None,
                                        "direction": "dw"},
                         "navDataCount": 0,
                         "serialnumber": 50,
                         "databasedisplay": "Compendex & Inspec",
                         "alertOwner": False,
                         "searchHistoryRecording": True,
                         "resultsCountWithCommas": gen_num(int(results_count)),
                         "offset": 0}
            js_data = await self.search_get_js(doc_id=doc_id, search_id=search_id, results_count=results_count)
            # 若请求失败,使用默认值进行后续请求
            if js_data:
                config_data = await self.search_get_script(account_id=js_data["account_id"], agent_id=js_data["agent_id"],
                                                     trust_key=js_data["trust_key"])
            else:
                js_data = {
                    "account_id": "1273121",
                    "agent_id": "1588758972",
                    "trust_key": "2038175",
                    "xpid": "VQQAUldRCRABUVRbAwAGUlcE",
                    "license_key": "2f90a42388"
                }
                config_data = await self.search_get_script(account_id=js_data["account_id"], agent_id=js_data["agent_id"], trust_key=js_data["trust_key"])
            self.headers["traceparent"] = config_data["trace_parent"]
            self.headers["tracestate"] = config_data["trace_state"]
            self.headers["content-type"] = "application/json"
            self.headers["accept"] = "application/json"
            newrelic_byte = bytes(
                '{"v":[0,1],"d":{"ty":"Browser","ac":"%s","ap":"%s","id":"%s","tr":"%s","ti":%d,"tk":"%s"}}' % (
                js_data["account_id"], js_data["agent_id"], config_data["span_id"], config_data["trace_id"],
                int(config_data["c"]), js_data["trust_key"]), encoding="utf8")
            newrelic = bytes.decode(base64.b64encode(newrelic_byte, ))
            self.headers["newrelic"] = newrelic
            try:
                async with sem:
                    resp = await async_client.post(_url, headers=self.headers, follow_redirects=True, params=params, json=json_data, cookies=self._cookie)
                    if resp.status_code in [200, 201]:
                        _data = resp.json()
                        # log.info(_data)
                        publish_year = int(_data["PAGE"]["PAGE-RESULTS"]["PAGE-ENTRY"][0]["EI-DOCUMENT"]["DOCUMENTPROPERTIES"]["YR"])
                        data_from = "EI"
                        keyword = ""
                        is_qikan = 1
                        article = _data["PAGE"]["PAGE-RESULTS"]["PAGE-ENTRY"][0]["EI-DOCUMENT"]["DOCUMENTPROPERTIES"]["TI"]
                        area = ""
                        _is_ch = 1
                        email = ""
                        name = ""
                        for au in _data["PAGE"]["PAGE-RESULTS"]["PAGE-ENTRY"][0]["EI-DOCUMENT"]["AUS"]["AU"]:
                            if "EMAIL" in list(au.keys()):
                                email = au["EMAIL"]
                                name = au["NAME"]
                                break
                            else:
                                continue
                        classify = ""
                        url = f"https://www.engineeringvillage.com/app/doc/?docid={doc_id}"
                        try:
                            abstract = _data["PAGE"]["PAGE-RESULTS"]["PAGE-ENTRY"][0]["EI-DOCUMENT"]["DOCUMENTPROPERTIES"]["AB"]
                        except:
                            abstract = ""
                        discipline = ""
                        subdiscipline = ""
                        conference = ""
                        journal = self.journal
                        _is_ch = is_ch(email)
                        m = md5()
                        m.update(url.encode("utf8"))
                        _id = m.hexdigest()
                        if email == "":
                            return
                        data = {
                            "id": _id,
                            "author": name,
                            "time": publish_year,
                            "data_from": data_from,
                            "keyword": keyword,
                            "is_qikan": is_qikan,
                            "article": article,
                            "abstract": abstract,
                            "email": email,
                            "area": area,
                            "is_ch": _is_ch,
                            "classify": classify,
                            "url": url,
                            "discipline": discipline,
                            "subdiscipline": subdiscipline,
                            "conference": conference,
                            "journal": journal,
                            "create_time": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
                        }
                        print(data)
                        await async_sql_util.create_table(data_from)
                        await async_sql_util.insert_data(data_from, data)
                    else:
                        with open(r"./err_page/err_ei_doc_detail.html", "w", encoding="utf8") as f:
                            f.write(resp.text)
                        raise Exception(f"err_status_code {resp.status_code}")
            except Exception as e:
                log.error(f"search_doc_detail_err {str(e)}")
                d = {
                    "title": search_data["title"],
                    "link": search_data["link"],
                    "pub_year": search_data["pub_year"],
                    "result_count": search_data["result_count"],
                    "journal": journal
                }
                await aio_redis.aredis_db.lpush(f"EI:{self.journal}", json.dumps(d))
        else:
            raise Exception("cookie no EISESSION")

    def product_main(self):
        try:
            asyncio.get_event_loop().run_until_complete(self.search_quick_index())
        except Exception as e:
            raise Exception(e)
            pass

    async def async_consumer_main(self):
        # await self.product_get_cookie()
        keys = await aio_redis.aredis_db.keys(pattern='*EI:buaa*')
        keys = [bytes.decode(_).replace("EI:buaa", "") for _ in keys]
        for k in keys:
            log.debug(f"pop key {k}")
            self.journal = k
            p = await aio_redis.aredis_db.pipeline()
            try:
                _datas = await batch_rpop(p, f"EI:buaa{k}", random.randint(4, 6))
                _datas = _datas[1]
                if len(_datas) != 0:
                    ret = await self.search_submit()
                    if not ret:
                        raise Exception("search submit err")
                    search_id = re.findall(r"^.*?SEARCHID=(.*?).*?$", str(ret["location"]), re.I)[0]
                    _tasks = [self.search_doc_detail(search_id, literal_eval(bytes.decode(_data))) for _data in _datas]
                    await asyncio.gather(*_tasks)
                else:
                    log.info("生产者队列已取完")
                    return
            except:
                return
            finally:
                p.pipeline().close()

    @staticmethod
    def consumer_main():
        try:
            while True:
                ei_buaa = EIbuaa("", 2018, "Quick", "")
                asyncio.get_event_loop().run_until_complete(ei_buaa.async_consumer_main())
                del ei_buaa
        except Exception as e:
            traceback.print_exc()
            if "search submit err" in str(e):
                sys.exit(1)
            pass


def EI_buaa_product_main(start_year):
    name = "journals:EI"
    search_type = "Quick"
    search_id = ""
    while True:
        journal = bytes.decode(_redis.redis_db.lpop(name))
        try:
            EI = EIbuaa(journal, start_year, search_type, search_id)
            EI.product_main()
            del EI
            time.sleep(random.randint(2, 4))
        except:
            traceback.print_exc()
            _redis.redis_db.rpush(name, journal)
            sys.exit(1)