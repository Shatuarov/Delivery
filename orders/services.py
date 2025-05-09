# orders/services.py
import openrouteservice
import requests
import pandas as pd
from django.conf import settings
from datetime import datetime
from .models import Order

class DeliveryDataService:
    def __init__(self):
        self.ors_client = openrouteservice.Client(key='YOUR_ORS_API_KEY')  # Замени на свой ключ
        self.weather_api_key = 'YOUR_OPENWEATHER_API_KEY'  # Замени на свой ключ

    def get_weather_data(self, lat, lon):
        """
        Получает погодные данные.
        :return: Температура (C), осадки (мм), тип погоды
        """
        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.weather_api_key}&units=metric'
            response = requests.get(url)
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            precipitation = weather_data.get('rain', {}).get('1h', 0)
            weather_type = weather_data['weather'][0]['main'].lower()
            return temperature, precipitation, weather_type
        except Exception as e:
            print(f"Ошибка получения погоды: {e}")
            return 20.0, 0.0, 'clear'  # Значения по умолчанию

    def get_route_data(self, origin, destination):
        """
        Получает данные о маршруте.
        :return: Расстояние (км), время (минуты)
        """
        try:
            route = self.ors_client.directions(
                coordinates=[origin, destination],
                profile='driving-car',
                preference='fastest',
                instructions=False
            )
            distance = route['routes'][0]['summary']['distance'] / 1000  # км
            duration = route['routes'][0]['summary']['duration'] / 60  # минуты
            return distance, duration
        except Exception as e:
            print(f"Ошибка получения маршрута: {e}")
            return 5.0, 15.0  # Значения по умолчанию

    def prepare_features(self, order):
        """
        Подготавливает признаки для ИИ.
        """
        # Данные о заказе
        item_count = order.orderitem_set.count()
        total_price = float(order.total_price)
        hour_of_day = order.created_at.hour

        # Данные о маршруте
        restaurant_coords = (order.restaurant.latitude, order.restaurant.longitude)
        delivery_coords = (order.latitude, order.longitude)
        distance, duration = self.get_route_data(restaurant_coords, delivery_coords)

        # Данные о погоде
        temperature, precipitation, weather_type = self.get_weather_data(order.latitude, order.longitude)
        is_rainy = 1 if weather_type in ['rain', 'snow', 'storm'] else 0

        return {
            'item_count': item_count,
            'total_price': total_price,
            'hour_of_day': hour_of_day,
            'distance': distance,
            'duration': duration,
            'temperature': temperature,
            'precipitation': precipitation,
            'is_rainy': is_rainy
        }

    def prepare_training_data(self):
        """
        Подготавливает данные для обучения модели.
        """
        orders = Order.objects.all()
        features = []
        labels = []

        for order in orders:
            feature_dict = self.prepare_features(order)
            features.append([
                feature_dict['item_count'],
                feature_dict['total_price'],
                feature_dict['hour_of_day'],
                feature_dict['distance'],
                feature_dict['duration'],
                feature_dict['temperature'],
                feature_dict['precipitation'],
                feature_dict['is_rainy']
            ])
            labels.append(1 if order.has_issue or order.status in ['CANCELLED', 'DELAYED'] else 0)

        return pd.DataFrame(features, columns=[
            'item_count', 'total_price', 'hour_of_day', 'distance', 'duration',
            'temperature', 'precipitation', 'is_rainy'
        ]), labels