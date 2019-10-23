# coding: UTF-8
__author__ = 'Шенк Евгений Станиславович'

import json
import requests
import os
from datetime import datetime as dt
from requests.exceptions import HTTPError

# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.


def status(url, option='account'):
    api_url = f'{url}{option}'

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def j_save(result_data, option):
    path = os.path.join(os.getcwd(), f'DigitalOcean_{option}_{int(dt.now().timestamp())}.json')
    with open(path, 'w') as j_file:
        j_file.write(json.dumps(result_data))


api_token = input('Enter your api token: ')  # Сюда копируем свой api_token

url = 'https://api.digitalocean.com/v2/'

headers = {'Content-Type': 'application/json',
           'Authorization': f'Bearer {api_token}'}

data = status(url)
data_proj = status(url, 'projects')

j_save(data, 'account')
j_save(data_proj, 'projects')

# Результат запросов к Digital Ocean по api token :
# {'account': {'droplet_limit': 10, 'floating_ip_limit': 3, 'volume_limit': 10, 'email': 'auress.es@gmail.com',
# 'uuid': 'be3e9b4f4352e17fd581d8ef32581ee61c6d7bf6', 'email_verified': True, 'status': 'active', 'status_message': ''}}
# ***
# {'projects': [{'id': '484973f2-5a52-41aa-b6e9-09ae369f5a99', 'owner_uuid': 'be3e9b4f4352e17fd581d8ef32581ee61c6d7bf6',
# 'owner_id': 6649518, 'name': 'Test_1', 'description': '', 'purpose': 'Just trying out DigitalOcean',
# 'environment': '', 'is_default': True, 'created_at': '2019-10-14T18:05:16Z', 'updated_at': '2019-10-14T18:05:16Z'}],
# 'links': {'pages': {'first': 'https://api.digitalocean.com/v2/projects?page=1',
# 'last': 'https://api.digitalocean.com/v2/projects?page=1'}}, 'meta': {'total': 1}}
