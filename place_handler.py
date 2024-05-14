from maps import __place
from tokens import map_search_api_token as token


def get_hotels(jsn):
    phone = '\n\t\t'
    answer = ''
    for phones in jsn['properties']['CompanyMetaData']['Phones']:
        if phones['type'] == 'phone':
            phone += f'''{phones['formatted']}\n\t\t'''
    try:
        hours = jsn['properties']['CompanyMetaData']['Hours']['text']
        answer += (
            f'''название отеля: {jsn['properties']['name']}\n\tадрес: {jsn['properties']['description']}
        сайт: {jsn['properties']['CompanyMetaData']['url']}
        часы работы: {jsn['properties']['CompanyMetaData']['Hours']['text']}
        телефоны: {phone}''')
    except KeyError:
        answer += (
            f'''название отеля: {jsn['properties']['name']}\n\tадрес: {jsn['properties']['description']}
                сайт: {jsn['properties']['CompanyMetaData']['url']}
                телефоны: {phone}''')
    return answer


def get_landmark(jsn):
    answer = f'''Достопремичательность: {jsn['properties']['name']}\n\n'''
    hours = 'лучше уточнить'
    try:
        hours = jsn['properties']['CompanyMetaData']['Hours']['text']
    except KeyError:
        answer = ''
        answer += (
            f'''Достопремичательность: {jsn['properties']['name']}\n\tадрес: {jsn['properties']['description']}
        часы работы: {hours}''')
    finally:
        return answer


def get_exchange(jsn):
    phone = '\n\t\t'
    answer = ''
    for phones in jsn['properties']['CompanyMetaData']['Phones']:
        if phones['type'] == 'phone':
            phone += f'''{phones['formatted']}\n\t\t'''
    try:
        hours = jsn['properties']['CompanyMetaData']['Hours']['text']
        answer += (
            f'''Обменник: {jsn['properties']['name']}\n\tадрес: {jsn['properties']['description']}
            сайт: {jsn['properties']['CompanyMetaData']['url']}
            часы работы: {hours}
            телефоны: {phone}''')
    except KeyError:
        answer += (
            f'''Обменник: {jsn['properties']['name']}\n\tадрес: {jsn['properties']['description']}
                    сайт: {jsn['properties']['CompanyMetaData']['url']}
                    телефоны: {phone}''')
    return answer


def question_info(response, num=5):
    land = ''
    bank = ''
    hotels = ''
    answer = ''
    place = __place(token, response, num=num)
    for p in place['features']:
        for _ in p['properties']['CompanyMetaData']['Categories']:
            if _['class'] == 'hotels':  # отели
                hotels += get_hotels(p)
            elif _['class'] == 'landmark':  # достопремечательности
                land += get_landmark(p)
            elif _['class'] == 'currency exchange' or _['class'] == 'banks':  # Обмен валюты
                bank += get_exchange(p)
    if land:
        answer += land
    if bank:
        answer += bank
    if hotels:
        answer += hotels

    return answer


if __name__ == '__main__':
    r = input()
    print(question_info(r))
