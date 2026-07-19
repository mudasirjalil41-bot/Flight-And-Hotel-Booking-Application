from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
    name = models.CharField(max_length=222)
    city = models.CharField(max_length=100, db_index=True)
    rooms = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.city}"


class Flight(models.Model):
    flight_number = models.CharField(max_length=20, default="PK-000")
    airline = models.CharField(max_length=100, default="PIA")
    origin = models.CharField(max_length=100, db_index=True)
    destination = models.CharField(max_length=100, db_index=True)
    seats = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flight_number} ({self.airline}) - {self.origin} to {self.destination}"


class HotelBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_hotel_bookings")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="hotel_bookings")
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Hotel Booking {self.id} | User: {self.user.username} | Hotel: {self.hotel.name}"


class FlightBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_flight_bookings")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="flight_bookings")
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)


    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Flight Booking {self.id} | User: {self.user.username} | Route: {self.flight.origin} -> {self.flight.destination}"
