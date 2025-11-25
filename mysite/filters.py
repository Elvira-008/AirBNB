from django_filters import filterset
from .models import Property

class PropertyFilter(filterset.FilterSet):
    class Meta:
        model = Property
        fields = {
            'price_per_night': ['gt','lt'],
            'max_guests': ['gt','lt'],

        }



