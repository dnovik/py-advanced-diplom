import requests
from VKkinder.settings import client_id
from datetime import datetime
import pandas as pd
import time
from pymongo import MongoClient

token = '9d1f99036a789cdcdb41c8b590ec6e528a5c09e4deb78a65ae158862e51c1948edf03f90071dd5a194606'
client = MongoClient('localhost', 27017)
my_database = client.VKkinder
meet_collection = my_database['SweetMeet']

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
        'fields' : 'sex, bdate, books, city, home_town, education, interests, movies, music, personal, relation',
        'v': '5.101'
    }

    user_info = requests.get(URL, params).json()

    return user_info['response'][0]


def search_users(user_info):

    search_results = list()

    def define_sex(user_sex):
        if user_sex == 1:
            partner_sex = 2
        else:
            partner_sex =1
        return partner_sex

    URL = 'https://api.vk.com/method/users.search'

    user_age = datetime.now().year - int(user_info['bdate'].split('.')[2])
    age_from = user_age - 7
    age_to = user_age + 7 
    user_city = user_info['city']['id']
    sex = define_sex(user_info['sex'])

    end_age = 0
    i = 0
    while end_age < age_to:
        i += 1
        start_age = age_from + i
        end_age = start_age
    
        params = {
            'access_token': token,
            'sort' : 1,
            'count' : 200,
            'age_from' : start_age,
            'age_to' : end_age,
            'city' : user_city,
            'sex' : sex,
            'fields' : 'bdate, sex, status, interests, books, movies, music, domain, photo_100, relation, verified,personal, followers_count, occupation, city',
            'v': '5.101'
        }

        result = requests.get(URL, params).json()

        for record in result['response']['items']:
            if record not in search_results:
                search_results.append(record)

        time.sleep(1)

    return search_results


def get_found_users(search_result):

    candidates = []

    for candidate in search_result:

        candidates.append(
            {
                        'user_id' : candidate.get('id'),
                        'bdate' : candidate.get('bdate'),
                        'books' : candidate.get('books'),
                        'first_name' : candidate.get('first_name'),
                        'last_name' : candidate.get('last_name'),
                        'movies' : candidate.get('movies'),
                        'music' : candidate.get('music'),
                        'relation' : candidate.get('relation'),
                        'sex' : candidate.get('sex'),
                        'city' : candidate.get('city', {'occupation' : 'Нет данных'}).get('id'),
                        'photo_100' : candidate.get('photo_100'),
                        'alcohol' : candidate.get('personal',{'personal' : 'Нет данных'}).get('alcohol'),
                        'langs' : candidate.get('personal',{'personal' : 'Нет данных'}).get('langs'),
                        'life_main' : candidate.get('personal',{'personal' : 'Нет данных'}).get('life_main'),
                        'people_main' : candidate.get('personal',{'personal' : 'Нет данных'}).get('people_main'),
                        'political' : candidate.get('personal',{'personal' : 'Нет данных'}).get('political'),
                        'smoking' : candidate.get('personal',{'personal' : 'Нет данных'}).get('smoking'),
                        'religion' : candidate.get('personal',{'personal' : 'Нет данных'}).get('religion_id')
                    }
            )

    return candidates


if __name__ == "__main__":
    # получаем информацию о пользователе для которого делаем запрос
    user_info = get_user_info('denis.novik')
    # выполняем запрос
    search_result = search_users(user_info)
    # пишем данные в базу
    meet_collection.insert_many(search_result)
    candidates = pd.DataFrame(get_found_users(search_result))
    candidates = candidates[[
        'user_id', 'first_name', 'last_name', 
        'bdate', 'city', 'sex', 'religion', 'relation', 'alcohol',  'smoking', 'life_main', 
        'people_main', 'political', 'langs', 'movies', 'music', 'photo_100']]
    free_persons = candidates[candidates['relation'].isin([1,6])]



'''1 — не женат/не замужем;
2 — есть друг/есть подруга;
3 — помолвлен/помолвлена;
4 — женат/замужем;
5 — всё сложно;
6 — в активном поиске;
7 — влюблён/влюблена;
8 — в гражданском браке;
0 — не указано.

alcohol (integer) — отношение к алкоголю. Возможные значения:
1 — резко негативное;
2 — негативное;
3 — компромиссное;
4 — нейтральное;
5 — положительное.

people_main (integer) — главное в людях. Возможные значения:
1 — ум и креативность;
2 — доброта и честность;
3 — красота и здоровье;
4 — власть и богатство;
5 — смелость и упорство;
6 — юмор и жизнелюбие.

life_main (integer) — главное в жизни. Возможные значения:
1 — семья и дети;
2 — карьера и деньги;
3 — развлечения и отдых;
4 — наука и исследования;
5 — совершенствование мира;
6 — саморазвитие;
7 — красота и искусство;
8 — слава и влияние;
'''

# TO DO 
# Написать функцию получения id пользователя 
# Написать функцию получения трех фото пользователя на основе лайка
# Написать функцию получения списка групп и добавления их в базу 