from django.db import models


# Create your models here.
class SilesraBankAccount(models.Model):
    BANK_CHOICES = [
        ('CBE', 'Commercial Bank of Ethiopia'),
        ('Awash', 'Awash Bank'),
        ('Dashen', 'Dashen Bank'),
       
    ]

    name = models.CharField(max_length=255, choices=BANK_CHOICES)
    account_number = models.CharField(max_length=255, unique=True)
    bank_icon = models.ImageField(upload_to='bank_icons/', blank=True, null=True, help_text="Upload the bank's icon")
   
    
    def __str__(self):
        return f"{self.name} - {self.account_number}"
    
class GeneralSetting(models.Model):
    service_call_number = models.CharField(max_length=255, blank=True, null=True, help_text="Customer service phone number")
    Default_bank_account = models.ForeignKey(
        SilesraBankAccount,
        on_delete=models.SET_NULL,
        null=True,
        related_name='default_for_settings',
        help_text="Default bank account for payments"
    )
    
    def __str__(self):
        return {self.service_call_number}    