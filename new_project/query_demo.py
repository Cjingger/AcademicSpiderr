# !/usr/bin/python3
# -*- coding:utf-8 -*-
from utils.aioSqlUtil import sqlAlchemyUtil
import asyncio, csv, openpyxl
import xlrd, os, sys
import traceback
from functools import wraps
import pandas as pd
import cmath, math


def counter():
    @wraps
    def func(*args, **kwargs):
        i = 0
        ret = func(*args, **kwargs)
        i += 1
        return ret
    return func


async def q(path, journal):
    try:
        sql_util = sqlAlchemyUtil()
        ret = await sql_util.query_data(t="EI", journal=journal)
        if len(ret) == 0:
            return
        res = []
        # for r in ret:
        #     d = [_ for _ in r]
        #     res.append(d)
        for i in ret:
            r = [j for j in i.values()]
            res.append(r)
        # print("res", res)
        print(len(res))
        with open(path, "a", newline="\n", encoding="utf8") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(res)
    except:
        traceback.print_exc()
        pass

async def writer_csv(path: str):
    wkbook = openpyxl.load_workbook("static/EI-bio_medicine.xlsx")
    wksheet = wkbook.active
    journals = []
    # row_nums = wksheet.max_row
    # journals = [wksheet.cell(i, 0) for i in range(0, row_nums)]
    query = ""
    _len = len(wksheet["A"][0::])
    c = 0
    for i in wksheet["A"][0::]:
        journals.append(i.value)
        c += 1
        if c == _len // 4:
            break
    #     # query += f''' or (journal like \"%{i.value}%\" and is_ch = 1)'''
    #     query += f''' or (journal = \"{i.value}\" and is_ch = 1)'''
    # print(query)
    # if os.path.exists(path):
    #     os.remove(path)
    #     print("file removed")
    print(journals)
    print(len(journals))
    with open(path, "a", newline="\n", encoding="utf8") as f:
        csv_writer = csv.writer(f)
        header = ["author", "article", "abstract", "url", "time", "data_from", "keyword", "is_qikan", "email", "area", "classify", "discipline", "subdiscipline", "conference", "journal"]
        csv_writer.writerow(header)
    tasks = [q(path, j)for j in journals]
    await asyncio.gather(*tasks)

def filter_csv(file: str):
    data_frame = pd.read_csv(file, dtype=object)
    # 根据指定列进行去重
    column_to_deduplicate = ["email", "article"]  # 替换为你要根据的列的名称
    deduplicated_data_frame = data_frame.drop_duplicates(subset=column_to_deduplicate)

    # 将去重后的数据保存回CSV文件
    output_csv_file_path = f'filter_{file}'
    deduplicated_data_frame.to_csv(output_csv_file_path, index=False)

if __name__ == '__main__':
   cter = 0
   csv_path = "EI-bio_medicine.csv"
   asyncio.get_event_loop().run_until_complete(writer_csv(csv_path))
   # filter_csv(csv_path)