#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/26 18:34
# @Author  : LIU
# @Site    : 
# @File    : mail.ru.py
# @Software: PyCharm

# #Desc:
import datetime, email, re
import traceback

from imapclient import IMAPClient


class RamblerImap():
    def __init__(self, host, port):
        self.server = None
        self.ssl = True
        self.timeout = None
        self.serverpath = None
        self.client_init(host, port)

    def client_init(self, host, port):
        self.server = IMAPClient(host=host, ssl=self.ssl, port=port)

    def login(self, username, password):
        self.server.login(username, password)

    def _select_mail(self):
        self.server.select_folder('INBOX', readonly=True)
        res = self.server.search([u'SINCE', datetime.date(2022, 6, 25)])
        return res

    def select_active_mail(self):
        res = self._select_mail()
        # print(res)
        if len(res) >= 1:
            for i in res:
                msgdict = self.server.fetch(i, ['BODY[]'])
                mailbody = msgdict[i][b'BODY[]'].decode('utf-8')
                e = email.message_from_string(mailbody)
                html = ''
                for part in e.walk():
                    html = part.get_payload(decode=True)
                receive_mail = str(bytes.decode(html, encoding="utf8"))
                # print(receive_mail)
                try:
                    pat = re.findall(r'.*?^FB-(\d+).*?$', receive_mail, re.M)[0]
                    return pat
                except:
                    traceback.print_exc()
                    return False
        else:
            return False

if __name__ == '__main__':
    tiImap = RamblerImap("imap.rambler.ru", 993)
    tiImap.login("vitalijkudrjavcevyz8097@rambler.ru", "IzqbTuaRmOex548")
    if tiImap.select_active_mail():
        print(tiImap.select_active_mail())
    else:
        raise Exception("接受谷歌邮箱信息错误")