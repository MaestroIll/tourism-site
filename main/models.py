from django.db import models
from django.utils import timezone

class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    reg_date = models.DateField(default=timezone.now, verbose_name="Дата регистрации")

    def __str__(self):
        return self.name


class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название тура")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.IntegerField(verbose_name="Длительность (дней)")
    country = models.CharField(max_length=100, verbose_name="Страна")
    start_date = models.DateField(verbose_name="Дата начала")

    def __str__(self):
        return self.title


class Hotel(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название отеля")
    stars = models.IntegerField(verbose_name="Звёзды")
    city = models.CharField(max_length=100, verbose_name="Город")
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена за ночь")

    def __str__(self):
        return f"{self.name} ({self.city})"


class Transport(models.Model):
    type = models.CharField(max_length=100, verbose_name="Тип транспорта")
    company = models.CharField(max_length=100, verbose_name="Компания")
    departure = models.DateTimeField(verbose_name="Время отправления")
    arrival = models.DateTimeField(verbose_name="Время прибытия")
    route = models.CharField(max_length=200, verbose_name="Маршрут")

    def __str__(self):
        return f"{self.type} - {self.company}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    book_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def calculate_total_price(self):
        hotel_cost = self.hotel.price_per_night * self.tour.duration
        transport_cost = 5000
        return self.tour.price + hotel_cost + transport_cost

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Бронирование #{self.id} - {self.client.name}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('online', 'Онлайн-платёж'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    def __str__(self):
        return f"Платёж #{self.id} ({self.amount} руб.)"

