import random
import sys
import time
import traceback
from copy import deepcopy

import httpx
from lxml import etree
import hashlib
import datetime
import asyncio
from spiders import async_sql_util
from common.tools import *
from common.logs import Logs
from utils import redisUtil

sslgen = SSLFactory()

def handle_headers(header: dict):
    k_list = []
    _header = deepcopy(header)
    for k in list(header.keys()):
        flag = random.choice([0, 1])
        if k in ["Cache-Control", "Pragma", "sec-ch-ua-mobile", "sec-ch-ua-platform", "sec-fetch-dest", "sec-fetch-mode", "sec-fetch-site", "Proxy-Connection"] and flag == 1:
            _header.pop(k)
        else:
            k_list.append(k)
            continue
    # for i in range(0, 6):
    #     _header[_random_string(random.randint(3, 10))] = _random_string(random.randint(5, 50))
    return _header

_timeout = httpx.Timeout(timeout=20, connect=15, read=16)
_limit = httpx.Limits(max_connections=200, max_keepalive_connections=150)
proxy = {
    "http://": f"http://a364187154_{random.randint(1, 100000000)}-country-hk:a123456z@gateus.rola.info:1000",
    "https://": f"http://a364187154_{random.randint(1, 100000000)}-country-hk:a123456z@gateus.rola.info:1000"
}

async_client_proxy = httpx.AsyncClient(timeout=_timeout, limits=_limit, follow_redirects=True, verify=sslgen(), http2=True, proxies=proxy)


log = Logs()
sem = asyncio.Semaphore(30)
_redis = redisUtil.RedisUtil()

class SpiderTandfonline():
    def __init__(self):
        self._header = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "deflate",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://www.tandfonline.com/",
            "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(108, 112)}.0.0.0 Safari/537.36"
        }
        # self._search_list = ['Lecture Notes In Computer Science']

    async def get_url_body_list(self, journal, i):
        log.info(f"start {journal} page {i+1}")
        url = f"https://www.tandfonline.com/action/doSearch?field1=AllField&text1={journal}&Ppub=&AfterYear=2018&BeforeYear=2023&pageSize=50&subjectTitle=&startPage={i}"
        try:
            async with sem:
                res = await async_client_proxy.get(url=url, headers=handle_headers(self._header))
                if res.status_code in [200, 201]:
                    html = etree.HTML(res.text)
                    url_body_list = html.xpath('//article[@class="searchResultItem"]/@data-doi')[0]
                    return url_body_list
                elif res.status_code in [403, 401] and "not been recognised to access" in res.text:
                    # with open(r"./err_page/err_tandfonline_search.html", "w", encoding="utf8") as f:
                    #     f.write(res.text)
                    raise Exception("IP address has been blocked")
                else:
                    log.debug(f"err_url_body_code {res.status_code}")
                    return
        except IndexError or TypeError as e:
            log.error(str(e))
            return
        except:
            traceback.print_exc()
            return

    def get_author_info(self,name_list, email_list):
        authors_info1 = list(zip(name_list, email_list))
        authors_info = []
        for i in authors_info1:
            if i[1] != "":
                authors_info.append(i)
        return authors_info

    async def get_real_rul(self,url_body_list):
        for i in url_body_list:
            return i
    async def parse(self,_real_rul):
        if not _real_rul:
            return
        url = "https://www.tandfonline.com/doi/abs/" + _real_rul
        async with sem:
            resp = await async_client_proxy.get(url=url, headers=self._header)
            html = etree.HTML(resp.text)
            # 出版时间
            publish_year_list = html.xpath('//div[@class="widget literatumContentItemHistory none  widget-none  widget-compact-all"]/div[@class="wrapped "]/div[@class="widget-body body body-none  body-compact-all"]/div/text()')
            # 关键词
            keyword_list = html.xpath('//a[@class="kwd-btn keyword-click"]/text()')
            # 文章标题
            article_list = html.xpath('//meta[@property="og:title"]/@content')
            # 第一作者或通讯作者
            name_list = html.xpath('//div[@class="entryAuthor"]/a[@class="author"]/text()')
            # 作者邮箱
            email_list = html.xpath('//span[@class="corr-email"]/a/text()')
            author_info = self.get_author_info(name_list, email_list)
            # 学科类别
            classify_list = html.xpath('//meta[@name="citation_journal_title"]/@content')
            # 摘要
            abstract_list = html.xpath('//div[@class="abstractSection abstractInFull"]/p/text()')
            # 来源名
            journal_list = html.xpath('//h1[@class="journal-heading"]/a/text()')
            # 链接
            if len(author_info) == 0:
                log.debug("无邮箱")
                return
            # info_list = [publish_year_list,keyword_list,article_list,author_info,classify_list,abstract_list,journal_list,url]
            data = self.save_info(publish_year_list,keyword_list,article_list,author_info,classify_list,abstract_list,journal_list,url)
            await async_sql_util.create_table(data["data_from"])
            await async_sql_util.insert_data(data["data_from"], data)
    def save_info(self,publish_year_list,keyword_list,article_list,author_info,classify_list,abstract_list,journal_list,url):
        abstract_list_1,journal_list_1 = self.check_info(abstract_list,journal_list)
        md5 = hashlib.md5()
        md5.update(url.encode("utf8"))
        _id = md5.hexdigest()
        data = {
            "id": _id,
            "author": author_info[0][0].strip(),
            "time": int(publish_year_list[-1:][0][-4:]),
            "data_from": "tandfonline",
            "keyword": str(keyword_list),
            "is_qikan": 1,
            "article": article_list[0],
            "abstract": abstract_list_1[0],
            "email": author_info[0][1],
            "area": "",
            "is_ch": is_ch(author_info[0][1]),
            "classify": classify_list[0],
            "url": url,
            "discipline": "",
            "subdiscipline": "",
            "conference": "",
            "journal": journal_list_1[0].strip().strip("\n"),
            "create_time": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        }
        return data

    def check_info(self,abstract_list,journal_list):
        if len(abstract_list) == 0:
            abstract_list1 = [""]
        else:
            abstract_list1 = abstract_list
        if len(journal_list) == 0:
            journal_list1 = [""]
        else:
            journal_list1 = journal_list

        return abstract_list1,journal_list1

    async def async_run(self, journal):
        try:
            tasks = [self.get_url_body_list(journal, i) for i in range(0, 20)]
            url_body_list = await asyncio.gather(*tasks)
            print(url_body_list)
            tasks3 = [self.parse(j) for j in url_body_list]
            await asyncio.gather(*tasks3)
        except Exception as e:
            raise Exception(e)

    @classmethod
    def run(cls, journal):

        try:
            c = cls()
            asyncio.get_event_loop().run_until_complete(c.async_run(journal))
            del c
        except Exception as e:
            raise Exception(e)


def tanfonline_main():
    try:
        j = int(_redis.redis_db.llen("journals:tandfonline"))
        while j != 0:
            spider_tandfonline = SpiderTandfonline()
            journal = bytes.decode(_redis.redis_db.rpop("journals:tandfonline"))
            log.debug(f"pop key {journal}")
            spider_tandfonline.run(journal)
            time.sleep(random.randint(1, 2))
            j = int(_redis.redis_db.llen("journals:tandfonline"))
            del spider_tandfonline
        log.debug("生产者已取完")
    except:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':

    # PATH = r"../static/EI.xlsx"
    # name = "tandfonline"
    # DataUtil.load_index_data(PATH, name)
    tanfonline_main()