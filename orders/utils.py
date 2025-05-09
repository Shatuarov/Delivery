# orders/utils.py
import openrouteservice
from django.conf import settings

def geocode_address(address):
    client = openrouteservice.Client(key='YOUR_ORS_API_KEY')  # Замени на свой ключ
    try:
        result = client.pelias_search(address)
        if result['features']:
            coords = result['features'][0]['geometry']['coordinates']
            return coords[1], coords[0]  # latitude, longitude
    except Exception as e:
        print(f"Ошибка геокодирования: {e}")
    return None, None