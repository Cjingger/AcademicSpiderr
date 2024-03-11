# !/usr/bin/python3
# -*- coding:utf-8 -*-
import asyncio
import sys
import traceback
from ast import literal_eval
from datetime import datetime
from hashlib import md5

from common.common_utils import batch_rpop
from spiders import async_sql_util, aio_redis, log, _redis
from utils.redisUtil import RedisUtil
from common.tools import *
import httpx
import websocket
import _thread as thread
from retrying import retry
from websocket._exceptions import WebSocketException
from socket import timeout

_timeout = httpx.Timeout(timeout=12, connect=10, read=10)
_limit = httpx.Limits(max_connections=50, max_keepalive_connections=50)


sslgen = SSLFactory()

proxy = {
    "http://": f"http://a364187154_{random.randint(1, 100000000)}-country-hk:a123456z@gateus.rola.info:1000",
    "https://": f"http://a364187154_{random.randint(1, 100000000)}-country-hk:a123456z@gateus.rola.info:1000"
}

globals()
msg = ""

def on_msg(ws, msg):

    if msg == "pong":
        ws.close()
    else:
        msg = json.loads(msg)
        if msg["key"] == "records":
            log.info(f"message {msg}")
            for d in msg["payload"].values():
                asyncio.get_event_loop().run_until_complete(aio_redis.aredis_db.lpush(f'webofscience:{str(d["titles"]["source"]["en"][0]["title"])}', json.dumps(d["colluid"])))
                log.info("redis add success")


def on_err(ws, err):
    raise Exception(err)


def on_close(ws):
    print("ws closed")


def on_open(ws):
    print("open ws connection...")

    # def run(*args):
    ws.send(msg)

    # thread.start_new_thread(run, ())


def retry_if_io_error(exc):
    log.debug("retrying...")
    return isinstance(exc, WebSocketException)


