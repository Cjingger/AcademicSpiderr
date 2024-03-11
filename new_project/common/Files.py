#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# @Time : 2021/09/02 16:23 下午
# @Author : 汤奇朋
# @File : Files.py
# @Software: PyCharm
import os
import json
import time
import configparser


def delete_line_breaks(line: str):
    return line.rstrip('\n') if line.__contains__('\n') else line


class Files:
    def __init__(self):
        self.basePath = os.path.abspath("")
        filePath = os.path.dirname(__file__)
        self.cf = configparser.ConfigParser()
        self.reafConfig('spider_service_config.ini')

    # 打开文件 替换换行符为 \n
    def open1(self, path: str, mode='r'):
        return open(file=self.basePath + path, mode=mode, newline='\n', encoding='utf_8_sig')

    # 打开文件 替换换行符为 \n
    def open_w(self, path: str, mode='a'):
        return open(file=self.basePath + path, mode=mode, newline='\n', encoding='utf_8_sig')

    def dump1(self, _list, key):
        stamp = time.strftime("%Y%m%d", time.localtime())

        if not os.path.exists(self.basePath + '/result/' + stamp):
            os.makedirs(self.basePath + '/result/' + stamp)

        with self.open1(path='/result/' + stamp + '/' + key + '.txt', mode='a') as f:
            for e in _list:
                f.write(str(e) + '\n')
            f.close()
        # 清空列表
        _list.clear()

    def createFile(self, path, content, model='a', encod='utf-8'):
        filePath = self.basePath + path
        fileJia = filePath[0:filePath.rindex('/')]
        if not os.path.exists(fileJia):
            os.makedirs(fileJia)
        with open(file=filePath, mode=model, encoding=encod) as f:
            f.write(content)
            f.close()

    def dump2(self, value, key):
        stamp = time.strftime("%Y%m%d", time.localtime())
        if not os.path.exists(self.basePath + '/result/' + stamp):
            os.makedirs(self.basePath + '/result/' + stamp)
        with self.open1(path='/result/' + stamp + '/' + key + '.txt', mode='a') as f:
            f.write(str(value) + '\n')
            f.close()

    def json(self, config):
        with self.open1('/config/' + config) as f:
            o = json.load(f)
            f.close()
        return o

    def reafConfig(self, name):
        self.cf.read(self.basePath + os.sep + 'config' + os.sep + name)

    def getConfigDict(self, name):
        return dict(self.cf.items(name))

    def getLogName(self, logDir, logName):
        logPath = os.path.join(self.basePath, logDir)
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        logName = os.path.join(logPath, logName)
        return logName
