from django.db import models

from user_managment.models import User
from .choices import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from setting.models import *
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
import uuid
import os
      

def upload_to(instance, filename):
   
    # Extract the file extension
    ext = filename.split('.')[-1]
    unique_filename = f'{uuid.uuid4()}.{ext}'
    model_name = instance.__class__.__name__.lower()
    
    return os.path.join(model_name, unique_filename)
class BaseListing(models.Model):
    name = models.CharField( max_length=100, blank=True, null=True)
    city = models.CharField(choices=Cities, max_length=50, blank=True, null=True)
    category = models.ForeignKey(Category, related_name='%(class)s', on_delete=models.CASCADE)
    approvalStatus = models.CharField(choices=approval, default='Pending', max_length=50,null=True,blank=True)
    paymentStatus = models.CharField(choices=payment_status, default='Pending', max_length=50,null=True,blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Latitude of the location", blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Longitude of the location", blank=True, null=True)
    phonenumber = models.CharField(max_length=50, blank=True, null=True)
    removed = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class ListingImage(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Reference to ContentType
    object_id = models.PositiveIntegerField()  # Foreign key to the model instance ID
    listing = GenericForeignKey('content_type', 'object_id')  # This links the image to any model via GenericForeignKey
    image = models.ImageField(upload_to='listing_images/')  # Store images in media/listing_images/
    imagepath = models.CharField(max_length=50, blank=True, null=True)  # Optional path to store image path
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp when image is uploaded
    
    def save(self, *args, **kwargs):
        """Override save method to store filename in imagepath."""
        if self.image and not self.imagepath:
            
            self.imagepath = os.path.basename(self.image.name)  # Save only the filename
        super().save(*args, **kwargs)  # Call the parent save method
    def __str__(self):
        return f"Image for {self.listing}" 
class ServiceFee(models.Model):
    contentType = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # Rename objectId to object_id
    catagory = GenericForeignKey('contentType', 'object_id')
    servicefeeBank = models.ForeignKey(CustomerBank, related_name='%(class)s', on_delete=models.CASCADE, blank=True, null=True)
    feeReciptImage = models.ImageField(upload_to="Servicefee_images/", default="payment.jpg", blank=True, null=True)
    feeReciptRefnumber = models.CharField(max_length=100, blank=True, null=True)


class Car(BaseListing):
    sell_or_rent = models.CharField(choices=sell_or_rent, max_length=50, null=True, blank=True)
    carMake = models.ForeignKey(carMake, related_name='car', on_delete=models.CASCADE)
    carType = models.ForeignKey(CarType, related_name='car', on_delete=models.CASCADE)
    transmission = models.CharField(choices=car_transmissions, max_length=50, blank=True, null=True)
    fuelType = models.CharField(choices=car_fuletypes, max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2 ,blank=True, null=True)
    license = models.CharField(choices=yes_no, max_length=50, blank=True, null=True)
    yearofMake = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    mileage = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
   

    def __str__(self):
        return self.model

        
class House(BaseListing):
    sell_or_rent = models.CharField(choices=sell_or_rent, max_length=50, null=True, blank=True)
    houseType = models.CharField(choices=housetypes, max_length=50, blank=True, null=True)
    numberofBedrooms = models.IntegerField(default=0)
    numberofBathrooms = models.IntegerField(default=0)
    area = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.houseType}"

class OtherItem(BaseListing):
    sell_or_rent = models.CharField(choices=sell_or_rent, max_length=50, null=True, blank=True)
    otherItemcategory = models.ForeignKey(OtherItemCategory, related_name='OtherItems', on_delete=models.CASCADE)
    title = models.CharField(choices=yes_no, max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
  
    def __str__(self):
        return f"{self.title}"

class Accessory(BaseListing):
    sell_or_rent = models.CharField(choices=sell_or_rent, max_length=50, null=True, blank=True)
    accessoryType = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.accessoryType} - {self.brand}"


class Fashion(BaseListing):
    sell_or_rent = models.CharField(choices=sell_or_rent, max_length=50, null=True, blank=True)
    fashionType = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField( max_length=20, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fashionType} - {self.brand} ({self.size})"


class Electronics(BaseListing):
    sell_or_rent = models.CharField(choices=sell_or_rent, max_length=50, null=True, blank=True)
    electronicsType = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, blank=True, null=True)
    warranty = models.CharField(choices=yes_no, max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.electronicsType} - {self.brand} ({self.model})"
class JobVacancy(BaseListing):
    positionType = models.CharField(choices=positontypes, max_length=50, blank=True, null=True)
    companyName = models.TextField(blank=True, null=True, max_length=500)
    positionTitle = models.TextField(blank=True, null=True, max_length=500)
    worklocation = models.TextField(blank=True, null=True, max_length=500)
    experianceLevel = models.CharField(choices=experiancelevel, max_length=50, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    applicationDeadline = models.DateField(blank=True, null=True)
    JobDescription = models.TextField(blank=True, null=True, max_length=2000)
    JobRequirment = models.TextField(blank=True, null=True, max_length=2000)
 

    def __str__(self):
        return f"{self.positionTitle} - {self.positionType}"


class ServiceOrBusinessType(BaseListing):
 
    busienssOrServiceType = models.ForeignKey(BusienssOrServiceType, related_name='ServiceOrBusinesstype', on_delete=models.CASCADE)
    businessLocation = models.TextField(blank=True, null=True, max_length=500)
    Title = models.TextField(blank=True, null=True, max_length=500)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True, max_length=2000)
  

    def __str__(self):
        return self.name


class LostOrFound(BaseListing):
    typeofadd = models.CharField(choices=lostfoudtypeofadd, max_length=255)
    Title = models.TextField(blank=True, null=True, max_length=500)
    description = models.TextField(blank=True, null=True, max_length=2000)
 

    def __str__(self):
        return self.name


class FreeStaffOrItem(BaseListing):
    title = models.TextField(blank=True, null=True, max_length=500)
    description = models.TextField(blank=True, null=True, max_length=2000)

    def __str__(self):
        return self.name


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    contentType = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    objectId = models.PositiveIntegerField()
    item = GenericForeignKey('contentType', 'objectId')
    removed = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.username} is watching {self.item}"
    

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    item = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} on {self.timestamp}"

    @property
    def is_from_seller(self):
        return self.sender == self.item.seller

    @property
    def is_from_buyer(self):
        return self.sender != self.item.seller
    
    