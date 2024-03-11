import json
import random, ssl
import re, string
# import requests

def headersChange(text=''):
    dic = {}
    for x in text.split('\n'):
        a = x.split(': ')
        if len(a) >= 2:
            dic.update({a[0].strip(): a[1].strip()})
    return dic

def has_val(obj, key):
    try:
        return obj[key]
    except:
        return False

ORIGIN_CIPHERS = ('ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
                  'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES')


def rand_handle_coo(cookies: dict):
    new_cookies = {}
    items = ["NRBA_SESSION", "acw_tc", "JSESSIONID", "_gid", "H_PS_PSSID"]
    random.shuffle(items)
    it = items[0:random.randint(1, 5)]
    coo_item = list(cookies.keys())
    random.shuffle(coo_item)
    for j in coo_item:
        new_cookies[j] = cookies[j]
    for i in it:
        new_cookies[i] = "".join(random.sample(string.ascii_letters + string.digits, random.randint(10, 14)))
    # print(new_cookies)
    return new_cookies

def cookie_to_str(cookies: dict):
    coo = ""
    for k, v in cookies.items():
        coo += f"{k}={v}; "
    cookie = coo.strip("; ")
    return cookie


# :RSA+HIGH:RSA+3DES
#

class SSLFactory:
    def __init__(self):
        self.ciphers = ORIGIN_CIPHERS.split(":")

    def __call__(self) -> ssl.SSLContext:
        random.shuffle(self.ciphers)
        ciphers = ":".join(self.ciphers)
        # ciphers = ciphers + ":!aNULL:!eNULL:!MD5"
        context = ssl.create_default_context()
        context.set_ciphers(ciphers)
        return context


class Proxy():
    def __init__(self):
        self.ip = ""
        self.port = 0
        self.username = ""
        self.password = ""
        self.available = False

    def loadByJson(self, proxy):
        self.ip = proxy["ip"]
        self.port = int(proxy["port"])
        self.username = proxy["username"]
        self.password = proxy["password"]

    def loadByString(self, proxy):
        c = proxy.split(":")
        if len(c) < 2:
            return
        if len(c) >= 2:
            self.ip = c[0].strip()
            self.port = int(c[1].strip())
        if len(c) >= 4:
            self.username = c[2].strip()
            self.password = c[3].strip()
        return

    def toJson(self):
        return {"ip": self.ip, "port": self.port, "username": self.username, "password": self.password}

    def toProxiesRequests(self):
        _result = None
        if self.ip != '':
            if self.username == '':
                _result = {'http': 'http://%s:%d' % (self.ip, self.port),
                           'https': 'https://%s:%d' % (self.ip, self.port)}
            else:
                _result = {
                    'http': 'http://%s:%s@%s:%d/' % (self.username, self.password, self.ip, self.port),
                    'https': 'https://%s:%s@%s:%d/' % (self.username, self.password, self.ip, self.port)}
        return _result

    def toProxiesHttpx(self):
        _result = None
        if self.ip != '':
            if self.username == '':
                _result = {'http://': 'http://%s:%d' % (self.ip, self.port),
                           'https://': 'http://%s:%d' % (self.ip, self.port)}
            else:
                _result = {
                    'http://': 'http://%s:%s@%s:%d/' % (self.username, self.password, self.ip, self.port),
                    'https://': 'https://%s:%s@%s:%d/' % (self.username, self.password, self.ip, self.port)}
        return _result

    def toProxiesAiohttp(self):
        _result = None
        if self.ip != '':
            if self.username == '':
                _result = 'http://%s:%d' % (self.ip, self.port)
            else:
                _result = 'http://%s:%s@%s:%d' % (self.username, self.password, self.ip, self.port)
        return _result

    def toString(self):
        _text = ""
        if self.ip != "":
            _text += self.ip + ":" + str(self.port)
        else:
            _text = "noproxy"
        if self.username != "":
            _text += ":" + self.username + ":" + self.password
        return _text


