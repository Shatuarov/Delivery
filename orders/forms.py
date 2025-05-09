# orders/forms.py
from django import forms
from .models import Order, OrderItem
from restaurants.models import MenuItem


class OrderForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Блюда'
    )

    class Meta:
        model = Order
        fields = ['restaurant', 'delivery_address', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['items'].label_from_instance = lambda obj: f"{obj.name} - ${obj.price}"

    def save(self, commit=True):
        order = super().save(commit=False)

        # Получаем данные о количестве из POST
        items = self.cleaned_data.get('items', [])
        total_price = 0
        for item in items:
            quantity = int(self.data.get(f'quantity_{item.id}', 1))  # Получаем количество из POST
            total_price += item.price * quantity

        order.total_price = total_price if total_price else 0

        if commit:
            order.save()
            OrderItem.objects.filter(order=order).delete()
            for item in items:
                quantity = int(self.data.get(f'quantity_{item.id}', 1))
                OrderItem.objects.create(order=order, menu_item=item, quantity=quantity)
        return order