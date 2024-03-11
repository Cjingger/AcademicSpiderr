# !/usr/bin/python3
# -*- coding:utf-8 -*-
import argparse
import traceback
from argparse import ArgumentTypeError
from typing import Union
from spiders.EI_buaa import EIbuaa, EI_buaa_product_main
from spiders.EI_office import EIOffice, EI_product_main
from spiders.scopus import Scopus, scopus_product_main
from spiders.scopus_buaa import ScopusBuaa, scopus_buaa_product_main
from spiders.tandfonline import tanfonline_main
from spiders.sci_WOS import SciWos, product_sci
from common.logs import Logs

log = Logs()

def spider_run(proj, cs:Union[str], start_year, SID):
    if cs == "c" and proj == "scopus":
        log.info(f"start {proj} consumer")
        Scopus.consumer_main()
    elif cs == "s" and proj == "scopus":
        log.info(f"start {proj} product")
        scopus_product_main()
    elif cs == "c" and proj == "scopus_buaa":
        log.info(f"start {proj} consumer")
        ScopusBuaa.consumer_main()
    elif cs == "s" and proj == "scopus_buaa":
        log.info(f"start {proj} product")
        scopus_buaa_product_main()
    elif cs == "c" and proj == "EI":
        log.info(f"start {proj} consumer")
        EIOffice.consumer_main()
    elif cs == "s" and proj == "EI":
        log.info(f"start {proj} product")
        EI_product_main(start_year)
    elif cs == "c" and proj == "EI_buaa":
        log.info(f"start {proj} consumer")
        EIbuaa.consumer_main()
    elif cs == "s" and proj == "EI_buaa":
        log.info(f"start {proj} product")
        EI_buaa_product_main(start_year)
    elif cs == "c" and proj == "sci" and SID != "":
        log.info(f"start {proj} consumer")
        SciWos.sci_consumer_main(SID)
    elif cs == "s" and proj == "sci" and SID != "":
        log.info(f"start {proj} product")
        product_sci(SID)
    elif proj == "tandfonline":
        log.info(f"start {proj} run")
        tanfonline_main()
    else:
        raise ArgumentTypeError("argument error")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='传参调用爬虫程序')
    parser.add_argument('--proj', type=str, default="scopus", help='proj')
    parser.add_argument('--cs', type=str, default="", help='pro/cus')
    parser.add_argument('--start_year', type=int, default=2018, help='start_year')
    parser.add_argument('--sid', type=str, default="", help='SID')
    try:
        args = parser.parse_args()
        s = spider_run(args.proj, args.cs, args.start_year, args.sid)
    except Exception as e:
        log.error(str(e))
