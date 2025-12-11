from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
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


# Страница со всеми турами
def tours_page(request):
    """Страница со всеми турами"""
    query = request.GET.get('q', '').strip()
    country_filter = request.GET.get('country', '')
    sort_by = request.GET.get('sort', 'start_date')
    
    tours = Tour.objects.all()
    
    # Фильтрация по поиску
    if query:
        tours = tours.filter(
            Q(title__icontains=query) |
            Q(country__icontains=query)
        )
    
    # Фильтрация по стране
    if country_filter:
        tours = tours.filter(country__icontains=country_filter)
    
    # Сортировка
    if sort_by == 'price_asc':
        tours = tours.order_by('price')
    elif sort_by == 'price_desc':
        tours = tours.order_by('-price')
    elif sort_by == 'duration':
        tours = tours.order_by('-duration')
    elif sort_by == 'date':
        tours = tours.order_by('start_date')
    else:
        tours = tours.order_by('start_date')
    
    # Получаем список уникальных стран для фильтра
    countries = Tour.objects.values_list('country', flat=True).distinct().order_by('country')
    
    return render(request, 'main/tours_page.html', {
        'tours': tours,
        'query': query,
        'countries': countries,
        'selected_country': country_filter,
        'sort_by': sort_by,
    })


# Страница со всеми отелями
def hotels_page(request):
    """Страница со всеми отелями"""
    query = request.GET.get('q', '').strip()
    city_filter = request.GET.get('city', '')
    stars_filter = request.GET.get('stars', '')
    sort_by = request.GET.get('sort', 'name')
    
    hotels = Hotel.objects.all()
    
    # Фильтрация по поиску
    if query:
        hotels = hotels.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query)
        )
    
    # Фильтрация по городу
    if city_filter:
        hotels = hotels.filter(city__icontains=city_filter)
    
    # Фильтрация по звездам
    if stars_filter and stars_filter != 'all':
        hotels = hotels.filter(stars=stars_filter)
    
    # Сортировка
    if sort_by == 'price_asc':
        hotels = hotels.order_by('price_per_night')
    elif sort_by == 'price_desc':
        hotels = hotels.order_by('-price_per_night')
    elif sort_by == 'stars':
        hotels = hotels.order_by('-stars', 'name')
    elif sort_by == 'name':
        hotels = hotels.order_by('name')
    else:
        hotels = hotels.order_by('name')
    
    # Получаем списки для фильтров
    cities = Hotel.objects.values_list('city', flat=True).distinct().order_by('city')
    stars_choices = [1, 2, 3, 4, 5]
    
    return render(request, 'main/hotels_page.html', {
        'hotels': hotels,
        'query': query,
        'cities': cities,
        'stars_choices': stars_choices,
        'selected_city': city_filter,
        'selected_stars': stars_filter,
        'sort_by': sort_by,
    })


# Страница отдельного тура
def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    hotels = Hotel.objects.filter(city=tour.country)
    transports = Transport.objects.all()
    return render(request, 'main/tour_detail.html', {
        'tour': tour,
        'hotels': hotels,
        'transports': transports
    })


# Создание бронирования для выбранного тура
def create_booking(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, tour=tour)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            booking.save()
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm(tour=tour) 

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

    if booking.status == 'cancelled':
        messages.error(request, f'Невозможно создать платёж: бронирование #{booking.id} отменено.')
        return redirect('booking_detail', booking_id=booking.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.save()
            messages.success(request, f'Платёж на сумму {payment.amount} руб. успешно обработан для бронирования #{booking.id}.')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = PaymentForm()

    return render(request, 'main/create_payment.html', {
        'form': form,
        'booking': booking
    })