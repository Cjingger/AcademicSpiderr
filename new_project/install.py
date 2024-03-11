# !/usr/bin/python3
# -*- coding:utf-8 -*-
from subprocess import run, Popen


def run_install():
    cmd = r'pip3 install -i https://pypi.douban.com/simple -r requirements.txt'
    completed = run(cmd, shell=True, check=True)
    return completed

if __name__ == '__main__':
    run_install()


