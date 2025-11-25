from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_name = models.CharField(max_length=50)
    UserRoleChoices = (
        ('hosts', 'hosts'),
        ('guest', 'guest'),
    )
    role = models.CharField(max_length=30, choices=UserRoleChoices, default='hosts')
    phone_number = PhoneNumberField()
    avatar = models.ImageField(upload_to='user_image/')

    def __str__(self):
        return self.user_name

class City(models.Model):
    city_name = models.CharField(max_length=100)
    city_image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'{self.city_name}'

class Amenity(models.Model):
    amenity_name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='icon/', null=True, blank=True)

    def __str__(self):
        return f'{self.amenity_name}'


class Property(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price_per_night = models.PositiveIntegerField()
    PropertyChoices =(
    ('apartment', 'apartment'),
    ('house', 'house'),
    ('studio', 'studio'),
    )
    property_type = models.CharField(max_length=40, choices=PropertyChoices, default='house')
    RulesChoices = (
    ('no_smoking', 'no_smoking'),
    ('pets_allowed', 'pets_allowed'),
    ('etc', 'etc'),
    )
    rules = models.CharField(max_length=50, choices=RulesChoices)
    max_guests = models.PositiveIntegerField(default=1)
    bed_rooms = models.PositiveIntegerField(default=1)
    bath_rooms = models.PositiveIntegerField(default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    is_active = models.BooleanField(default=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_property', null=True, blank=True)
    address = models.CharField(max_length=100)
    amenities = models.ManyToManyField(Amenity, related_name='ss')

    def __str__(self):
        return self.title

    def get_avg_rating(self):
        rating = self.reviews.all()
        if rating.exists():
            return round(sum([i.rating for i in rating]) / rating.count(), 1)
        return 0

    def get_price_for_two_nights(self, nights: int = 1):
        return self.price_per_night * nights


class ImageProperty(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f'{self.property}'

class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    StatusPropertyChoices = (
    ('pending', 'pending'),
    ('approved', 'approved'),
    ('rejected', 'rejected'),
    ('cancelled', 'cancelled'),
    )
    status = models.CharField(max_length=15, choices=StatusPropertyChoices)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.check_in} {self.check_out}'

class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='review')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.comment}'






