from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
from .models import Hotel,Flight,FlightBooking,HotelBooking

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password],
        style = {'input_type': "password"}

    )
    email = serializers.EmailField(
        required = True,
        validators = [EmailValidator(message = "Enter a valid email address.")]
    )

    class Meta:
        model = User
        fields = ["username",'password','email']

    def validate_email(self,value):
            normalize_email = value.lower().strip()
            if User.objects.filter(email__iexact = normalize_email).exists():
                raise serializers.ValidationError("a user with this email already registered.")
            return normalize_email
    def validate_username(self,value):
        normalize_username = value.lower().strip()
        if User.objects.filter(username__iexact = normalize_username).exists():
            raise serializers.ValidationError("this user is already taken.")
        return normalize_username

    def create(self,validated_data):
        user = User.objects.create_user(
            username = validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"]
        )
        return user

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class HotelBookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    hotel_details = HotelSerializer(source = "hotel",read_only = True)
    hotel = serializers.PrimaryKeyRelatedField(queryset = Hotel.objects.all())
    quantity = serializers.IntegerField(required=True, min_value=1)
    class Meta:
        model = HotelBooking
        fields = ["id","user",'hotel',"quantity",'hotel_details','paid',"booking_date",'created_at']
        read_only_fields = ["paid",'created_at','booking_date']


class FlightBookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    flight_details = FlightSerializer(source="flight", read_only=True)
    flight = serializers.PrimaryKeyRelatedField(queryset = Flight.objects.all())
    quantity = serializers.IntegerField(required=True, min_value=1)


    class Meta:
        model = FlightBooking
        fields = ["id", "user", 'flight',"quantity", 'flight_details', 'paid', "booking_date", 'created_at']
        read_only_fields = ["paid",'booking_date','created_at']



