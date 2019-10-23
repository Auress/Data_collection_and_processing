# coding: UTF-8
__author__ = 'Шенк Евгений Станиславович'

import json
import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime as dt
import time
import dateutil.parser as pr

domain_url = 'https://geekbrains.ru'
blog_url = 'https://geekbrains.ru/posts'


def get_page_strict(soup):  # Сбор нужных данных со страницы, возвращает список инфы из статьи
    posts_list = []
    posts_data = soup.find_all('div', class_='page-content')

    for post in posts_data:
        try:
            img = post.find(class_='row blogpost p-t p-b-xl').find(
                class_='blogpost-content').find('img').attrs.get('src')
        except AttributeError:
            img = None
        post_dict = {
            "post_title": post.find(class_='row blogpost p-t p-b-xl').find(class_='blogpost-title').text,
            "post_image": img,
            "post_text": post.find(class_='row blogpost p-t p-b-xl').find(class_='blogpost-content').text,
            "post_pub_date": pr.parse((post.find(class_='row blogpost p-t p-b-xl').find(
                class_='blogpost-date-views').find(class_='m-r-md').attrs.get('datetime'))).timestamp(),
            "post_autor": {"name": post.find(class_='col-md-5 col-sm-12 col-lg-8 col-xs-12 padder-v').find(
                class_='text-lg').text,
                           "url": post.find(class_='col-md-5 col-sm-12 col-lg-8 col-xs-12 padder-v').find(
                               'a').attrs.get('href'), },
        }

        posts_list.append(post_dict)
    return posts_list


def get_page_soup(url):  # Получение soup с нужной страницы
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    page_data = requests.get(url, headers=headers)
    soup_data = BeautifulSoup(page_data.text, 'lxml')
    return soup_data


def parser(url):  # Пагинатор, +возвращает всю информацию
    total_list = []
    while True:
        soup = get_page_soup(url)
        total_list.extend(get_info(soup))
        try:
            url = soup.find('a', text='›', attrs={'rel': 'next'}).attrs.get('href')
        except AttributeError:
            break
        url = f"{domain_url}{url}"
        time.sleep(1)
    return total_list


def get_info(soup):  # Парсер инфы со страницы
    posts_list = []
    for x in soup.find_all('div', class_='post-item event'):
        data_url = x.find('a', class_='post-item__title h3 search_text').attrs.get('href')
        data_url = f"{domain_url}{data_url}"
        data_soup = get_page_soup(data_url)
        posts_list.extend(get_page_strict(data_soup))
    return posts_list


result_data = parser(blog_url)

# Сохранение в json
path = os.path.join(os.getcwd(), f'GeekBrains_blogs_info_{int(dt.now().timestamp())}.json')
with open(path, 'w', encoding='utf8') as j_file:
    j_file.write(json.dumps(result_data, ensure_ascii=False))

print(1)




