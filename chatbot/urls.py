from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_page),
    path('api/send_message/', views.food_delivery_chatbot),
]
