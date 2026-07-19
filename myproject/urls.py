from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from booking_system.views import (
    RegistrationViewSet,
    HotelViewSet,
    FlightViewSet,
    HotelBookingViewSet,
    FlightBookingViewSet)
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r"register",RegistrationViewSet, basename = 'register')
router.register(r"hotels",HotelViewSet, basename = 'hotel')
router.register(r"flight",FlightViewSet, basename = 'flight')
router.register(r"hotel_booking",HotelBookingViewSet, basename = 'hotel_booking')
router.register(r"flight_booking",FlightBookingViewSet, basename = 'flight_booking')







urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

]
