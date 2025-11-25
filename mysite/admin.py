from django.contrib import admin
from .models import User, Property, City, Booking, Review, Amenity, ImageProperty
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin

class ImagePropertyInline(admin.TabularInline):
    model = ImageProperty
    extra = 1


@admin.register(Property)
class PropertyAdmin(TranslationAdmin):
    inlines = [ImagePropertyInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(User)
admin.site.register(City)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Amenity)


