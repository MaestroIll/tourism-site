from django import forms
from .models import Booking, Payment, Client, Hotel, Transport

class BookingForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), label="Клиент")
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), label="Отель")
    transport = forms.ModelChoiceField(queryset=Transport.objects.all(), label="Транспорт")
    status = forms.ChoiceField(choices=Booking.STATUS_CHOICES, label="Статус бронирования")

    class Meta:
        model = Booking
        fields = ['client', 'hotel', 'transport', 'status']


class PaymentForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices=Payment.PAYMENT_METHODS, label="Метод оплаты")

    class Meta:
        model = Payment
        fields = ['amount', 'payment_method']