# class UtlsNetwork():
#     def __init__(self, proxy=Proxy(), server_name="nike.com.hk", timeout=45):
#         self.server_host = "http://localhost:9726"
#         self.session_id = ""
#         self.proxy = proxy
#         self.type_common = False
#         self.server_name = server_name
#         self.http2 = False
#         self.timeout = timeout
#         self.not_redirect = True
#         self.fingerprint_http2_stream = []  # [["0x0", "2147483648", "0xc8"], ["0x0", "2147483648", "0xc8"]]
#
#     def create_session(self):
#         if self.type_common == False:
#             url = self.server_host + '/session/create'
#         else:
#             url = self.server_host + '/session/common/create'
#         if self.proxy == None or self.proxy.port == 0:
#             data = {"ip": "", "auth_username": "", "auth_password": ""}
#         else:
#             data = {"ip": self.proxy.ip + ":" + str(self.proxy.port), "auth_username": self.proxy.username,
#                     "auth_password": self.proxy.password}
#
#         data["not_redirect"] = self.not_redirect
#         data["use_http2"] = self.http2
#         data["server_name"] = self.server_name
#
#         ret = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
#         try:
#             ret_json = json.loads(ret.text)
#         except Exception as e:
#             raise Exception("Json load error, %s" % e)
#         if 'Message' not in ret_json or 'StatusCode' not in ret_json or ret_json['StatusCode'] != 0:
#             raise Exception("%d/%s" % (ret.status_code, ret.text))
#         self.session_id = ret_json['Message']
#
#     def delete_session(self):
#         if self.type_common == False:
#             url = self.server_host + '/session/close'
#         else:
#             url = self.server_host + '/session/common/close'
#         ret = requests.post(url=url, json={"id": self.session_id}, headers={"Content-Type": "application/json"})
#
#     def request(self, url="", data='', method="", header="", cookie={}, res=[], timeout=None, wait_response=True,
#                 delay=0):
#         header_list = []
#         header_order = []
#         for x in header.split('\n'):
#             a = x.split(': ')
#             if len(a) >= 2:
#                 h = {}
#                 h.update({"name": a[0].strip()})
#                 h.update({"value": ": ".join(a[1:]).strip()})
#                 header_list.append(h)
#                 header_order.append(a[0].strip().lower())
#         cookie_list = []
#         for n, v in cookie.items():
#             c = {}
#             c.update({"name": n.strip()})
#             c.update({"value": v.strip()})
#             cookie_list.append(c)
#
#         if not self.http2:
#             header_order = []
#
#         if self.type_common == False:
#             _url = self.server_host + '/session/request'
#         else:
#             _url = self.server_host + '/session/common/request'
#         _data = {"id": self.session_id,
#                  "request": {"header": header_list,
#                              "method": method, "cookie": cookie_list, "url": url, "res": res, "data": data,
#                              "wait_response": wait_response, "fingerprint_http2_stream": self.fingerprint_http2_stream,
#                              "delay": delay, "header_order": header_order}, "code": self._encode()}
#         if timeout == None:
#             ret = requests.post(url=_url, json=_data, headers={"Content-Type": "application/json"},
#                                 timeout=self.timeout)
#         else:
#             ret = requests.post(url=_url, json=_data, headers={"Content-Type": "application/json"}, timeout=timeout)
#         try:
#             ret_json = json.loads(ret.text)
#         except Exception as e:
#             raise Exception("Json load error, %s" % e)
#         if 'Message' in ret_json:
#             print(ret_json)
#             raise Exception('%d/%s' % (ret_json['StatusCode'], ret_json['Message']))
#         ret_json['cookie'] = {}
#         if 'header' in res:
#             for n, v in ret_json['Header'].items():
#                 if n.strip().lower() == "set-cookie":
#                     ret_json['cookie'][v.split("=", 1)[0].strip()] = v.split("=", 1)[1].strip()
#
#         ret_json["request_url"] = url
#         return ret_json
#
#     def _encode(self):
#         id = self.session_id
#         id = id.replace('-', '')
#         count = 0
#         sum = 0
#         for i in id:
#             # print(ord(i))
#             if count % 2 == 0:
#                 sum += ord(i)
#             else:
#                 sum -= ord(i)
#             count += 1
#         # print(sum)
#         return sum
#
#     def _header_get_sec(self, header=[]):
#         useragent = self._header_get_useragent(header)
#
#         # Chrome
#         rule = "Chrome\/(.*) Safari\/"
#         result = re.findall(rule, useragent)
#         # sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"
#         # sec-ch-ua-mobile: ?0
#         # sec-ch-ua-platform: "Windows"
#         # sec-fetch-dest: script
#         # sec-fetch-mode: no-cors
#         # sec-fetch-site: cross-site
#         if len(result) != 0:
#             # print(_)
#             header.append({"name": "sec-ch-ua",
#                            "value": '"Chromium";v="{v}", "Google Chrome";v="{v}", ";Not A Brand";v="99"'.format(
#                                v=result[0].split(".")[0])})
#             header.append({"name": "sec-ch-ua-mobile",
#                            "value": '?0'})
#             header.append({"name": "sec-ch-ua-platform",
#                            "value": '"{}"'.format(self._header_get_platform(useragent))})
#             header.append({"name": "sec-fetch-dest",
#                            "value": 'empty'})
#             header.append({"name": "sec-fetch-mode",
#                            "value": 'cors'})
#             header.append({"name": "sec-fetch-site",
#                            "value": 'same-origin'})
#         return header
#
#     def _header_get_useragent(self, header=[]):
#         for i in header:
#             if i["name"].lower() == "user-agent":
#                 return i["value"]
#
#     def _header_get_platform(self, useragent=""):
#         if "Windows" in useragent:
#             return "Windows"
#         if "Linux" in useragent:
#             return ""
#         if "MacOS" in useragent:
#             return "macOS"


