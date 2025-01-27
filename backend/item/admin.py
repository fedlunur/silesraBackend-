from django.contrib import admin
from .models import *

@admin.register(Cars)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'city', 'sell_or_rent', 'price', 'fuelType', 'model', 'year')
    search_fields = ('name', 'model', 'fuelType', 'city')
    list_filter = ('category', 'sell_or_rent', 'fuelType', 'city')

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'city', 'sell_or_rent', 'price', 'houseType', 'numberofBedrooms', 'numberofBathrooms')
    search_fields = ('name', 'houseType', 'city')
    list_filter = ('category', 'sell_or_rent', 'houseType', 'city')
