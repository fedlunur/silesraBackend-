from django.contrib import admin
from django.utils.html import format_html
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .models import (
    Car, House, OtherItem, Accessory, Fashion, Electronics, JobVacancy, 
    ServiceOrBusinessType, LostOrFound, FreeStaffOrItem, ListingImage
)
# Inline Image Display in the Form
@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'object_id', 'imagepath', 'uploaded_at', 'preview')  # Controls main admin columns
    readonly_fields = ('preview',)  # Make preview read-only in form view

    def preview(self, obj):
        """Displays image previews in the DataTable."""
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit: cover;"/>', obj.image.url)
        return "No Image"

    preview.short_description = "Preview"

# Inline Image Display in Forms (nested within other models)
class ListingImageInline(GenericTabularInline):
    model = ListingImage
    extra = 1  
    readonly_fields = ('preview',)  # Inline forms don't use list_display

    def preview(self, obj):
        """Displays image previews in the inline form."""
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit: cover;"/>', obj.image.url)
        return "No Image"
    
    preview.short_description = "Preview"

class BaseListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'category', 'approvalStatus', 'paymentStatus', 'created', 'updated', 'display_image','recipt_image')
    list_filter = ('city', 'approvalStatus', 'paymentStatus', 'created', 'updated')
    search_fields = ('name', 'phonenumber')
    readonly_fields = ('created', 'updated')
    inlines = [ListingImageInline]

    fieldsets = [
        ("General Info", {"fields": ("name", "city", "category", "price", "sell_or_rent")}),
        ("Approval & Payment", {"fields": ("approvalStatus", "paymentStatus")}),
        ("Location", {"fields": ("latitude", "longitude")}),
        ("Contact", {"fields": ("phonenumber",)}),
        ("Status", {"fields": ("removed",)}),
        ("Timestamps", {"fields": ("created", "updated"), "classes": ("collapse",)}),
    ]

    def display_image(self, obj):
   
        images = ListingImage.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id
        )
    
   
        valid_images = [image for image in images if image.image and hasattr(image.image, 'url')]
        
        if valid_images:
            image_urls = [image.image.url for image in valid_images]
            first_image_url = image_urls[0]  # Use the first valid image as a thumbnail preview
            
            # Creating the modal trigger and passing image URLs as data attributes
            return format_html(
                '<a href="#" class="open-slider" data-images="{}">'
                '<img src="{}" width="100" height="75" style="object-fit: cover;"/>'
                '</a>',
                ",".join(image_urls),  # Passing all image URLs as a comma-separated string
                first_image_url  # Thumbnail image URL
            )
        
        return "No Image"
        
    def display_recipt(self, obj):
     
        if obj.feeReciptImagePath:
     
            try:
                return format_html(
                    '<img src="{}" width="100" height="65" style="object-fit: cover;"/>',
                    obj.feeReciptImage.url  # Use the fee receipt image URL
                )
            except ValueError:
                return "Invalid Image"  # In case the image URL is not valid or the image is missing
        return "No Image"  # Fallback if no receipt image is present
 
    display_image.short_description = "Preview Image"
    display_recipt.short_description = "Receipt"
    
    class Media:
        js = ('admin/js/image_slider.js',)
        css = {'all': ('admin/css/image_slider.css',)}

# Admin classes for specific models
class CarAdmin(BaseListingAdmin):
    list_display = ('model', 'carMake', 'carType', 'price', 'sell_or_rent', 'display_image')
    list_filter = ('sell_or_rent', 'carMake', 'carType')
    search_fields = ('model', 'carMake__name', 'carType__name')

    fieldsets = [("Car Details", {"fields": ("model", "carMake", "carType")})] + BaseListingAdmin.fieldsets