def is_ch(email):
    if '.uk' == email[-3:] or ".ca" == email[-3:] or ".au" == email[-3:] or ".nz" == email[
                                                                                     -3:] or ".ie" == email[
                                                                                                      -3:] or '.de' == email[
                                                                                                                       -3:]:
        is_ch = 2
    elif "163.com" == email[-7:] or ".cn" == email[-3:] or ".hk" == email[
                                                                    -3:] or "qq.com" in email or "126.com" in email or "189.com" in email or "21cn.com" in email or "tom.com" in email or "sohu.com" in email or "aliyun.com" in email or "188.com" in email or "139.com" in email or "foxmail.com" in email or "jsinm.org" in email or "hecpharm.com" in email or "sina.com" in email or "njucm.com" in email or "bloomagefreda.com" in email or "263.net" in email or "edu.tw" in email or "yeah.net" in email or ".mo" == email[
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             -3:]:
        is_ch = 1
    else:
        is_ch = 0
    return is_ch


def parse_int(str, digit):
    res = 0
    for i, _s in enumerate(str):
        try:
            res += digit ** (len(str) - i - 1) * int(_s)
        except:
            res += digit ** (len(str) - i - 1) * to_int(_s.lower())
    return res


_map = {
    "a": 10,
    "b": 11,
    "c": 12,
    "d": 13,
    "e": 14,
    "f": 15,
}


def to_int(_s: str):
    return _map[_s]


def decode_email(_code):
    a = r(_code, 0)
    o = ""
    for i in range(2, len(_code), 2):
        l = r(_code, i) ^ a
        o += chr(l)
    return o


def r(_code, t):
    return parse_int(_code[t:t + 2], 16)

def gen_num(num: int):
    if len(str(num)) <= 4:
        res = str(num)[0] + "," + str(num)[1::]
    elif len(str(num)) == 5:
        res = str(num)[0:2] + "," + str(num)[2::]
    elif len(str(num)) == 6:
        res = str(num)[0:2] + "," + str(num)[3::]
    elif len(str(num)) == 7:
        res = str(num)[0] + "," + str(num)[1:3] + "," + str(num)[4::]
    else:
        res = str(num)[0] + "," + str(num)[1:3] + "," + str(num)[4::]
    return res
# print(decode_email("2a44044b044f5c4e45414347455c4b1a1f6a4d474b434604494547"))

if __name__ == '__main__':
    coo = {'CLIENTIDSESSION': 'f64305143929480c8e615560b3af1f8f', 'AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg': '-1124106680%7CMCIDTS%7C19488%7CMCMID%7C41051432569101542082650354428200694762%7CMCAID%7CNONE%7CMCOPTOUT-1683706452s%7CNONE%7CMCAAMLH-1684304052%7C11%7CMCAAMB-1684304052%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCSYNCSOP%7C411-19495%7CMCCIDH%7C-1556852246%7CvVersion%7C5.2.0', 'mbox': 'PC#03d4a9a3c8f34e0787f2a4e7cb5367a8.32_0#1746950852|session#d52845126c70492a84ab356b2f009009#1683707911', 's_pers': '%20v8%3D1683706052207%7C1778314052207%3B%20v8_s%3DLess%2520than%25201%2520day%7C1683707852207%3B%20c19%3Dev%253Atimeout%253Aregister%7C1683707852212%3B%20v68%3D1683706050947%7C1683707852217%3B', 'OptanonAlertBoxClosed': '2023-05-11T08:47:53.550Z', 'ev_oneclickdl': 'null', '__cf_bm': 'myZiR_46KZrHuf8o6SfvrAlnOr_tNj2xsvpGCLxS_S4-1694603593-0-ARdgOR7BpNtNKPBnAsuVIGLRbjtVcbz5bO1faVmMcPVQUBV3l+uNqDIFD6Btq6VlkvwTdZKjnqR338XbPcGLZY0', '_cfuvid': 'WR0W3Z1sp8pM_6lQ_Ljk7c0y96YjXcsCVRBcLkBHNZI-1694603593930-0-604800000', 'EV-API-TOKEN': 'EVSESS-bdde08aa-b2e1-402c-b9fe-eb94362140c8-i-0514e4a55b8eff3e9', 'EISESSION': '"0_d17646a4aa234434b07bf8293745b83f:i-0514e4a55b8eff3e9_2023-09-13 07:14:51_7944c4ecbb30f0fcff5736669691676a"', 'OptanonConsent': 'isGpcEnabled'}
    # cookie_to_str(coo)
    rand_handle_coo(coo)