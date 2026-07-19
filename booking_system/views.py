from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from django.db import transaction
from django.utils import timezone
from .models import Flight,FlightBooking,Hotel,HotelBooking
from .serializers import RegistrationSerializer,HotelSerializer,FlightSerializer,FlightBookingSerializer,HotelBookingSerializer
from rest_framework import serializers


class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {"message":"User Registered successfully! You can now log in."},status = status.HTTP_201_CREATED
        )
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_permissions(self):
        if self.action in ["list",'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(),IsAdminUser()]

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_permissions(self):
        if self.action in ["list",'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(),IsAdminUser()]

class HotelBookingViewSet(viewsets.ModelViewSet):
        serializer_class = HotelBookingSerializer
        permission_classes = [IsAuthenticated]
        http_method_names = ["get", 'post', 'delete']

        def get_queryset(self):
            return HotelBooking.objects.filter(user=self.request.user)

        def perform_create(self, serializer):
            hotel_instance = serializer.validated_data.get("hotel")
            if not hotel_instance:
                raise serializers.ValidationError({"hotel":"Hotel field is required."})
            quantity = self.request.data.get("quantity",1)
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    raise serializers.ValidationError({"error":"minimum quantity required is 1"})
            except ValueError:
                raise serializers.ValidationError({"error":'Invalid quantity format.'})


            with transaction.atomic():
                locked_hotel = Hotel.objects.select_for_update().get(pk = hotel_instance.pk)

                if locked_hotel.rooms < quantity:
                    raise serializers.ValidationError({"error": "sorry no rooms available in this hotel."})

                locked_hotel.rooms -= quantity
                locked_hotel.save()
                total_bill = locked_hotel.price*quantity

                serializer.save(
                    user = self.request.user,
                    paid = total_bill,
                    quantity = quantity,
                    booking_date = timezone.now()

                )


        def destroy(self, request, *args, **kwargs):
            booking = self.get_object()
            if booking.user != request.user:
                return Response({
                    "error": "You do not have permission to cancel this booking."
                }, status=status.HTTP_403_FORBIDDEN)
            is_confirmed = request.query_params.get("confirm", 'false').lower() == 'true'
            if not is_confirmed:
                return Response({
                    "warning": "Are you sure you want to cancel this booking?",
                    "action_required": "To complete this cancellation, append '?confirm=true' to the end of the URL."
                }, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                hotel = Hotel.objects.select_for_update().get(id=booking.hotel.id)
                hotel.rooms += booking.quantity
                hotel.save()
                booking.delete()
            return Response(
                {
                    "message": "Hotel booking successfully cancelled.",
                    "details": f"{booking.quantity} rooms have been restored to hotel inventory."
                },
                status=status.HTTP_200_OK
            )


class FlightBookingViewSet(viewsets.ModelViewSet):
    serializer_class = FlightBookingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get",'post','delete']

    def get_queryset(self):
        return FlightBooking.objects.filter(user = self.request.user)

    def perform_create(self,serializer):
        flight_instance = serializer.validated_data.get("flight")
        if not flight_instance:
            raise serializers.ValidationError({"flight":"flight field is required."})
        quantity = self.request.data.get("quantity", 1)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise serializers.ValidationError({"error": "minimum quantity required is 1"})
        except ValueError:
            raise serializers.ValidationError({"error": 'Invalid quantity format.'})

        with transaction.atomic():
            locked_flight = Flight.objects.select_for_update().get(pk = flight_instance.pk)

            if locked_flight.seats < quantity:
                raise serializers.ValidationError({"error":"no seats available in this flight."})

            locked_flight.seats -= quantity
            locked_flight.save()
            total_bill = locked_flight.price*quantity
            serializer.save(
                user = self.request.user,
                paid = total_bill,
                quantity = quantity,
                booking_date = timezone.now()

            )



    def destroy(self,request,*args,**kwargs):
        booking = self.get_object()
        if booking.user != request.user:
            return Response({
                "error":"You do not have permission to cancel this booking."
            },status = status.HTTP_403_FORBIDDEN)
        is_confirmed = request.query_params.get("confirm",'false').lower() == 'true'
        if not is_confirmed:
            return Response({
                "warning":"Are you sure you want to cancel this booking?",
                "action_required": "To complete this cancellation, append '?confirm=true' to the end of the URL."
            },status = status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            flight = Flight.objects.select_for_update().get(id = booking.flight.id)
            flight.seats += booking.quantity
            flight.save()
            booking.delete()
        return Response(
                {
                    "message": "Flight booking successfully cancelled.",
                    "details": f"{booking.quantity} seats have been restored to flight inventory."
                },
                status=status.HTTP_200_OK
            )




