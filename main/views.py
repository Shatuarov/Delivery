# main/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from orders.models import Order
from restaurants.models import Restaurant

def home(request):
    # Получаем последние 4 заказа
    orders = Order.objects.all().order_by('-created_at')[:4]
    # Получаем 4 ресторана (можно добавить логику для "популярных")
    restaurants = Restaurant.objects.all()[:4]
    return render(request, 'main/home.html', {
        'orders': orders,
        'restaurants': restaurants,
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})