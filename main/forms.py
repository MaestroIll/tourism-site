# main/forms.py
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

    def __init__(self, *args, **kwargs):
        tour = kwargs.pop('tour', None)
        super().__init__(*args, **kwargs)
        if tour:
            self.fields['hotel'].queryset = Hotel.objects.filter(city=tour.country)


class PaymentForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices=Payment.PAYMENT_METHODS, label="Метод оплаты")

    class Meta:
        model = Payment
        fields = ['amount', 'payment_method']