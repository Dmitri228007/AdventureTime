import requests


def coord(token, place):
    geocoder_request = f'''http://geocode-maps.yandex.ru/1.x/?apikey={token}&geocode={place}&format=json'''
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        cord = str(toponym["Point"]['pos']).split()
        return cord


def organization(token, place):
    geocoder_request = f'''https://search-maps.yandex.ru/v1/?text={place}&type=biz&lang=en_US&apikey={token}'''
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        cord = str(toponym["Point"]['pos']).split()
        return cord


def __place(token, place, lg='ru_RU', num=10):
    geocoder_request = f'''https://search-maps.yandex.ru/v1/?text={place}&type=biz&lang={lg}&apikey={token}&results={num}'''
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        return json_response


if __name__ == '__main__':
    print(__place('633870d0-426c-43c5-96ee-be30e550827e', 'Австралия'))
