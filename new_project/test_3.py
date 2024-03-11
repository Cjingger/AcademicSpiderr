# !/usr/bin/python3
# -*- coding:utf-8 -*-
import base64
import random
import re
import urllib.parse as up

fingerprint = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68"
}
def rand_sec_header():
    _sec_ch_ua = ""
    _dict = {
        '112.0.0.0 Safari': '"Not?A_Brand";v="99", "Chromium";v="112", "Google Chrome";v="112"',
        '111.0.0.0 Safari': '"Not?A_Brand";v="8", "Chromium";v="111", "Google Chrome";v="111"',
        '110.0.0.0 Safari': '"Not?A_Brand";v="24", "Chromium";v="110", "Google Chrome";v="110"',
        '109.0.0.0 Safari': '"Not?A_Brand";v="8", "Chromium";v="109", "Google Chrome";v="109"',
        '108.0.0.0 Safari': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        '107.0.0.0 Safari': '"Not?A_Brand";v="99", "Chromium";v="107", "Google Chrome";v="107"',
        '106.0.0.0 Safari': '"Not?A_Brand";v="99", "Chromium";v="106", "Google Chrome";v="106"',
        '105.0.0.0 Safari': '"Not?A_Brand";v="8", "Chromium";v="105", "Google Chrome";v="105"', }
    # '104.0.0.0 Safari': '"Not?A_Brand";v="99", "Chromium";v="104", "Google Chrome";v="104"',
    # '103.0.0.0 Safari': '"Not?A_Brand";v="99", "Chromium";v="103", "Google Chrome";v="103"'}
    for i in list(_dict.keys()):
        if i in fingerprint["user-agent"]:
            _sec_ch_ua = _dict[i]
    sec_header_a = {
        "sec-fetch-site": random.choice(["same-site", "cross-site"]),
        "sec-fetch-mode": random.choice(["cors", "no-cors"]),
        "sec-fetch-dest": "empty"
    }
    sec_header_b = {
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua-mobile": random.choice(["?0", "?1"]),
        "sec-ch-ua": _sec_ch_ua
    }
    rand_a = random.choices(list(sec_header_a.keys()), cum_weights=[10, 10, 10], k=random.randint(0, 3))
    new_sec_header_a = {a: sec_header_a[a] for a in rand_a}
    rand_b = random.choices(list(sec_header_b.keys()), cum_weights=[10, 10, 10], k=random.randint(0, 3))
    new_sec_header_b = {b: sec_header_b[b] for b in rand_b}
    new_sec_header_a.update(new_sec_header_b)
    return new_sec_header_a

_cookie = {
    "CLIENTIDSESSION": "5b9ba18e9c544ad59042958179e24ef2",
    "at_check": "true",
    "ev_dldpref": "%7B%22location%22%3A%22mypc%22%2C%22format%22%3A%22pdf%22%2C%22displaytype%22%3A%22default%22%2C%22rmselected%22%3A%22false%22%2C%22summary%22%3A%22false%22%2C%22baseaddress%22%3A%22www.engineeringvillage.com%22%2C%22filenameprefix%22%3A%22Engineering_Village%22%7D",
    "AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg": "1",
    "ev_oneclickdl": "null",
    "mbox": "PC#95ff95f472114110973f7eba4914907d.32_0#1746929335|session#45880af0567c4e90a4fc45cf69dca8ef#1683686395",
    "AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg": "-1124106680%7CMCIDTS%7C19488%7CMCMID%7C34680833624956583821395009355630351846%7CMCAAMLH-1684289335%7C11%7CMCAAMB-1684289335%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1683691735s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-1807344119%7CvVersion%7C5.2.0",
    "s_pers": "%20v8%3D1683684535215%7C1778292535215%3B%20v8_s%3DMore%2520than%25207%2520days%7C1683686335215%3B%20c19%3Dev%253Atimeout%253Aregister%7C1683686335221%3B%20v68%3D1683684534327%7C1683686335227%3B",
    "s_sess": "%20s_cpc%3D0%3B%20e78%3Dsearchword1%2520%253F%2520ab%2520contains%2520computer%2520communications%3B%20c21%3Dsearchword1%2520%253F%2520ab%2520contains%2520computer%2520communications%3B%20e13%3Dsearchword1%2520%253F%2520ab%2520contains%2520computer%2520communications%253A%3B%20c13%3Drelevance-dw%3B%20s_sq%3D%3B%20s_ppvl%3Dev%25253Asearch%25253Aquick%252C100%252C88%252C1156%252C1067%252C936%252C1920%252C1080%252C1%252CP%3B%20s_ppv%3Dev%25253Atimeout%25253Aregister%252C100%252C100%252C936%252C1067%252C936%252C1920%252C1080%252C1%252CP%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B",
    "EV-API-TOKEN": "EVSESS-d25b51c7-246c-4ca3-bb3e-be7fd26dfb41-i-02ee38cf37724e7fb",
    "OptanonAlertBoxClosed": "2023-05-10T02:30:10.722Z",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Wed+May+10+2023+11%3A35%3A33+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202302.1.0&isIABGlobal=false&hosts=&consentId=e081e2c4-df86-4d2e-a5eb-a37e202ab13d&interactionCount=2&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A0%2C4%3A0&AwaitingReconsent=false&geolocation=CN%3BHB",
    "EISESSION": "\"0_6c9cf8b9049045a687601702dff1a4bf:i-02ee38cf37724e7fb_2023-05-09 23:36:10_5a801b23c7438a92820724dce104d9b3\""
}

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

if __name__ == '__main__':
     quick = "https://www.engineeringvillage.com/search/results/quick.url?CID=quickSearchCitationFormat&database=1&SEARCHID=5be0bd1b2d094d1f9adc910ac09223a4&intialSearch=true&angularReq=true&usageOrigin=searchfo"
     search_id = re.findall(r"^.*?&SEARCHID=(.*?)&.*?$", str(quick), re.I)[0]
     # print(search_id)
     print(base64.b64decode("0gPjYyIzSSikldLyeEBiBmVEY2QAAAAAwINURaIXOAbVrmPJ9Pbvvw=="))
