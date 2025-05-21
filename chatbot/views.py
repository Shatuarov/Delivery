from django.shortcuts import render
from django.http import JsonResponse

def chatbot_page(request):
    return render(request, "chatbot.html")

def food_delivery_chatbot(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "").lower()
        if "меню" in user_message:
            return JsonResponse({"response": "В нашем меню: пицца, суши, бургеры, салаты."})
        elif "где" in user_message and "заказ" in user_message:
            return JsonResponse({"response": "Ваш заказ в пути! Обычно доставка занимает до 40 минут."})
        elif "адрес" in user_message:
            return JsonResponse({"response": "Вы можете изменить адрес в вашем профиле или сообщите новый адрес здесь."})
        elif "отменить" in user_message:
            return JsonResponse({"response": "Ваш заказ был отменён. Надеемся, вы вернётесь позже!"})
        else:
            return JsonResponse({"response": "Извините, я не понял. Попробуйте задать вопрос о доставке, меню или заказе."})
