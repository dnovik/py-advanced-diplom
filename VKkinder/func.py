import requests
from VKkinder.settings import client_id
from datetime import datetime
import pandas as pd

token = 'a411bfb8349a25ad58e81d001f0653541c3a49c0174deed87b68e109b385bbb8edd3480567d304c9356a3'


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
        'v': '5.101'
    }

    result = requests.get(URL, params).json()

    return result


def get_found_users(search_result):

    candidates = []

    for candidate in result['response']['items']:
        candidates.append(
            {
                'user_id' : candidate['id'],
                'books' : candidate['books'],
                'first_name' : candidate['first_name'],
                'last_name' : candidate['last_name'],
                'movies' : candidate['movies'],
                'music' : candidate['music'],
                'alcohol' : candidate['personal']['alcohol'],
                'langs' : candidate['personal']['langs'],
                'life_main' : candidate['personal']['life_main'],
                'people_main' : candidate['personal']['people_main'],
                'political' : candidate['personal']['political'],
                'smoking' : candidate['personal']['smoking'],
                'relation' : candidate['relation'],
                'sex' : candidate['sex'],
                'photo_100' : candidate['photo_100']
            }
        )

    return candidates


if __name__ == "__main__":
    
    user_info = get_user_info('denis.novik')
    search_result = search_users(user_info)
    candidates = get_found_users(search_result)



candidates = []

for candidate in search_result['response']['items']:
    try:
        candidates.append(
                {
                    'user_id' : candidate['id'],
                    'books' : candidate['books'],
                    'first_name' : candidate['first_name'],
                    'last_name' : candidate['last_name'],
                    'movies' : candidate['movies'],
                    'music' : candidate['music'],
                    'alcohol' : candidate['personal']['alcohol'],
                    'langs' : candidate['personal']['langs'],
                    'life_main' : candidate['personal']['life_main'],
                    'people_main' : candidate['personal']['people_main'],
                    'political' : candidate['personal']['political'],
                    'smoking' : candidate['personal']['smoking'],
                    'relation' : candidate['relation'],
                    'sex' : candidate['sex'],
                    'photo_100' : candidate['photo_100']
                    }
        )
    except KeyError as err:
        candidate[err] = 'nan'

candidates



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