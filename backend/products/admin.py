from django.contrib import admin
from .models import *
from django import forms

# Define the form for each model
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['city', 'category', 'sell_or_rent', 'carMake', 'carType', 'transmission', 'fuelType', 'price', 'license', 'yearofMake', 'model', 'mileage', 'description', 'carimage', 'approvalStatus', 'paymentStatus', 'servicefeeBank', 'feeReciptImage', 'feeReciptRefnumber', 'latitude', 'longitude', 'phonenumber', 'removed', 'created', ]


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['city', 'category', 'sell_or_rent', 'houseType', 'numberofBedrooms', 'numberofBathrooms', 'area', 'price', 'license', 'description', 'houseimage', 'approvalStatus', 'paymentStatus', 'servicefeeBank', 'feeReciptImage', 'feeReciptRefnumber', 'latitude', 'longitude', 'phonenumber', 'removed', 'created', ]


class OtherItemForm(forms.ModelForm):
    class Meta:
        model = OtherItem
        fields = ['city', 'category', 'sell_or_rent', 'otherItemcategory', 'title', 'price', 'description', 'itemImage', 'approvalStatus', 'paymentStatus', 'servicefeeBank', 'feeReciptImage', 'feeReciptRefnumber', 'latitude', 'longitude', 'phonenumber', 'removed', 'created', ]


class JobVacancyForm(forms.ModelForm):
    class Meta:
        model = JobVacancy
        fields = ['city', 'category', 'positionType', 'companyName', 'positionTitle', 'worklocation', 'experianceLevel', 'salary', 'applicationDeadline', 'JobDescription', 'JobRequirment', 'approvalStatus', 'paymentStatus', 'servicefeeBank', 'feeReciptImage', 'feeReciptRefnumber', 'latitude', 'longitude', 'phonenumber', 'removed', 'created', ]


class ServiceOrBusinessTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceOrBusinessType
        fields = ['city', 'category', 'name', 'busienssOrServiceType', 'businessLocation', 'Title', 'payment', 'description', 'serviceImage', 'approvalStatus', 'paymentStatus', 'servicefeeBank', 'feeReciptImage', 'feeReciptRefnumber', 'latitude', 'longitude', 'phonenumber', 'removed', 'created', ]


class LostOrFoundForm(forms.ModelForm):
    class Meta:
        model = LostOrFound
        fields = ['city', 'category', 'typeofadd', 'Title', 'description', 'serviceImage', 'approvalStatus', 'paymentStatus', 'servicefeeBank', 'feeReciptImage', 'feeReciptRefnumber', 'latitude', 'longitude', 'phonenumber', 'removed', 'created', ]


class FreeStaffOrItemForm(forms.ModelForm):
    class Meta:
        model = FreeStaffOrItem
        fields = ['city', 'category', 'title', 'description', 'freeItemsImage', 'servicefeeBank', 'feeReciptImage', 'feeReciptRefnumber', 'approvalStatus', 'paymentStatus', 'latitude', 'longitude', 'phonenumber', 'removed', 'created', ]


class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ['user', 'content_type', 'object_id', 'removed', 'created', ]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'item', 'content', ]


# Register each model in the admin interface
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    form = CarForm
    list_display = ('city', 'category', 'sell_or_rent', 'model', 'price', 'approvalStatus', 'paymentStatus', 'created', )
    search_fields = ['model', 'price', 'category__name']
    list_filter = ('category', 'approvalStatus', 'paymentStatus')


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    form = HouseForm
    list_display = ('city', 'category', 'sell_or_rent', 'houseType', 'price', 'approvalStatus', 'paymentStatus', 'created', )
    search_fields = ['houseType', 'price', 'category__name']
    list_filter = ('category', 'approvalStatus', 'paymentStatus')


@admin.register(OtherItem)
class OtherItemAdmin(admin.ModelAdmin):
    form = OtherItemForm
    list_display = ('city', 'category', 'sell_or_rent', 'title', 'price', 'approvalStatus', 'paymentStatus', 'created', )
    search_fields = ['title', 'price', 'category__name']
    list_filter = ('category', 'approvalStatus', 'paymentStatus')


@admin.register(JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    form = JobVacancyForm
    list_display = ('city', 'category', 'positionTitle', 'companyName', 'salary', 'applicationDeadline', 'approvalStatus', 'paymentStatus', 'created', )
    search_fields = ['positionTitle', 'companyName', 'category__name']
    list_filter = ('category', 'approvalStatus', 'paymentStatus')


@admin.register(ServiceOrBusinessType)
class ServiceOrBusinessTypeAdmin(admin.ModelAdmin):
    form = ServiceOrBusinessTypeForm
    list_display = ('city', 'category', 'name', 'busienssOrServiceType', 'payment', 'approvalStatus', 'paymentStatus', 'created', )
    search_fields = ['name', 'payment', 'category__name']
    list_filter = ('category', 'approvalStatus', 'paymentStatus')


@admin.register(LostOrFound)
class LostOrFoundAdmin(admin.ModelAdmin):
    form = LostOrFoundForm
    list_display = ('city', 'category', 'typeofadd', 'Title', 'approvalStatus', 'paymentStatus', 'created', )
    search_fields = ['Title', 'category__name']
    list_filter = ('category', 'approvalStatus', 'paymentStatus')


@admin.register(FreeStaffOrItem)
class FreeStaffOrItemAdmin(admin.ModelAdmin):
    form = FreeStaffOrItemForm
    list_display = ('city', 'category', 'title', 'approvalStatus', 'paymentStatus', 'created', )
    search_fields = ['title', 'category__name']
    list_filter = ('category', 'approvalStatus', 'paymentStatus')


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    form = WatchlistForm
    list_display = ('user', 'item', 'removed', 'created', )
    search_fields = ['user__username', 'item__title']
    list_filter = ('removed', 'created')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    form = MessageForm
    list_display = ('sender', 'recipient', 'item', 'timestamp')
    search_fields = ['sender__username', 'recipient__username', 'item__title']
    list_filter = ('timestamp',)
