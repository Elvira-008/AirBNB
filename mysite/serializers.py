from rest_framework import serializers
from .models  import (User, Property, ImageProperty, City,
                     Booking, Review, Amenity)

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status', 'date_registered')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','user_name','email','avatar']


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']


class ImagePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProperty
        fields = ['image']


class PropertyListSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    images = ImagePropertySerializer()
    get_avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['id', 'city', 'title', 'images', 'price_per_night', 'get_avg_rating']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()


class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'check_in', 'check_out']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ReviewSerializers(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format= 'd% H%')
    guest = UserNameSerializer()

    class Meta:
        model = Review
        fields = ['created_at', 'guest', 'rating', 'comment']


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['amenity_name']


class PropertyDetailSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True)
    city = CitySerializer()
    images = ImagePropertySerializer(many=True)
    owner = UserNameSerializer()
    review = ReviewSerializers(many=True)

    class Meta:
        model = Property
        fields = ['id', 'title', 'description', 'price_per_night', 'city', 'address',
                  'property_type', 'rules', 'max_guests', 'bed_rooms', 'bath_rooms',
                  'bath_rooms', 'images', 'owner', 'review']
