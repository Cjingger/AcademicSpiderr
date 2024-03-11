# !/usr/bin/python3
# -*- coding:utf-8 -*-
import json

if __name__ == '__main__':
    # charles导出的文件（仅需修改这个即可）
    charles_export_file = 'C:\\Users\Administrator\Desktop\charles导出的文件.har'

    with open(charles_export_file, encoding='utf-8') as f:
        result = f.readlines()
    result_json = json.loads(result[0])
    entries = result_json['log']['entries']

    for i in entries:
        for i_header in i['response']['headers']:
            for i_key, i_value in i_header.items():
                if i_value == 'Content-Type' and i_header['value'].startswith('text/'):
                    s = '【已替换】type:{}'.format(i_header['value'])
                    print(s.ljust(20), i['request']['url'])
                    # 查找text中的双引号 并转义
                    response_str_old = str(i['response']['content']['text'])
                    response_str_new = response_str_old.replace('"', '\\"')
                    break
    new_file = ''
    file_list = charles_export_file.split('\\')
    file_list[len(file_list) - 1] = '可正常导入_{}'.format(file_list[len(file_list) - 1])
    for i in file_list:
        new_file += i
        new_file += '\\'
    # 删除最后一个 \
    new_file = new_file[:-1]
    result_json = json.dumps(result_json)
    with open(new_file, 'w') as f:
        f.writelines(result_json)
