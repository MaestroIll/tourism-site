"""
URL configuration for index project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views  # импортируем views из приложения blog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('tour/<int:tour_id>/booking/', views.create_booking, name='create_booking'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/payment/', views.create_payment, name='create_payment'),
]


