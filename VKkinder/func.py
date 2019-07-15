import requests
from VKkinder.settings import client_id
from datetime import datetime

token = '9698ecf5d0cc51aded8a386dc6076dad93fe0055382aa9984074893d031bff441a291bb864329aca450ed'


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
        'fields' : 'sex, bdate, books, city, education, interests, movies, music',
        'v': '5.89'
    }

    user_info = requests.get(URL, params)

    return user_info.json()


def search_users(user_info):
    URL = 'https://api.vk.com/method/users.search'

    user_age = datetime.now().year - int(user_info['response'][0]['bdate'].split('.')[2])
    age_from = user_age - 5
    age_to = user_age + 5   
    user_city = user_info['response'][0]['city']['id']

    params = {
        'access_token': token,
        'age_from' : age_from,
        'age_to' : age_to,
        'city' : user_city,
        'fields' : 'sex, status, interests, books, movies, music, domain, photo_100, relation, verified,personal, followers_count',
        'v': '5.89'
    }

    candidates = requests.get(URL, params)

    return candidates


user_info = get_user_info('denis.novik')
results = search_users(user_info)

results.json()


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