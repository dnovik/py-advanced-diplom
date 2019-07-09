import requests
from VKkinder.settings import client_id


token = 'ed6a8d2f9afa3474026da743b59c102f45513d021bb287a1e01d438eb7d45bce5d8a28292bef23de196c6'


def get_token_url(client_id):
    URL = 'https://oauth.vk.com/authorize'

    params = {
        'client_id' : client_id,
        'display' : 'page',
        'scope' : 'friends',
        'response_type' : 'token',
        'v' : '5.101'
    }

    token_url = requests.get(URL, params)
    return token_url.url


def get_user_info(username):
    URL = 'https://api.vk.com/method/users.get'

    params = {
        'access_token': token,
        'domain': username,
        'fields' : ['about', 'photo_100'],
        'v': '5.101'
    }

    user_info = requests.get(URL, params)

    return user_info.json()

def search_users():
    URL = 'https://api.vk.com/method/users.search'



get_user_info('denis.novik')

#ОБЩИЙ АЛГОРИТМ ПРИЛОЖЕНИЯ

1 # Определяем базовую информация пользователя, которая будет являться
#  критерием поиска новых друзей: 
# - Пол 
# - Возраст 
# - Список групп 
# - Город 
# - Семейное положение 
# - Образование

2 # Получаем список подходящих кандидатов
3 # Получаем список подходящих кандидатов