# api/serializers.py

from rest_framework import serializers
from restaurants.models import Restaurant, MenuItem
from orders.models import Order, Customer, OrderItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'restaurant']


class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone', 'menu_items']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'address']


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(), source='menu_item',
                                                      write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer',
                                                     write_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    order_items = OrderItemSerializer(source='order_items', many=True, read_only=True)
    items = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_id', 'restaurant', 'delivery_address', 'status', 'total_price',
                  'order_date', 'order_items', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total = 0
        for item in items_data:
            mi = item['menu_item']
            qty = item['quantity']
            OrderItem.objects.create(order=order, menu_item=mi, quantity=qty)
            total += mi.price * qty
        order.total_price = total
        order.save()
        return order
