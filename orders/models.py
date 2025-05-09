# orders/models.py
from django.db import models

class Customer(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)  # Широта адреса доставки
    longitude = models.FloatField(null=True, blank=True)  # Долгота адреса доставки
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'В ожидании'),
        ('IN_PROGRESS', 'В процессе'),
        ('DELIVERED', 'Доставлен'),
        ('CANCELLED', 'Отменен'),
        ('DELAYED', 'Задержан'),  # Добавляем статус "Задержан"
    ], default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    has_issue = models.BooleanField(default=False)  # Была ли проблема с заказом

    def __str__(self):
        return f"Order {self.id} by {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey('restaurants.MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity}) in Order {self.order.id}"

    def get_total(self):
        return self.menu_item.price * self.quantity