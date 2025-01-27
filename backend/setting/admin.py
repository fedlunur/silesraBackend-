from django.contrib import admin

from django.contrib import admin
from .models import SilesraBankAccount, GeneralSetting
from django.utils.html import format_html

@admin.register(SilesraBankAccount)
class SilesraBankAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_number', 'bank_icon_display')
    search_fields = ('name', 'account_number')
    list_filter = ('name',)

    def bank_icon_display(self, obj):
        """
        Display a small preview of the bank icon in the admin interface.
        """
        if obj.bank_icon:
            return format_html("<img src='{}' style='height: 40px;' />", obj.bank_icon.url)
        return "No Icon"
    bank_icon_display.short_description = "Bank Icon"
    bank_icon_display.short_description = "Bank Icon"
    bank_icon_display.allow_tags = True

@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):
    list_display = ('service_call_number', 'default_bank_account')
    search_fields = ('service_call_number',)
    autocomplete_fields = ('Default_bank_account',)

    def default_bank_account(self, obj):
        """
        Display the default bank account as a combination of name and account number.
        """
        if obj.Default_bank_account:
            return f"{obj.Default_bank_account.name} - {obj.Default_bank_account.account_number}"
        return "No Default Account"
    default_bank_account.short_description = "Default Bank Account"

