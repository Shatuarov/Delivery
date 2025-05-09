# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import RestaurantViewSet, MenuItemViewSet, CustomerViewSet, OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