class SciWos():
    # Sec-WebSocket-Key: Kt{random.randint(23, 99)}bCO71eFZ6tvCJ4yZUw==
    def __init__(self, journal, start_year):
        self.journal = journal
        self.start_year = start_year
        self.host = "www.webofscience.com/wos/woscc"
        self.headers = headersChange(f'''Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cache-Control: no-cache
Connection: Upgrade
Host: www.webofscience.com
Origin: https://www.webofscience.com
Pragma: no-cache
Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits
Sec-WebSocket-Key: {random.randint(1, 9)}{chr(random.randint(65, 90))}DxGJjKm7ImxY/FZOiI7w==
Sec-WebSocket-Version: 13
Upgrade: websocket
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36
''')
        self.sci_url = "https://www.webofscience.com/wos/woscc/full-record"
        self._cookie = 'OptanonAlertBoxClosed=2023-05-04T07:10:00.984Z; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; group=group-f; _abck=70ABC5BBD4B43AD6A26D46F15A337430~0~YAAQh+IZuHUq9QmIAQAATjwoSwmloaTA0A0WxBiZguFP2kYssqflUsFUPbV4LamtY1Uu0o2Y2Y3fipamZSzkPYTnQBjh3ybxQGjmZOXcjlqs+gQWfH8u4X4L0iDdjGcnQi7iLH2uMr7ZcbmuZNjPcaMXDlwyQ8YUZK8I8ElpUKRrPOfvG7q9V260XUX8rzH0juEh7UWKiH2pjKbJS7XoE7Rd9CcuTC1axqFCUCL5Pwl7WEb0hkitJDLqcnc7Qfv1EMOQTsuCAQFvlxtRXPEP4FyUeTtLrTAid5YgYlekSonrv2+H9PUVsThNe+jpvC0f+4GROhl1asH58czcL4FmvTqHilLOEgn9/QCX24WQHM6H9L0rFys+S2rI7DlSHdevLnTHCEP1WSXufuxxYO6ZIMFYrJ4Do8qjYs5lczsL~-1~-1~-1; bm_sz=D5E956BEA97FF02F335494C94EDA0673~YAAQh+IZuHYq9QmIAQAATjwoSxOJwsQKTSq1heSEwXdhhbhrJwLyhSTC06+/SHiZFmV9LxoBqYlaxxU1bdSaaqsGbV2wf4P8yjO3XHj03wfCl6MGbJ6pcqaSbGdZUVGKnRAGz6qvepmO6e8p4tZ89VCOV/g0O9avXB3wpp0lT/QySCt/Pu6bIvQm9xtOc+Q7ntpBwqYKP7HpIKsTiJ5OO84O802g3eih4eCOS4DbOJC4lAm7jMO+jvjLAdvNY/YJGDO864hEdA16+mhJ59bHfX8RyMGeNDLDdRtZaiJdrc8PvQ90OIqhclY=~3683396~4534841; _sp_id.840c=de2d6ea5-1d1f-4320-840c-1d1b676fee5e.1683184179.67.1684888118.1684862495.1f176632-5bb9-46f8-a31e-fbf36508470f.ab0c9e65-9b95-4e1c-9ca1-29a6c4815caa.9ea6e2f1-8407-48bb-a91f-649cf387ac99.1684888109841.2; OptanonConsent=isGpcEnabled=0&datestamp=Wed+May+24+2023+08%3A28%3A40+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202303.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=9838f1e4-c258-4ca2-854d-6fd0318a26ec&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1%2CC0002%3A1&geolocation=CN%3BHB&AwaitingReconsent=false; RT="z=1&dm=www.webofscience.com&si=6b6b8fb9-0a37-4652-8e45-15576809f83c&ss=li0yvq0e&sl=0&tt=0&bcn=%2F%2F684d0d43.akstat.io%2F"'
        self.global_id = 0
        self.cy = "PEOPLES R CHINA"
    def download_journal_data(self):
        '''

        :return:
        '''
        pass

    @retry(stop_max_attempt_number=3, retry_on_exception=Exception)
    def  request_get_total_info(self, SID, id):
        '''
        获取检索信息总览
        :param p:
        :param SID:
        :param qid:
        :param id:
        :return:
        '''
        ws = websocket.WebSocket()
        websocket.enableTrace(True)
        ws_link = f"wss://www.webofscience.com/api/wosnxcorews?SID={SID}"
        # ws.set_proxy()
        ws.connect(ws_link, timeout=15, redirect_limit=5)
        # msg = '{"commandId":"runQueryGetRecordsStream","params":{"qid":"%s","retrieve":{"first":51,"sort":"relevance","count":50,"jcr":true,"highlight":false,"analyzes":[]},"product":"WOSCC","searchMode":"general","viewType":"records"},"id":%d}' % (
        #     qid, id)
        # 主要爬取国内数据
        msg = '{"commandId":"runQuerySearch","params":{"product":"WOSCC","searchMode":"general","viewType":"search","serviceMode":"summary","search":{"mode":"general","database":"WOSCC","query":[{"rowText":"SO=(%s) AND CU=(%s)"}],"sets":[],"options":{"lemmatize":"On"},"timespan":{"type":"symbolic","using":"publication","symbol":"latest5Years"}},"retrieve":{"count":50,"sort":"relevance","history":true,"jcr":true,"analyzes":["TP.Value.6","REVIEW.Value.6","EARLY ACCESS.Value.6","OA.Value.6","DR.Value.6","ECR.Value.6","PY.Field_D.6","DT.Value.6","AU.Value.6","DX2NG.Value.6","PEERREVIEW.Value.6"]},"eventMode":null, "isPreprintReview": false},"id":%d}' % (self.journal, self.cy, id)
        ws.send(msg)
        # ws.recv()
        _data = json.loads(ws.recv())
        print("message", _data)
        if _data["key"] == "searchInfo":
            return {
                "result_count": _data["payload"]["RecordsAvailable"],
                "qid": _data["payload"]["QueryID"]
            }
        else:
            raise Exception("No searchInfo")

    def request_product_main(self, SID, _id):
        try:
            result = self.request_get_total_info(SID, _id)
            if result["result_count"] == 0:
                log.debug("no result")
                return
            page = result["result_count"] // 50 + 1
            log.info(f"{self.journal} total page {page}")
            for p in range(page):
                self.request_get_article_ids(p, SID, result["qid"], _id)
        except:
            traceback.print_exc()
            sys.exit(1)

    @retry(stop_max_attempt_number=3, retry_on_exception=retry_if_io_error)
    def request_get_article_ids(self, p, SID, qid, id):
        ws = websocket.WebSocket()
        ws_link = f"wss://www.webofscience.com/api/wosnxcorews?SID={SID}"
        ws.connect(ws_link, timeout=15, redirect_limit=5)
        msg = '{"commandId":"runQueryGetRecordsStream","params":{"qid":"%s","retrieve":{"first":%s,"sort":"relevance","count":50,"jcr":true,"highlight":false,"analyzes":[]},"product":"WOSCC","searchMode":"general","viewType":"records"},"id":%d}' % (
        qid, str(p * 50 + 1), id)
        log.info(f"page {p + 1}")
        ws.send(msg)
        while True:
            # ws.recv()
            _data = json.loads(ws.recv())
            if _data["key"] == "records":
                log.info(f"message {_data}")
                for key in list(_data["payload"].keys()):
                    try:
                        abstract = _data["payload"][key]["abstract"]["basic"]["en"]["abstract"]
                    except KeyError:
                        abstract = ""
                    data = {
                        "id": _data["payload"][key]["id"]["value"],
                        "qid": qid,
                        "publish_year": int(_data["payload"][key]["pub_info"]["pubyear"]),
                        "article": _data["payload"][key]["titles"]["item"]["en"][0]["title"],
                        "journal": _data["payload"][key]["titles"]["source"]["en"][0]["title"],
                        "index": key,
                        "abstract": abstract,
                    }
                    # data_list.append(data)
                    _redis.redis_db.lpush(f"sci:{self.journal}", json.dumps(data))
                    log.info("redis add success")
            elif _data["key"] == "COMPLETE":
                log.debug("record over")
                break
            else:
                continue
        # except Exception as err:
        #     traceback.print_exc()
        #     pass

    @retry(stop_max_attempt_number=3, retry_on_exception=retry_if_io_error)
    def request_query(self, SID, qid, id):
        websocket.enableTrace(False)
        # ws = websocket.WebSocket()
        ws_link = f"wss://www.webofscience.com/api/wosnxcorews?SID={SID}"
        ws = websocket.WebSocketApp(url=ws_link, on_error=on_err, on_close=on_close, header=self.headers, cookie=self._cookie)
        # ws.connect(ws_link, timeout=15, redirect_limit=5, header=["host: www.webofscience.com", "Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits", "Sec-WebSocket-Key: Dw1vSlF/IGcT4pYcTKT83g==", "Sec-WebSocket-Version: 13"], cookie='bm_sz=DD78212694C90C5E4379D6018376A266~YAAQdYFtaHjrjAaHAQAAlCkeCBOE4IXAIGUimNUwVeIKDlREvLEsiKYOcNvov48fgXjElQOkJfjkA4HxUwtYJMPwrWAtuaZKvsmqh4Es+Hm+VAECrt2MhbIbZ/UIR77QK9W0bvYDcSQr6YKkKrqm0JEDEDm95AG1MM5aUMFrJJx+PNUN739/c10o2TqaotnOUqekQWtppRHSe0/vyQXnl/8Zhy9eGZAo48Oyd+P4/EtjkngUmFuhHlTnVOGbHfNESYUa0jP9oZnNPjYbt2pX30CI4CpIc8YQwATn5hUUhXWe2okgfrD908E=~3289139~3748913; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; group=group-f; bm_mi=EF4EB7CD115337C896371E8E9D0C770D~YAAQdYFtaI/rjAaHAQAAHCseCBNejSlsc82RsQYzvxOOUJAsVUbrVDOHlPDGMNIz91H6YKxGcfELRVBBX6DKYDfKKZsH5RUhm1V8CDLmHR+sYxU2FC8qDP5DMOXgvKQttBc2c52i8tWLvVzqWGakS+9kBBK8qQGpv1UaonDwWXyR5FXbzy3N7QfVWsU3KO0pQnJ0GE6dLZMrARs9j28WwY/lb2u3zPBB+LN5ZxK9uPqw85aa7MNYGTtznHvDFXWaVuhnmeBLqwJlbz8htKPZaOddRgW7SZhNWa11WzHWNB2obKLx8bhX3IQiqzKpsovXbDI9jf0H0SA=~1; _sp_ses.840c=*; _abck=77620CF35994A2DC4438B4258BD334E6~0~YAAQdYFtaPTrjAaHAQAA1jAeCAnGNjVnh6zKwzBeDsRuwzMCb+4I0hyZnEhOv3eMCmc3/oagto0vFHBlaj/hy5jwHasRuikA5uKT/nh4jaxkm17A8+nerLBWPm8bJOL3Dg8IVfFMMmqAsCZ052OwCO/BCiwJsrmr4csefNaE1awSk//JSFjt+xsLGJW5e37REYKazFh8R8kb7AwK57h0zmk1R9l+chUnG0H6FWEWxO2ctJWPrUIcvgtBGVbb0oKlZqwf2dlBKP5Wt/zhIVbegyNL8jF29Q6SV5qkBceH8hNPcenJj5PJ282bpWBhAmKgTBAWWjWFMJxdbCjNUvygjqnO3vOSjmrtWUcxrLErxkkS4HFezXilEMavAZv8pIxqZoLUeMPphTBjmMoSw101FmN/V9S62YAYK/Fg3W/zMw==~-1~-1~-1; OptanonAlertBoxClosed=2023-03-22T07:00:19.982Z; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Mar+22+2023+15:00:19+GMT+0800+(中国标准时间)&version=6.39.0&isIABGlobal=false&hosts=&consentId=bed7338c-b058-4ddb-b324-73bfa7970dc9&interactionCount=1&landingPath=NotLandingPage&groups=C0001:1,C0003:1,C0004:1,C0005:1,C0002:1; ak_bmsc=B1DB912F4687879D7C1A5562A9C5F650~000000000000000000000000000000~YAAQdYFtaKHtjAaHAQAA3oYeCBNLuc+F/kDyCOFiYFO7tbUwJ8GsH6/knSmnk1Z65yLNY8401ujyR0z8KJnV4UuACpGxsVLwwBdowQZrgmbZhK5oin9822Z6yu/jcl7evTeedoSfSmv+MFVmVuXZDD1BBrs/dMFIVf5tvxmPZaNth/124ycub/0oa+olaeJwURgSYlyJDGucwcfoz9vASnhCtdHGlDkaWPoV8qBce/3FmwthAaBs5KISwtp70kRovnEmjGJxo+u/iWstTn/AdreugJjDqtN2rqFAnBW7ps/+Zhe+4YSC67WqAZE7FrwKlc7WXPkLnBzqAdP46iyGY7oSPdE3+VNZLKgm9bRDvGxX8cPong7Ld5pRKi33UT9e9AEzNXhFi6VAUXRy//AmAO63iwx0xGFqBK8eG0Jy03jMGBXkQmc=; _sp_id.840c=370363c4-a3cf-4718-af01-0b2a26bee754.1679468409.1.1679470005..48dd152e-7798-4532-a39a-a9045d68d4b0..70303ede-7c46-4fb5-9394-dac6527372aa.1679468408927.39; bm_sv=911C348A64770344A0A289C5DEB1678F~YAAQfjItF/UUKuqGAQAA3/k6CBMpjZ/4I1jyxivnEL5GMUfsCm+wPHq39+G0GqiSWCCMDpxoklfGSl62FCFC0slUyFjOdvnijPP4qrZkwESWSaKO6qboi5WqrJNIInjHJoHlWXd8urM+HQyQNKkfEbaK3NJnXwohJ8j49zYejlOWqkYRjbTQ/xuueCXAOnzqruNVShsOoZMQ1D/BIFwzbxU+eW7S5P328ix8aVQjBI/gWblzo5PW+KKFR+1KWCwAI2VpdVzgTQ==~1; RT="z=1&dm=www.webofscience.com&si=bec20eed-572c-4882-8f91-6970cec1625f&ss=lfjc4jyl&sl=0&tt=0&bcn=//684d0d41.akstat.io/&ul=14hn1&hd=14i1r"')
        # ws.send('{"commandId":"runQuerySearch","params":{"product":"WOSCC","searchMode":"general","viewType":"search","serviceMode":"summary","search":{"mode":"general","database":"WOSCC","query":[{"rowField":"SO","rowText":"Electric Power Systems Research"},{"rowBoolean":"AND","rowField":"AU","rowText":""}],"timespan":{"type":"symbolic","using":"publication","symbol":"latest5Years"}},"retrieve":{"count":50,"sort":"relevance","history":true,"jcr":true,"analyzes":["TP.Value.6","DR.Value.6","REVIEW.Value.6","EARLY ACCESS.Value.6","OA.Value.6","TMSO.Value.6","PY.Field_D.6","TASCA.Value.6","OG.Value.6","DT.Value.6","AU.Value.6","SO.Value.6","PUBL.Value.6","ECR.Value.6","DX2NG.Value.6"]},"eventMode":null},"id":%s}') % id
        # recv_data = json.loads(ws.recv())
        # print("query_data", recv_data)
        msg = '{"commandId":"runQueryGetRecordsStream","params":{"qid":"%s","retrieve":{"first":1,"sort":"relevance","count":50,"jcr":true,"highlight":false,"analyzes":[]},"product":"WOSCC","searchMode":"general","viewType":"records"},"id":%d}' % (qid, id)
        ws.on_open = on_open
        ws.on_message = on_msg
        ws.run_forever()

    def __consumer(self, data, SID):
        _id = random.randint(20, 188)
        ws = websocket.WebSocket()
        try:
            ws_link = f"wss://www.webofscience.com/api/wosnxcorews?SID={SID}"
            ws.connect(ws_link, timeout=10, redirect_limit=5)
            # msg = '{"commandId":"runQuerySearch","params":{"product":"WOSCC","searchMode":"record_ids","viewType":"search","serviceMode":"summary","search":{"database":"WOSCC","mode":"record_ids","uts":["WOS:%s"]},"retrieve":{"first":1,"links":"retrieve","sort":"relevance","count":1,"view":"super","coll":null,"activity":false,"analyzes":null,"jcr":true,"reviews":true,"highlight":null,"secondaryRetrieve":{"associated_data":{"sort":"relevance","count":10},"cited_references":{"sort":"author-ascending","count":"30"},"citing_article":{"sort":"date","count":2,"links":null,"view":"mini"},"cited_references_with_context":{"sort":"date","count":135,"view":"mini"},"recommendation_articles":{"sort":"recommendation-relevance","count":5,"links":null,"view":"mini"}}},"eventMode":null},"id":5}' % journal_id
            msg = '{"commandId":"getFullRecordByQueryId","params":{"qid":"%s","id":{"value":"%s","type":"colluid"},"retrieve":{"first":6,"links":"retrieve","sort":"relevance","count":1,"view":"super","coll":"","activity":true,"analyzes":null,"jcr":true,"reviews":true,"highlight":false,"secondaryRetrieve":{"associated_data":{"sort":"relevance","count":10},"cited_references":{"sort":"author-ascending","count":"30"},"citing_article":{"sort":"date","count":2,"links":null,"view":"mini"},"cited_references_with_context":{"sort":"date","count":135,"view":"mini"},"recommendation_articles":{"sort":"recommendation-relevance","count":5,"links":null,"view":"mini"}}},"product":"WOSCC","searchMode":"record_ids","serviceMode":"summary","viewType":"records","paginated":true},"id":%s}' % (
            data["qid"], data["id"], str(_id))
            ws.send(msg)
            _msg = None
            ws.recv()
            _id += 1
            _data = json.loads(ws.recv())
            ws.close()
            if _data["key"] == "full-record":
                return _data
            elif _data["key"] == "COMPLETE":
                log.debug("get full record over")
                return
            else:
                return
        except timeout:
            _redis.redis_db.rpush(f"sci:{self.journal}", json.dumps(data))
            log.debug("req time out")
            raise Exception("req time out")

        except Exception as e:
            ws.close()
            raise Exception(str(e))

        # ws.close()
        # return _msg


    async def request_consumer_main(self, SID):
        # _data = json.loads(redis.redis_db.lpop(f"sci:{self.journal}"))
        # journal_id = _data["journal_id"]; _id = _data["id"]
        keys = await aio_redis.aredis_db.keys(pattern='*sci:*')
        if len(keys) == 0:
            raise Exception("生产者队列已取完")
        keys = [bytes.decode(_).replace("sci:", "") for _ in keys]
        p = await aio_redis.aredis_db.pipeline()
        for k in keys:
            try:
                log.debug(f"pop key {k}")
                self.journal = k
                _datas = await batch_rpop(p, f"sci:{k}", random.randint(10, 16))
                _datas = _datas[1]
                if len(_datas) != 0:
                    for d in _datas:
                        try:
                            d = literal_eval(bytes.decode(d))
                            consumer_data = self.__consumer(d, SID)
                            if consumer_data is None:
                                raise Exception("resp data err")
                            # publish_year = _data["publish_year"]
                            consumer_data = consumer_data["payload"]
                            publish_year = int(consumer_data["pub_info"]["pubyear"])
                            data_from = "webofscience"
                            keyword = ""
                            if has_val(consumer_data, "keywords"):
                                for k in consumer_data["keywords"]:
                                    keyword += k + ","
                            keyword = keyword.strip(",")
                            is_qikan = 1 if consumer_data["pub_info"]["pubtype"] == "Journal" else 0
                            article = consumer_data["titles"]["item"]["en"][0]["title"]
                            try:
                                area = consumer_data["address_data"]["address"][0]["address_spec"]["city"]
                            except:
                                area = ""
                            email = None
                            name = None
                            # 谁有邮箱就记录哪个作者的信息
                            for a in consumer_data["names"]["author"]["en"]:
                                if has_val(a, "email_addr"):
                                    name = a["full_name"]
                                    email = a["email_addr"]
                                else:
                                    continue
                            if not email:
                                return
                            _is_ch = is_ch(email)
                            try:
                                classify = consumer_data["category_info"]["subjects"][0]["subject"]
                            except:
                                classify = ""
                            # url = _data["article_url"]
                            discipline = consumer_data["category_info"]["subjects"][0]["subject"]
                            subdiscipline = str(consumer_data["category_info"]["headings"][0])
                            conference = ""
                            journal = d["journal"]
                            m = md5()
                            url = f"https://www.webofscience.com/wos/woscc/full-record/WOS:{d['id']}"
                            m.update(url.encode("utf8"))
                            _id = m.hexdigest()
                            data = {
                                "id": _id,
                                "author": name,
                                "time": publish_year,
                                "data_from": data_from,
                                "keyword": keyword,
                                "is_qikan": is_qikan,
                                "article": article,
                                "abstract": d["abstract"],
                                "email": email,
                                "area": area,
                                "is_ch": _is_ch,
                                "classify": classify,
                                "url": url,
                                "discipline": discipline,
                                "subdiscipline": subdiscipline,
                                "conference": conference,
                                "journal": journal,
                                "create_time": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                            }
                            await async_sql_util.create_table(data_from)
                            await async_sql_util.insert_data(data_from, data)
                        except KeyError as err:
                            await aio_redis.aredis_db.lpush(f"sci:{self.journal}", json.dumps(d))
                            log.error(err)
                            pass
            except Exception as e:
                raise Exception(e)

    @staticmethod
    def sci_consumer_main(SID):
        while True:
            try:
                sci = SciWos("", 2018)
                asyncio.get_event_loop().run_until_complete(sci.request_consumer_main(SID))
                del sci
            except Exception as err:

                traceback.print_exc()
                sys.exit(1)

def product_sci(SID):
    name = "journals:SCI-10-17"
    while _redis.redis_db.llen(name) > 0:
        journal = bytes.decode(_redis.redis_db.lpop(name))
    #     journal = "JOURNAL OF THE INSTITUTE OF ENERGY"
        log.debug(f"product {journal}")
        start_year = 2018
        # qid = "7c6f5fed-f84e-40e0-848e-09b8e2606e65-85a25b12"
        _id = 6
        SciWos(journal, start_year).request_product_main(SID, _id)
    log.debug("期刊已取完")

# if __name__ == '__main__':
#     journal = "Computer Physics Communications"
#     start_year = 2018
#     # journal_id = "WOS:000680413700023"
#     SID = "USW2EC0A4DKPqjNSMaf9KT9j3JotT"
#     qid = "c8536ebb-5f36-4c09-9b4f-9689080c5a17-7b1aaf11"
#     _id = 9
#     colluid = "000932511700001"

