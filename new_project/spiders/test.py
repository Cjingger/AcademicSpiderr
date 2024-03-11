# !/usr/bin/python3
# -*- coding:utf-8 -*-
from urllib.parse import *

if __name__ == '__main__':
    aa = {
        "eid":"2-s2.0-85166786299",
        "origin":"resultslist",
        "sort":"plf-f",
        "src":"s",
        "sid":"83fef8f5654ef79296e36f957ccc7e02",
        "sot":"a",
        "sdt":"a",
        "s":f"SRCTITLE(computer) AND PUBYEAR &gt; 2018",
        "sl":"40",
        "sessionSearchId":"83fef8f5654ef79296e36f957ccc7e02"
    }
    url = "https://www.scopus.com/record/display.uri"
    url = url + "?" + urlencode(aa)
    bb = "https://www.scopus.com/record/display.uri?eid=2-s2.0-85166786299&origin=resultslist&sort=plf-f&src=s&sid=83fef8f5654ef79296e36f957ccc7e02&sot=a&sdt=a&s=SRCTITLE%28computer%29+AND+PUBYEAR+%26gt%3B+2018&sl=40&sessionSearchId=83fef8f5654ef79296e36f957ccc7e02"
    if url == bb:
        print("wwwww")