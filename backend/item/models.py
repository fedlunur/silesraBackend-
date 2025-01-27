from django.db import models

from products.models import *

fueltypes =  [
         ('electric', 'electric'),
          ('hybrid', 'hybrid'),
          ('petrol', 'petrol'),
          ('diseal', 'diseal'),
       
           ]
class Cars(ItemCommonProperty):
    carType = models.ForeignKey(CarType, related_name='houses', on_delete=models.CASCADE)
    model = models.CharField(max_length=255,blank=True,null=True)
    year=models.IntegerField(default=0)
    mileage=models.CharField(max_length=255,blank=True,null=True)
    fuelType=models.CharField(choices=fueltypes,max_length=255)
 
    def __str__(self):
        return f"{self.name} ({self.model})"

     
class House(ItemCommonProperty):
    houseType = models.ForeignKey(HouseType, related_name='houses', on_delete=models.CASCADE)
    numberofBedrooms = models.IntegerField(default=0)
    numberofBathrooms = models.IntegerField(default=0)
    size =models.CharField(max_length=255,blank=True,null=True)
 
    def __str__(self):
        return f"{self.name} ({self.houseType})"    
 
class otherItem(ItemCommonProperty):
    title =models.CharField(max_length=255,blank=True,null=True)
   
    def __str__(self):
        return f"{self.name} ({self.houseType})"   
    
     
class Service(ItemCommonProperty):
    title = models.CharField(max_length=255,)
   

    def __str__(self):
        return f"{self.name}"    
        
class ServiceOrBusinesstype(ServiceCommonProperty):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name  
      
  