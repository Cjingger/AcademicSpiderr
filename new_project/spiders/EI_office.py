# !/usr/bin/python3
# -*- coding:utf-8 -*-
# engineeringvillage官网
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
from common.common_utils import compile_js, batch_rpop, local2utc, handle_headers, async_client
from utils import redisUtil

import httpx
import execjs
from asyncio import Semaphore

from utils.aioSqlUtil import sqlAlchemyUtil

_timeout = httpx.Timeout(timeout=20, connect=15, read=16)
_limit = httpx.Limits(max_connections=200, max_keepalive_connections=150)
log = Logs()
_redis = redisUtil.RedisUtil()

sem = asyncio.Semaphore(20)

class EIOffice(object):

    def __init__(self, journal, start_year, _search_type, search_id):
        self.journal = journal
        self.start_year = start_year
        self._search_type = _search_type
        self.search_id = search_id
        self.headers = headersChange(f'''accept: application/json, text/javascript, */*; q=0.01
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: no-cache
content-type: application/x-www-form-urlencoded
origin: https://www.engineeringvillage.com
pragma: no-cache
referer: https://www.engineeringvillage.com/search/quick.url
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(109, 111)}.0.0.0 Safari/537.36
x-newrelic-id: VQQAUldRCRABUVRbAwAGUlcE
x-requested-with: XMLHttpRequest
''')
        self.host = "www.engineeringvillage.com"

        self.search_type_map = {
            "Quick": "quicksearch",
            "Advanced": "advancedsearch"
        }
        self._cookie = literal_eval(bytes.decode(_redis.redis_db.srandmember("EI_cookie"), encoding="utf8"))

        self.async_sql_util = sqlAlchemyUtil()
        self.cy = "china"

    # async def search_submit(self):
    #     submit_url = "https://www.engineeringvillage.com/search/submit.url"
    #     form_data = {
    #         "usageOrigin": "searchform",
    #         "usageZone": self.search_type_map[self._search_type],
    #         "editSearch": "",
    #         "isFullJsonResult": True,
    #         "angularReq": True,
    #         "CID": "searchSubmit",
    #         "searchtype": self._search_type,
    #         "origin": "searchform",
    #         "category": self.search_type_map[self._search_type],
    #         "section1": "KY",
    #         "searchWord1": self.journal,
    #         "boolean1": "AND",
    #         "section2": "CO",
    #         "searchWord2": self.cy,
    #         # "allDb": "9437217",
    #         "allDb": "8388609",
    #         "database": ["1", "8388608"],
    #         # "database": "1",
    #         "yearselect": "yearrange",
    #         "startYear": str(self.start_year),
    #         "endYear": str(datetime.datetime.now().year),
    #         "updatesNo": "1",
    #         "language": "NO-LIMIT",
    #         "doctype": ["NO-LIMIT", "BK", "JA"],
    #         "sort": "relevance",
    #         "searchStartTimestamp": str(int(time.time() * 1e3))
    #     }
    #     try:
    #         async with sem:
    #             resp = await async_client.post(submit_url, data=form_data, headers=self.headers, follow_redirects=False, cookies=self._cookie)
    #             coo = ""
    #             if resp.status_code in [301, 302]:
    #                 for k, v in resp.cookies.items():
    #                     coo += f"{k}={v}; "
    #                     self._cookie[k] = v
    #                 coo = coo.strip("; ")
    #                 return {
    #                     "location": resp.headers["location"],
    #                     "cookies": coo
    #                 }
    #             else:
    #                 log.error(f"err search status code {resp.status_code}")
    #                 return
    #     except Exception as e:
    #         log.error(str(e))
    #         return

    async def search_submit(self, start_year: int):
        endYear = str(start_year + 1) if start_year != datetime.datetime.now().year else start_year
        submit_url = "https://www.engineeringvillage.com/search/submit.url"
        # form_data = {
        #     "usageOrigin": "searchform",
        #     "usageZone": self.search_type_map[self._search_type],
        #     "editSearch": "",
        #     "isFullJsonResult": True,
        #     "angularReq": True,
        #     "CID": "searchSubmit",
        #     "searchtype": self._search_type,
        #     "origin": "searchform",
        #     "category": self.search_type_map[self._search_type],
        #     "section1": "KY",
        #     "searchWord1": self.journal,
        #     "boolean1": "AND",
        #     "section2": "CO",
        #     "searchWord2": self.cy,
        #     # "allDb": "9437217",
        #     "allDb": "35",
        #     "database": ["1", "2"],
        #     # "database": "1",
        #     "yearselect": "yearrange",
        #     "startYear": str(start_year),
        #     "endYear": str(endYear),
        #     "updatesNo": "1",
        #     "language": "NO-LIMIT",
        #     "doctype": ["NO-LIMIT", "BK", "CH", "CA", "CP", "DS", "JA", "PP", "RC", "RR", "ST"],
        #     "sort": "relevance",
        #     "treatmentType": "NO-LIMIT",
        #     "searchStartTimestamp": str(int(time.time() * 1e3))
        # }
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
            "section1": "NO-LIMIT",
            "searchWord1": self.journal,
            "allDb": "35",
            "database": ["1", "2"],
            # "database": "1",
            "yearselect": "yearrange",
            "startYear": str(start_year),
            "endYear": str(endYear),
            "updatesNo": "1",
            "language": "NO-LIMIT",
            "doctype": ["NO-LIMIT", "BK", "CH", "CA", "CP", "DS", "JA", "PP", "RC", "RR", "ST"],
            "sort": "relevance",
            "treatmentType": "NO-LIMIT",
            "searchStartTimestamp": str(int(time.time() * 1e3))
        }
        try:
            async with sem:
                rand_cookies = rand_handle_coo(self._cookie)
                self.headers["cookie"] = cookie_to_str(rand_cookies)
                resp = await async_client.post(submit_url, data=form_data, headers=self.headers, follow_redirects=False, cookies=rand_cookies)
                coo = ""
                if resp.status_code in [301, 302]:
                    for k, v in resp.cookies.items():
                        coo += f"{k}={v}; "
                        self._cookie[k] = v
                    coo = coo.strip("; ")
                    return {
                        "location": resp.headers["location"],
                        "cookies": coo
                    }
                else:
                    log.error(f"err search status code {resp.status_code}")
                    return
        except Exception as e:
            traceback.print_exc()
            # log.error(str(e))
            return

    async def search_quick_index(self, start_yr):
        ret = await self.search_submit(start_yr)
        quick_search_url = "https://" + self.host + ret["location"]
        self.headers["referer"] = 'https://www.engineeringvillage.com/search/quick.url'
        self.headers["x-newrelic-id"] = "VQQAUldRCRAFUFFQBwgCUQ=="
        log.info(f"search journal {self.journal}")
        log.debug(f"quick_search_url {quick_search_url}")
        search_id = re.findall(r"^.*?&SEARCHID=(.*?)&.*?$", str(quick_search_url), re.I)[0]
        try:
            async with sem:
                seed = "".join(random.sample(string.ascii_lowercase + string.digits, random.randint(12, 12)))
                proxy_ipidea = {
                    "http://": f"http://qsx_global-zone-custom-region-hk-session-{seed}-sessTime-30:qsxglobal999@as.ipidea.io:2334",
                    "https://": f"http://qsx_global-zone-custom-region-hk-session-{seed}-sessTime-30:qsxglobal999@as.ipidea.io:2334"
                }
                _async_c = httpx.AsyncClient(timeout=_timeout, limits=_limit, follow_redirects=True, verify=False,
                                             http2=True, proxies=proxy_ipidea)
                resp = await _async_c.get(quick_search_url, headers=self.headers, follow_redirects=True, cookies=self._cookie)
                if resp.status_code in [200, 201]:
                    # update cookie
                    for k, v in resp.cookies.items():
                        self._cookie[k] = v
                    # log.info(resp.json())
                    resp_data = resp.json()
                    # 判断初始页面是不是每页100展示
                    if int(resp_data["pagenav"]["resultscount"]) > 100 and len(resp_data["results"]) < 100:
                        await self.search_quick_index_max_page(search_id, resp_data["pagenav"]["resultscount"])
                    else:
                        total_page = floor(int(resp_data["pagenav"]["resultscount"]) / 100) + 1
                        log.info(f"{self.journal} total_page {total_page}")
                        for r in resp_data["results"]:
                            try:
                                title = re.findall(r'^.*?</span> (.*?)"$', r["title"], re.I)[0]
                            except:
                                title = r["title"].strip()
                            try:
                                doc_id = r["doc"]["docid"]
                                doc_index = str(r["doc"]["hitindex"])
                                link = f"https://www.engineeringvillage.com/app/doc/?docid={doc_id}&pageSize=100&index={doc_index}&searchId={search_id}&resultsCount={str(resp_data['pagenav']['resultscount'])}&usageZone=resultslist&usageOrigin=searchresults&searchType=Quick"
                                pub_year = int(r["yr"])
                                d = {
                                    "title": title,
                                    "link": link,
                                    "pub_year": pub_year,
                                    "result_count": resp_data["pagenav"]["resultscount"]
                                }
                                await aio_redis.aredis_db.lpush(f"EI-10-11:{self.journal}", json.dumps(d))
                                log.info("redis add success")
                                del _async_c
                            except:
                                pass
                        # 遍历每页
                        for p in range(total_page):
                            await self.search_quick_page(search_id, resp_data["pagenav"]["resultscount"], p)
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
        self.headers["referer"] = 'https://www.engineeringvillage.com/search/quick.url'
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
                        link = f"https://www.engineeringvillage.com/app/doc/?docid={doc_id}&pageSize=100&index={doc_index}&searchId={search_id}&resultsCount={str(resp_data['pagenav']['resultscount'])}&usageZone=resultslist&usageOrigin=searchresults&searchType=Quick"
                        pub_year = int(resp_data["yr"])
                        d = {
                            "title": title,
                            "link": link,
                            "pub_year": pub_year,
                            "result_count": result_count
                        }
                        await aio_redis.aredis_db.lpush(f"EI-10-11:{self.journal}", json.dumps(d))
                        log.info("redis add success")
                    except:
                        pass
                # 遍历每页
                tasks = [self.search_quick_page(search_id, resp_data["pagenav"]["resultscount"], p) for p in range(total_page)]
                await asyncio.gather(*tasks)
            else:
                with open(r"./err_page/err_ei_search_quick_max.html", "w", encoding="utf8") as f:
                    f.write(resp.text)
                raise Exception(f"err_status_code {resp.status_code}")
        except Exception as e:
            log.error(str(e))
            pass

    async def search_quick_page(self, search_id, result_count, page: int):
        if page == 0 or page >= 50:
            return
        log.debug(f"{self.journal} page {page+1}")
        count = page * 100 + 1
        if count == 101:
            self.headers[
                "referer"] = f"https://www.engineeringvillage.com/search/quick.url?SEARCHID={search_id}&COUNT=1&usageOrigin=&usageZone="
        else:
            self.headers[
                "referer"] = f"https://www.engineeringvillage.com/search/quick.url?SEARCHID={search_id}&COUNT={str(count - 100)}&usageOrigin=&usageZone="
        self.headers["accept"] = "application/json, text/javascript, */*; q=0.01"
        self.headers["sec-ch-ua-mobile"] = "?0"
        self.headers["sec-fetch-mode"] = "cors"
        try:
            url = f"https://www.engineeringvillage.com/search/results/quick.url?navigator=NEXT&SEARCHID={search_id}&database=1&angularReq=true&isFullJsonResult=false&usageOrigin=searchresults&COUNT={str(count)}&usageZone=nextpage"
            async with sem:
                seed = "".join(random.sample(string.ascii_lowercase + string.digits, random.randint(12, 12)))
                proxy_ipidea = {
                    "http://": f"http://qsx_global-zone-custom-region-hk-session-{seed}-sessTime-30:qsxglobal999@as.ipidea.io:2334",
                    "https://": f"http://qsx_global-zone-custom-region-hk-session-{seed}-sessTime-30:qsxglobal999@as.ipidea.io:2334"
                }
                _async_c = httpx.AsyncClient(timeout=_timeout, limits=_limit, follow_redirects=True, verify=False,
                                             http2=True, proxies=proxy_ipidea)
                resp = await _async_c.get(url, headers=handle_headers(self.headers), follow_redirects=True, cookies=self._cookie)
                if resp.status_code in [200, 201]:
                    # update cookie
                    for k, v in resp.cookies.items():
                        self._cookie[k] = v
                    # with open("err_EI_quick_search_page.html", "w") as f:
                    #     f.write(resp.text)
                    if "System Error" in resp.text:
                        log.error("search error")
                        return
                    with open("EI_next_page.json", "w") as f:
                        f.write(json.dumps(resp.json()))
                    resp_data = resp.json()
                    for r in resp_data["results"]:
                        try:
                            if "Journal" in r["dt"][0]:
                                title = r["title"]
                                doc_id = r["doc"]["docid"]
                                doc_index = str(r["doc"]["hitindex"])
                                classify = r["source"]
                                link = f"https://www.engineeringvillage.com/app/doc/?docid={doc_id}&pageSize=100&index={doc_index}&searchId={search_id}&resultsCount={str(resp_data['pagenav']['resultscount'])}&usageZone=resultslist&usageOrigin=searchresults&searchType=Quick"
                                pub_year = int(r["yr"])
                                d = {
                                    "title": title,
                                    "link": link,
                                    "pub_year": pub_year,
                                    "result_count": result_count,
                                    "journal": self.journal,
                                    "classify": classify
                                }
                                await aio_redis.aredis_db.lpush(f"EI-10-11:{self.journal}", json.dumps(d))
                                log.info("redis add success")
                                del _async_c
                            else:
                                log.debug("not a Journal")
                                pass
                        except:
                            # traceback.print_exc()
                            pass
                else:
                    with open(r"./err_page/err_EI_search.html", "w", encoding="utf8") as f:
                        f.write(str(resp.headers))
                    raise Exception(f"err_status_code {resp.status_code}")
        except Exception as e:
            # traceback.print_exc()
            log.error(str(e))
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
        _referer = f"https://www.engineeringvillage.com/app/doc/?docid={kwargs['doc_id']}&pageSize=100&index=4&searchId={kwargs['search_id']}&resultsCount={str(kwargs['results_count'])}&usageZone=resultslist&usageOrigin=searchresults&searchType={self._search_type}"
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
        _url = "https://www.engineeringvillage.com/rest/doc"
        try:
            doc_id = re.findall(r"^.*?docid=(.*?)&.*?$", search_data["link"])[0]
            # search_id = self.search_id
            results_count = re.findall(r"^.*?resultsCount=(\d+)&.*?$", search_data["link"])[0]
            params = {
                "docid": doc_id,
                "pageSize": "100",
                "docIndex": str(89),
                "searchId": search_id,
                "resultsCount": str(results_count),
                "usageZone": "resultslist",
                "usageOrigin": "searchresults",
                "searchType": self._search_type
            }
            if has_val(self._cookie, "EISESSION"):
                session_id = self._cookie["EISESSION"].split(" ")[0].split("_")[1]
                _datetime = local2utc(datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.000+0000")
                json_data = {"searchId": search_id,
                             "sessionId": session_id,
                             # "userid": "27c5aa2bdc7b4becbb4836ed51e3b5d5",
                             "databasemask": "19980291",
                             # "searchtype": "Quick",
                             "searchtype": "Expert",
                             "savedate": _datetime,
                             "accessdate": _datetime,
                             "emailalert": "Off",
                             "saved": "Off",
                             "visible": "On",
                             "resultscount": str(results_count),
                             # "language": "NO-LIMIT",
                             "startYear": self.start_year,
                             "endYear": str(datetime.datetime.now().year),
                             "autostem": "on",
                             "sort": "relevance",
                             "sortdir": "dw",
                             "displayquery": f"((({self.journal}) WN KY) AND (({self.cy}) WN CO))",
                             "intermediatequery": f"((({self.journal}) WN KY) AND (({self.cy}) WN CO))",
                             # "documenttype": "NO-LIMIT",
                             # "treatmentType": "NO-LIMIT",
                             "refinestack": f"all@All@ALL@true@0~((({self.journal}) WN KY) AND (({self.cy}) WN CO))~((({self.journal}) WN KY) AND (({self.cy}) WN CO))QqQ<>",
                             "searchWord1": self.journal,
                             "searchWord2": self.cy,
                             "section1": "KY",
                             "section2": "CO",
                             "boolean1": "AND",
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
                             "serialnumber": 4,
                             "databasedisplay": "Compendex, Inspec, GEOBASE, GeoRef, US Patents, EP Patents & WO Patents",
                             "alertOwner": False,
                             "searchHistoryRecording": True,
                             "resultsCountWithCommas": gen_num(int(results_count)),
                             "offset": 0}
                js_data = await self.search_get_js(doc_id=doc_id, search_id=search_id, results_count=results_count)
                # 若请求失败,使用默认值进行后续请求
                if js_data:
                    config_data = await self.search_get_script(account_id=js_data["account_id"],
                                                               agent_id=js_data["agent_id"],
                                                               trust_key=js_data["trust_key"])
                else:
                    js_data = {
                        "account_id": "1273121",
                        "agent_id": "1588758972",
                        "trust_key": "2038175",
                        "xpid": "VQQAUldRCRABUVRbAwAGUlcE",
                        "license_key": "2f90a42388"
                    }
                    config_data = await self.search_get_script(account_id=js_data["account_id"],
                                                               agent_id=js_data["agent_id"], trust_key=js_data["trust_key"])
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
                rand_cookies = rand_handle_coo(self._cookie)
                self.headers["cookie"] = cookie_to_str(rand_cookies)
                seed = "".join(random.sample(string.ascii_lowercase + string.digits, random.randint(12, 12)))
                proxy_ipidea = {
                    "http://": f"http://qsx_global-zone-custom-region-hk-session-{seed}-sessTime-30:qsxglobal999@as.ipidea.io:2334",
                    "https://": f"http://qsx_global-zone-custom-region-hk-session-{seed}-sessTime-30:qsxglobal999@as.ipidea.io:2334"
                }
                async with sem:
                    _async_c = httpx.AsyncClient(timeout=_timeout, limits=_limit, follow_redirects=True, verify=False, http2=True, proxies=proxy_ipidea)
                    resp = await _async_c.post(_url, headers=self.headers, follow_redirects=True, params=params,
                                                   json=json_data, cookies=rand_cookies)
                    if resp.status_code in [200, 201]:
                        _data = resp.json()
                        # log.info(_data)
                        publish_year = int(
                            _data["PAGE"]["PAGE-RESULTS"]["PAGE-ENTRY"][0]["EI-DOCUMENT"]["DOCUMENTPROPERTIES"]["YR"])
                        data_from = "EI"
                        keyword = ""
                        is_qikan = 1
                        article = _data["PAGE"]["PAGE-RESULTS"]["PAGE-ENTRY"][0]["EI-DOCUMENT"]["DOCUMENTPROPERTIES"][
                            "TI"]
                        area = ""
                        _is_ch = 0
                        # email = ""
                        # name = ""
                        try:
                            for au in _data["PAGE"]["PAGE-RESULTS"]["PAGE-ENTRY"][0]["EI-DOCUMENT"]["AUS"]["AU"]:
                                if "EMAIL" in list(au.keys()):
                                    email = au["EMAIL"]
                                    name = au["NAME"]
                                    _is_ch = is_ch(email)
                                    # classify = search_data["classify"]
                                    url = f"https://www.engineeringvillage.com/app/doc/?docid={doc_id}"
                                    try:
                                        abstract = \
                                            _data["PAGE"]["PAGE-RESULTS"]["PAGE-ENTRY"][0]["EI-DOCUMENT"][
                                                "DOCUMENTPROPERTIES"]["AB"]
                                    except:
                                        abstract = ""
                                    discipline = ""
                                    subdiscipline = ""
                                    conference = ""
                                    if has_val(search_data, "journal"):
                                        journal = search_data["journal"]
                                    else:
                                        journal = self.journal.replace(":", "").replace("buaa", "")
                                    m = md5()
                                    d = url + str(email)
                                    m.update(d.encode("utf8"))
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
                                        "classify": "",
                                        "url": url,
                                        "discipline": discipline,
                                        "subdiscipline": subdiscipline,
                                        "conference": conference,
                                        "journal": journal,
                                        "create_time": datetime.datetime.strftime(datetime.datetime.now(),
                                                                                  "%Y-%m-%d %H:%M:%S")
                                    }
                                    # print(data)
                                    # await async_sql_util.create_table(data_from)
                                    await async_sql_util.insert_data(data_from, data)
                                    # break
                                else:
                                    continue
                        except:
                            traceback.print_exc()
                            log.debug("no author")
                            return
                        # classify = ""
                        # url = f"https://www.engineeringvillage.com/app/doc/?docid={doc_id}"
                        # try:
                        #     abstract = \
                        #     _data["PAGE"]["PAGE-RESULTS"]["PAGE-ENTRY"][0]["EI-DOCUMENT"]["DOCUMENTPROPERTIES"]["AB"]
                        # except:
                        #     abstract = ""
                        # discipline = ""
                        # subdiscipline = ""
                        # conference = ""
                        # if has_val(search_data, "journal"):
                        #     journal = search_data["journal"]
                        # else:
                        #     journal = self.journal.replace(":", "").replace("buaa", "")
                        # _is_ch = is_ch(email)
                        # m = md5()
                        # m.update(url.encode("utf8"))
                        # _id = m.hexdigest()
                        # if email == "":
                        #     return
                        del _async_c
                    else:
                        with open(r"./err_page/err_ei_doc_detail.html", "w", encoding="utf8") as f:
                            f.write(resp.text)
                        raise Exception(f"err_status_code {resp.status_code}")
            else:
                raise Exception("cookie no EISESSION")
        except Exception as e:
            # with open(r"./err_page/err_ei_doc_detail.html", "w", encoding="utf8") as f:
            #     f.write(resp.text)
            if "Access denied" in resp.text:
                log.error("Access denied!!!")
            else:
                log.error(f"search_doc_detail_err {str(e)}")
            d = {
                "title": search_data["title"],
                "link": search_data["link"],
                "pub_year": search_data["pub_year"],
                "result_count": search_data["result_count"],
                "journal": journal,
                # "classify": search_data["classify"]
            }
            await aio_redis.aredis_db.lpush(f"EI-10-11:{journal}", json.dumps(d))


    def product_main(self, start_yr):
        try:
            asyncio.get_event_loop().run_until_complete(self.search_quick_index(start_yr))
        except:
            traceback.print_exc()
            pass

    async def async_consumer_main(self):
        # await self.product_get_cookie()
        keys = await aio_redis.aredis_db.keys(pattern='*EI-10-11:*')
        if len(keys) == 0:
            raise Exception("生产者队列已取完")
        keys = [bytes.decode(_).replace("EI-10-11:", "") for _ in keys]
        for k in keys:
            log.debug(f"pop key {k}")
            self.journal = k
            p = await aio_redis.aredis_db.pipeline()
            try:
                _datas = await batch_rpop(p, f"EI-10-11:{k}", random.randint(15, 20))
                _datas = _datas[1]
                if len(_datas) != 0:
                    ret = await self.search_submit(datetime.datetime.now().year)
                    if not ret:
                        _tasks = [aio_redis.back_in_redis(f"EI-10-11:{k}", json.dumps(literal_eval(bytes.decode(_data)))) for _data in _datas]
                        await asyncio.gather(*_tasks)
                        log.debug("back into redis success")
                        raise Exception("search submit err")
                    search_id = re.findall(r"^.*?SEARCHID=(.*?).*?$", str(ret["location"]), re.I)[0]
                    __tasks = [self.search_doc_detail(search_id, literal_eval(bytes.decode(_data))) for _data in _datas]
                    await asyncio.gather(*__tasks)
                else:
                    log.info("生产者队列已取完")
                    return
            except Exception as e:
                log.error(str(e))
                return
            finally:
                p.pipeline().close()

    @staticmethod
    def consumer_main():
        try:
            while True:
                ei = EIOffice("", 2018, "Quick", "")
                asyncio.get_event_loop().run_until_complete(ei.async_consumer_main())
                del ei
                time.sleep(random.randint(0, 1))
        except Exception as e:
            if "已取完" in str(e):
                sys.exit(1)
            traceback.print_exc()
            log.error(str(e))
            pass


def EI_product_main(start_year):
    name = "journals:EI-10-13"
    search_type = "Quick"
    search_id = ""
    while True:
        journal = bytes.decode(_redis.redis_db.lpop(name))
        try:
            for year in range(start_year, datetime.datetime.now().year + 1):
                EI = EIOffice(journal, year, search_type, search_id)
                EI.product_main(year)
                del EI
            time.sleep(random.randint(2, 4))
        except:
            traceback.print_exc()
            _redis.redis_db.rpush(name, journal)
            continue
