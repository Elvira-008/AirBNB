from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import (UserViewSet, ImagePropertyViewSet, AmenityViewSet,
                    PropertyListApiview, PropertyDetailAPView,
                    BookingListAPView,BookingViewSet,
                    ReviewListAPView, CityViewSet,
                    CustomLoginView, LogoutView,
                    BookingCreateAPView, BookingAllAPView)

router = SimpleRouter()
router.register('city', CityViewSet)
router.register('auth/users', UserViewSet)
router.register('images', ImagePropertyViewSet)
router.register('amenities', AmenityViewSet)
router.register('bookings/admin', BookingViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('properties/', PropertyListApiview.as_view(), name='property-list'),
    path('properties/<int:pk>/', PropertyDetailAPView.as_view(), name='property-detail'),
    #path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('bookings/', BookingListAPView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/', BookingAllAPView.as_view(), name='booking-all'),
    path('bookings/create/', BookingCreateAPView.as_view(), name='booking-create'),
    path('reviews/', ReviewListAPView.as_view(), name='review-edit'),

]


