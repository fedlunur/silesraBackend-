import importlib
from django.apps import apps
from django.db.models.base import ModelBase
from user_managment.models import *
from products.models import *
from setting.models import *

def import_all_models():
   
    models = {}
    for app_config in apps.get_app_configs():
        try:
            app_module = importlib.import_module(app_config.name + '.models')
           
        except ModuleNotFoundError:
            continue

     
        for attr_name in dir(app_module):
            attr = getattr(app_module, attr_name)
            if isinstance(attr, ModelBase):
                models[attr_name] = attr
    print(app_module)
    return models

# left URl pattern and right Excat model name should map with URL's 
model_mapping = {
           # Products /all catagories 
        'car':Car,
        'house':House,
        'otheritem':OtherItem,
        'serviceorbussinesstype':ServiceOrBusinessType,
        'jobvacancy':JobVacancy,
        'lostorfoud':LostOrFound,
        'freestafforitem':FreeStaffOrItem,
        'messages':Message,
        'watchlist':Watchlist,
        
          # User managment
        'user':User,
        'role': Role,
   
        # setting
        'category': Category,
        'serviceorbussinesstypes':BusienssOrServiceType,
        'carmake':carMake,
        'cartype':CarType,
        'customerbank':CustomerBank,
        'generalsetting':GeneralSetting,
        'otheritemcatagory':OtherItemCategory,
        'silesrabankaccount':SilesraBankAccount
    }

# for any model exclude fileds 
donot_include_fields = {

   'user': ['removed','created','updated','enabled','password','user_permissions','groups','is_superuser','last_login','is_staff','date_joined'],
   'role': ['removed','created','updated','enabled'],
   
}

#return Json instead of Id for foreign keys 
genericlist_filds_nested_model = {
   
    'user':['id','phone','first_name',],
    'role':['id','name'],
   
    
}



def get_unique_users(users_queryset):
    unique_users = {user.id: user for user in users_queryset}
    return list(unique_users.values())# constants.py

