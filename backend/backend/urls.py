
from django.urls import path, re_path
from django.contrib import admin
from django.urls import path,include

from item.views import *
from user_managment.views import *
from .views import GenericListAPIView,PasswordChangeView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
router = DefaultRouter()


 
""" structure Routes """
router.register(r'house', GenericModelViewSet, basename='house')
router.register(r'car', GenericModelViewSet, basename='car')
router.register(r'user', GenericModelViewSet, basename='user')
router.register(r'role', GenericModelViewSet, basename='role')
router.register(r'userRole', GenericModelViewSet, basename='userrole')

urlpatterns = [
    path('api/admin/', admin.site.urls),
    
    re_path(r'^api/token/?$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^api/token/refresh/?$', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^api/logout/?$', LogoutView.as_view(), name='logout'),
    re_path(r'^api/register/?$', UserRegister.as_view(), name='register'),
    re_path(r'^api/login/?$', UserLogin.as_view(), name='login'),
    re_path(r'^api/user_logout/?$', UserLogout.as_view(), name='user_logout'),

    # Generics

    re_path(r'^api/(?P<model_name>\w+)/list/?$', GenericListAPIView.as_view(), name='generic-list'),
    re_path(r'^api/(?P<model_name>\w+)/search/?$', GenericListAPIView.as_view(), name='generic-list'),
    #  re_path(r'^api/(?P<model_name>\w+)/advanced-list/?$', advanced_list, name='advanced-paginated-list'),
    re_path(r'^api/download/(?P<file_name>[^/]+)/$', download_file, name='download_file'),
  
    # Counts api 
    # re_path(r'^api/(?P<model_name>\w+)/by/(?P<foreign_key_field>\w+)/(?P<foreign_key_value>\d+)/$', get_by_foreign_key, name='get_by_foreign_key'),

    path('api/', include(router.urls)),
    re_path(r'^api/change-password/', PasswordChangeView.as_view(), name='change-password'),
   
]

