# coding: UTF-8
__author__ = 'Шенк Евгений Станиславович'

import json
import requests
import os
from datetime import datetime as dt
from requests.exceptions import HTTPError

# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.


def j_save():
    path = os.path.join(os.getcwd(), f'{username}_repos_{int(dt.now().timestamp())}.json')
    with open(path, 'w') as j_file:
        j_file.write(json.dumps(result_data))


result_data = []

# username = 'Auress'
# username = 'TelegramBot'
# username = 'wycats'
username = input('Username: ')

url = str(f'https://api.github.com/users/{username}/repos')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
           'Accept': 'application/vnd.github.v3+json'}

i = 1
while True:
    try:
        params = {'per_page': '100', 'page': f'{i}'}
        data = requests.get(url, params=params, headers=headers)
        data.raise_for_status()
        j_data = data.json()
        if len(j_data) == 0:
            j_save()
            break
        for x in j_data:
            result_data.append(x['name'])
    except HTTPError as http_error:
        print(f'HTTP error occurred: {http_error}')
        break
    except Exception as error:
        print(f'Other error occurred: {error}')
        break
    else:
        print('Success!')
    i += 1
