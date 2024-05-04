from maps import __place
from tokens import map_search_api_token as token


def get_hotels(jsn):
    phone = '\n\t\t'
    answer = ''
    for phones in jsn['properties']['CompanyMetaData']['Phones']:
        phone += f'''{phones['formatted']}\n\t\t'''
    answer += (
        f'''название отеля: {jsn['properties']['name']}\n\tадрес: {jsn['properties']['description']}
    сайт: {jsn['properties']['CompanyMetaData']['url']}\n\tчасы работы: {jsn['properties']['CompanyMetaData']['Hours']['text']}
    телефоны: {phone}\n'''
    )
    return answer


def question_info(response, num=10):
    place = __place(token, response, num=num)
    for p in place['features']:
        for _ in p['properties']['CompanyMetaData']['Categories']:
            if _['class'] == 'hotels':  # отели
                print(get_hotels(p))
            elif _['class'] == 'landmark':  # достопремечательности
                pass
            elif _['class'] == 'currency exchange':  # Обмен валюты
                pass


if __name__ == '__main__':
    r = input()
    question_info(r)
