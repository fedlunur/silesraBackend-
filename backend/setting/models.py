from django.db import models
from products.choices import BANK_CHOICES

# Create your models here.
class SilesraBankAccount(models.Model):


    name = models.CharField(max_length=255, choices=BANK_CHOICES)
    account_number = models.CharField(max_length=255, unique=True)
    bank_icon = models.ImageField(upload_to='bank_icons/', blank=True, null=True, help_text="Upload the bank's icon")
   
    
    def __str__(self):
        return f"{self.name} - {self.account_number}"    
class CustomerBank(models.Model):
    name = models.CharField(max_length=255 ,unique=True)     
    bank_icon = models.ImageField(upload_to='bank_icons/', blank=True, null=True, help_text="Upload the bank's icon")    
class GeneralSetting(models.Model):
    service_call_number = models.CharField(max_length=255, blank=True, null=True, help_text="Customer service phone number")
    Default_bank_account = models.ForeignKey(
        SilesraBankAccount,
        on_delete=models.SET_NULL,
        null=True,
        related_name='GeneralSetting',
        help_text="Default bank account for payments"
    )
    
    def __str__(self):
        return {self.service_call_number}    
    
    

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
   
    def __str__(self):
        return self.name
class  carMake(models.Model):
    name = models.CharField(max_length=255 ,unique=True)         
class CarType(models.Model):
    name = models.CharField(max_length=255 ,unique=True)      
class OtherItemCategory(models.Model):
    name = models.CharField(max_length=255 ,unique=True)     
class BusienssOrServiceType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
   
    