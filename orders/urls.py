# orders/urls.py
from django.urls import path
from .views import OrderIssuePredictionView
from . import views


urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/predict-issue/', OrderIssuePredictionView.as_view(), name='order_issue_prediction'),
]