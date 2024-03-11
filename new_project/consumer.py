# !/usr/bin/python3
# -*- coding:utf-8 -*-
from spiders.EI_office import EIOffice
from spiders.scopus import Scopus
from spiders.sci_WOS import SciWos

def scopus_consumer():
    Scopus.consumer_main()

def web_of_science_consumer():
    journal = "ACM COMMUNICATIONS IN COMPUTER ALGEBRA"
    start_year = 2018
    SID = "USW2EC0B3Dqd1c9zNyB8x5a1gNzjN"
    qid = "ae90ab81-3ded-4196-89f9-d70046fcfd57-7b269063"
    _id = 48
    colluid = "WOS:000887983900014"
    SciWos(journal, start_year).request_consumer_main(SID, _id)


def EI_office_consumer():
    journal = ""
    start_year = 2018
    search_type = "Quick"
    search_id = ""
    EI = EIOffice(journal, start_year, search_type, search_id)
    EI.consumer_main()

if __name__ == '__main__':
    scopus_consumer()