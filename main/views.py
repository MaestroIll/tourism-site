from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Tour, Hotel, Transport, Booking, Payment
from .forms import BookingForm, PaymentForm 
from django.db.models import Q

# Главная страница: список всех туров

def home(request):
    query = request.GET.get('q', '').strip()
    if query:
        tours = Tour.objects.filter(
            Q(title__icontains=query) |
            Q(country__icontains=query) |
            Q(start_date__icontains=query)
        )
    else:
        tours = Tour.objects.all()
    return render(request, 'main/home.html', {'tours': tours, 'query': query})


# Страница отдельного тура
def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    hotels = Hotel.objects.filter(city=tour.country)  # Отели в стране тура
    transports = Transport.objects.all()  # Можно фильтровать по маршруту
    return render(request, 'main/tour_detail.html', {
        'tour': tour,
        'hotels': hotels,
        'transports': transports
    })


# Создание бронирования для выбранного тура
def create_booking(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            booking.save()
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'main/create_booking.html', {
        'form': form,
        'tour': tour
    })


# Просмотр информации о бронировании
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'main/booking_detail.html', {'booking': booking})


# Создание платежа для бронирования
def create_payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.save()
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = PaymentForm()
    
    return render(request, 'main/create_payment.html', {
        'form': form,
        'booking': booking
    })