class HouseAdmin(BaseListingAdmin):
    list_display = ('houseType', 'numberofBedrooms', 'numberofBathrooms', 'price', 'sell_or_rent', 'display_image')
    list_filter = ('sell_or_rent', 'houseType')
    search_fields = ('houseType',)

    
    fieldsets = [("House Details", {"fields": ("houseType", "numberofBedrooms", "numberofBathrooms")})] + BaseListingAdmin.fieldsets



class OtherItemAdmin(BaseListingAdmin):
    list_display = ('title', 'otherItemcategory', 'price', 'sell_or_rent', 'display_image')
    list_filter = ('sell_or_rent', 'otherItemcategory')
    search_fields = ('title',)

class AccessoryAdmin(BaseListingAdmin):
    list_display = ("accessoryType", "brand", "condition", "price", "display_image")
    list_filter = ("brand", "condition")
    search_fields = ("accessoryType", "brand", "description")

class FashionAdmin(BaseListingAdmin):
    list_display = ("fashionType", "brand", "size", "gender", "condition", "price", "display_image")
    list_filter = ("brand", "gender", "condition", "size")
    search_fields = ("fashionType", "brand", "description")

class ElectronicsAdmin(BaseListingAdmin):
    list_display = ("electronicsType", "brand", "model", "condition", "warranty", "price", "display_image")
    list_filter = ("brand", "condition", "warranty")
    search_fields = ("electronicsType", "brand", "model", "description")

class JobVacancyAdmin(BaseListingAdmin):
    list_display = ('positionTitle', 'companyName', 'positionType', 'salary', 'approvalStatus', 'display_image')
    list_filter = ('positionType', 'experianceLevel', 'approvalStatus')
    search_fields = ('positionTitle', 'companyName')

class ServiceOrBusinessTypeAdmin(BaseListingAdmin):
    list_display = ('name', 'busienssOrServiceType', 'payment', 'approvalStatus', 'display_image')
    list_filter = ('busienssOrServiceType', 'approvalStatus')
    search_fields = ('name',)

class LostOrFoundAdmin(BaseListingAdmin):
    list_display = ('Title', 'typeofadd', 'approvalStatus', 'display_image')
    list_filter = ('typeofadd', 'approvalStatus')
    search_fields = ('Title',)

class FreeStaffOrItemAdmin(BaseListingAdmin):
    list_display = ('title', 'description', 'created', 'display_image')
    search_fields = ('title', 'description')

class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'uploaded_at', 'display_image',)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit: cover;"/>', obj.image.url)
        return "No Image"

    display_image.short_description = "Preview Image"

# Register models with custom admin views
admin.site.register(Car, CarAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(OtherItem, OtherItemAdmin)
admin.site.register(Accessory, AccessoryAdmin)
admin.site.register(Fashion, FashionAdmin)
admin.site.register(Electronics, ElectronicsAdmin)
admin.site.register(JobVacancy, JobVacancyAdmin)
admin.site.register(ServiceOrBusinessType, ServiceOrBusinessTypeAdmin)
admin.site.register(LostOrFound, LostOrFoundAdmin)
admin.site.register(FreeStaffOrItem, FreeStaffOrItemAdmin)


class CustomAdminSite(admin.AdminSite):
    site_header = "Silesra Admin"
    site_title = "Silesra Admin Panel"
    index_title = "Welcome to Silesra Admin"

    def get_app_list(self, request):
        """Custom sorting for models in the admin panel."""
        app_list = super().get_app_list(request)
        for app in app_list:
            if app["app_label"] == "backend":
                sort_order = {
                    "Car": 1, "House": 2, "OtherItem": 3, "Accessory": 4, "Fashion": 5,
                    "Electronics": 6, "JobVacancy": 7, "ServiceOrBusinessType": 8,
                    "LostOrFound": 9, "FreeStaffOrItem": 10, "ListingImage": 11
                }
                app["models"].sort(key=lambda x: sort_order.get(x["object_name"], 99))
        return app_list

custom_admin_site = CustomAdminSite(name="custom_admin")
