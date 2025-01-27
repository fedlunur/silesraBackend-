from django.contrib import admin
from .models import *
@admin.register(ItemCommonProperty)
class ItemCommonPropertyAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'category', 
        'subcategory', 
        'city', 
        'sell_or_rent', 
        'price', 
        'approval_status', 
        'payment_status'
    )
    search_fields = ('name', 'category__name', 'subcategory__name', 'city')
    list_filter = ('category', 'subcategory', 'sell_or_rent', 'approval_status', 'payment_status', 'city')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name','category' )
    search_fields = ('name','category' )

@admin.register(HouseType)
class HouseTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

@admin.register(Banks)
class BanksAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
from django.contrib import admin
from .models import Watchlist

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'content_type', 'object_id', 'added_at')
    list_filter = ('user', 'content_type', 'added_at')
    search_fields = ('user__username', 'content_type__model', 'object_id')
    date_hierarchy = 'added_at'

    def get_queryset(self, request):
        """
        Optimize the query to prefetch related content types for performance.
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'content_type')
