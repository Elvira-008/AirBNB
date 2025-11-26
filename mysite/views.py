from rest_framework import viewsets, generics, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .permissions import *
from .models import User, Property, ImageProperty, City, Booking, Review, Amenity
from .serializers import ( UserSerializer, UserNameSerializer, ImagePropertySerializer, PropertyListSerializer,
                          PropertyDetailSerializer, UserRegisterSerializer, LoginSerializer,
                          CitySerializer, BookingListSerializer,
                          ReviewSerializers, BookingSerializer, AmenitySerializer)

from .filters import PropertyFilter

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class ImagePropertyViewSet(viewsets.ModelViewSet):
    queryset = ImageProperty.objects.all()
    serializer_class = ImagePropertySerializer


class PropertyListApiview(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'address','city_name']
    ordering_fields = ['price_per_night', 'property_type']
    permissions_class = [permissions.AllowAny]


class PropertyDetailAPView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer
    permission_classes = [permissions.AllowAny]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class BookingListAPView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer


class BookingAllAPView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [CheckCreateBooking]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [CheckCreateBooking]


class BookingCreateAPView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [CheckCreateBooking]

    def get_queryset(self):
        return Booking.objects.filter(gosts=self.request.user)


class ReviewListAPView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer



