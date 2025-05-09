# orders/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderForm
from .models import Customer

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .predictor import DeliveryIssuePredictor

class OrderIssuePredictionView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        predictor = DeliveryIssuePredictor()
        result = predictor.predict(order)
        return Response(result, status=status.HTTP_200_OK)

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_create(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        return redirect('profile_create')  # Страница создания профиля клиента (пока можно заглушку)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.save()
            return redirect('order_list')
    else:
        form = OrderForm()

    return render(request, 'orders/order_create.html', {'form': form})