from django.contrib import admin
from .models import Client, Tour, Hotel, Transport, Booking, Payment


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'reg_date')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('reg_date',)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'duration', 'country', 'start_date')
    list_filter = ('country', 'start_date')
    search_fields = ('title', 'country')


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stars', 'city', 'price_per_night')
    list_filter = ('city', 'stars')
    search_fields = ('name', 'city')


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'company', 'route', 'departure', 'arrival')
    list_filter = ('company', 'type')
    search_fields = ('type', 'company', 'route')


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'tour', 'hotel', 'transport', 'book_date', 'status', 'total_price')
    readonly_fields = ('total_price',)
    list_filter = ('status', 'book_date')
    search_fields = ('client__name', 'tour__title', 'hotel__name')
    inlines = [PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'pay_date', 'payment_method')
    list_filter = ('payment_method', 'pay_date')

# Register your models here.
