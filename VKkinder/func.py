import requests
from VKkinder.settings import client_id
from datetime import datetime

token = '23e76c21921f6d0892dfa162f3c49c9147d784488425508ac52bfb3291a888f64c83a372d93cc0edcaf19'


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


def search_users():
    URL = 'https://api.vk.com/method/users.search'

    params = {
        'age_from' : '',
        'age_to' : '',
        'city' : '',
        'fields' : 'sex, interests, movies, music'
    }



user_info = get_user_info(token)
user_age = datetime.now().year - int(user_info['response'][0]['bdate'].split('.')[2])
age_from = user_age - 5
age_to = user_age + 5



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