# !/usr/bin/python3
# -*- coding:utf-8 -*-
import base64

import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime, timedelta
from common.common_utils import local2utc

def get_top_selling_items():
    url = 'https://www.amazon.com/Best-Sellers/zgbs'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', class_='a-link-normal')
    top_selling_items = []
    for link in links:
        href = link.get('href')
        if href.startswith('/gp/'):
            top_selling_items.append('https://www.amazon.com' + href)
    return top_selling_items[:50]

def get_product_info(product_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('span', id='productTitle').text.strip()
    price = soup.find('span', class_='a-price-whole').text.strip()
    rating = soup.find('span', class_='a-icon-alt').text.split()[0]
    reviews_count = soup.find('span', id='acrCustomerReviewText').text.split()[0]
    product_info = {
    'title': title,
    'price': price,
    'rating': rating,
    'reviews_count': reviews_count
    }
    return product_info

if __name__ == '__main__':

    # top_selling_items = get_top_selling_items()
    # print(top_selling_items)
    # today = datetime.now().strftime('%Y%m%d')
    # file_name = f'top_selling_items_{today}.csv'
    # with open(file_name, mode='w', encoding='utf-8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['title', 'price', 'rating', 'reviews_count'])
    # for product_url in top_selling_items:
    #     product_info = get_product_info(product_url)
    #     writer.writerow([product_info['title'], product_info['price'], product_info['rating'], product_info['reviews_count']])
    #     print(f"Product {product_info['title']} information saved successfully.")
    _datetime = local2utc(datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.000+0000")
    print(_datetime)