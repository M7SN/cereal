from django.contrib import admin

from main.models import Cereal, Manufacturer, Nutrition
# Register your models here.

admin.site.register(Cereal)
admin.site.register(Manufacturer)
admin.site.register(Nutrition)