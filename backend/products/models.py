from django.db import models

from user_managment.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
   
    def __str__(self):
        return self.name


# Subcategory Model
class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class HouseType(models.Model):
    name = models.CharField(max_length=255,unique=True)    
class CarType(models.Model):
    name = models.CharField(max_length=255 ,unique=True)     
class Banks(models.Model):
    name = models.CharField(max_length=255 ,unique=True)     
    bank_icon = models.ImageField(upload_to='bank_icons/', blank=True, null=True, help_text="Upload the bank's icon")

sell_or_rent =  [
         ('Sale', 'Sale'),
          ('Rent', 'Rent'),
        
       
           ]
approval=[
    ('Pending','Pending'),
    ('Approved','Approved'),
]
payment_status=[(
    'Pending','Pending'
),
                ('Paid','Paid')
                
                ]
# Product Model
Regions=[(
    'Addis Ababa','Addis Ababa'
),
                ('Amhara','Amhara')
                
                ]
import uuid
import os
def get_upload_path(instance, filename):
   
    # Extract the file extension
    ext = filename.split('.')[-1]
    # Create a unique filename using UUID
    unique_filename = f'{uuid.uuid4()}.{ext}'
    # Get the model name (lowercase)
    model_name = instance.__class__.__name__.lower()
    # Return the upload path, organized by model name
    return os.path.join(model_name, unique_filename)

class ItemCommonProperty(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='itemcommonproperty', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, related_name='itemcommonproperty', on_delete=models.CASCADE ,null=True,blank=True)
    city=models.CharField(choices=Regions, max_length=50,blank=True,null=True)
    sell_or_rent = models.CharField(choices=sell_or_rent, max_length=50,null=True,blank=True) # 'For ' or 'For Rent'
    price = models.DecimalField(max_digits=10, decimal_places=2)
    productimage = models.FileField(upload_to=get_upload_path,blank=True, null=True )
    image_url = models.JSONField()  # Use JSON to store list of image URLs
    description = models.TextField(blank=True,null=True)
    service_fee_bank=models.ForeignKey(Banks, related_name='ServiceCommonProperty', on_delete=models.CASCADE,blank=True,null=True)
    fee_recipt=models.ImageField(upload_to="Servicefee_images", default="payment.jpg",blank=True,null=True)
    fee_recipt_number=models.CharField( max_length=100,blank=True,null=True) 
    approval_status = models.CharField(choices=approval,default='Pending', max_length=50)  # 'For Sale' or 'For Rent'
    payment_status = models.CharField(max_length=50,default='Pending',choices=payment_status)  # 'Paid', '', etc.
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Latitude of the location",blank=True,null=True)  
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Longitude of the location",blank=True,null=True)  
    
    def __str__(self):
        return self.name
 

class ServiceCommonProperty(models.Model):
    
    category = models.ForeignKey(Category, related_name='ServiceCommonProperty', on_delete=models.CASCADE)
    city=models.CharField(choices=Regions, max_length=50,blank=True,null=True)
    description = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    serviceimage = models.ImageField(upload_to="product_images", default="default.jpg",blank=True,null=True)
    image_url = models.JSONField()  # Use JSON to store list of image URLs
    service_fee_bank=models.ForeignKey(Banks, related_name='Service_ServiceCommonProperty', on_delete=models.CASCADE,blank=True,null=True)
    fee_recipt=models.ImageField(upload_to="Servicefee_images", default="servicepayment.jpg",blank=True,null=True)
    fee_recipt_number=models.CharField( max_length=100,blank=True,null=True) 
    approval_status = models.CharField(choices=approval,default='Pending', max_length=50)  # 'For Sale' or 'For Rent'
    payment_status = models.CharField(max_length=50,default='Pending',choices=payment_status)  # 'Paid', '', etc.
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Latitude of the location",blank=True,null=True)  
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Longitude of the location",blank=True,null=True)  
    
    def __str__(self):
        return {self.name}
        

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} is watching {self.item}"