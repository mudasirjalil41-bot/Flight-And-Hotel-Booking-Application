from django.contrib import admin
from .models import Hotel, Flight, FlightBooking, HotelBooking

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ["name", "city", 'rooms', 'price']
    list_filter = ["city"]
    search_fields = ["name", "city"]
    list_editable = ['rooms', 'price']


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['airline','flight_number',"origin", "destination", 'seats', 'price']
    list_filter =  ["origin", "destination"]
    search_fields = ["origin", "destination"]
    list_editable = ['seats', 'price']


@admin.register(FlightBooking)
class FlightBookingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", 'flight', 'paid', 'booking_date', 'created_at']
    list_filter = ["booking_date", "created_at"]
    search_fields = ["user__username", "user__email", 'flight__origin', 'flight__destination']
    readonly_fields = ["paid", 'created_at']


@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", 'hotel', 'paid', 'booking_date', 'created_at']
    list_filter = ["booking_date", "created_at"]
    search_fields = ["user__username", "user__email", 'hotel__name', 'hotel__city']
    readonly_fields = ["paid", 'created_at']