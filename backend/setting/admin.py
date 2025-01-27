from django.contrib import admin
from .models import SilesraBankAccount, CustomerBank, GeneralSetting, Category, carMake, CarType, OtherItemCategory, BusienssOrServiceType

class SilesraBankAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_number', 'bank_icon')
    search_fields = ('name', 'account_number')
    list_filter = ('name',)

class CustomerBankAdmin(admin.ModelAdmin):
    list_display = ('name', 'bank_icon')
    search_fields = ('name',)
    
class GeneralSettingAdmin(admin.ModelAdmin):
    list_display = ('service_call_number', 'Default_bank_account')
    search_fields = ('service_call_number',)
    list_filter = ('Default_bank_account',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class OtherItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BusienssOrServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Registering models with customized admin configurations
admin.site.register(SilesraBankAccount, SilesraBankAccountAdmin)
admin.site.register(CustomerBank, CustomerBankAdmin)
admin.site.register(GeneralSetting, GeneralSettingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(carMake, CarMakeAdmin)
admin.site.register(CarType, CarTypeAdmin)
admin.site.register(OtherItemCategory, OtherItemCategoryAdmin)
admin.site.register(BusienssOrServiceType, BusienssOrServiceTypeAdmin)
