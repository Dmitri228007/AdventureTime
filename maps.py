import requests
from tokens import map_static_api_token as map_token


def coord(token, place):
    geocoder_request = f'''http://geocode-maps.yandex.ru/1.x/?apikey={token}&geocode={place}&format=json'''
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        cord = str(toponym["Point"]['pos']).split()
        return cord
