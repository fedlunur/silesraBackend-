
from django.urls import path, re_path
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from products.views import *
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
router.register(r'otheritem', GenericModelViewSet, basename='otheritem')
router.register(r'listingimage', GenericModelViewSet, basename='listingimage')
router.register(r'serviceorbussinesstype', GenericModelViewSet, basename='serviceorbussinesstype')
router.register(r'jobvacancy', GenericModelViewSet, basename='jobvacancy')
router.register(r'lostorfoud', GenericModelViewSet, basename='lostorfoud')
router.register(r'freestafforitem', GenericModelViewSet, basename='freestafforitem')
router.register(r'messages', GenericModelViewSet, basename='messages')
router.register(r'watchlist', GenericModelViewSet, basename='watchlist')

# setting
router.register(r'category', GenericModelViewSet, basename='category')
router.register(r'serviceorbussinesstypes', GenericModelViewSet, basename='serviceorbussinesstypes')
router.register(r'carmake', GenericModelViewSet, basename='carmake')
router.register(r'cartype', GenericModelViewSet, basename='cartype')
router.register(r'customerbank', GenericModelViewSet, basename='customerbank')
router.register(r'generalsetting', GenericModelViewSet, basename='generalsetting')
router.register(r'otheritemcatagory', GenericModelViewSet, basename='otheritemcatagory')
router.register(r'silesrabankaccount', GenericModelViewSet, basename='silesrabankaccount')

router.register(r'accessory', GenericModelViewSet, basename='accessory')
router.register(r'fashion', GenericModelViewSet, basename='fashion')
router.register(r'electronics', GenericModelViewSet, basename='electronics')

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
  
    re_path(r'^api/download/(?P<image_type>[A-Za-z0-9_]+)/(?P<file_path>.+)$', download_file, name='download_file'),
    # Counts api 
    # re_path(r'^api/(?P<model_name>\w+)/by/(?P<foreign_key_field>\w+)/(?P<foreign_key_value>\d+)/$', get_by_foreign_key, name='get_by_foreign_key'),
    re_path(r'^api/modelinfo/(?P<model_name>\w+)/$', ModelContentTypeView.as_view(), name='model-content-type-list'),
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api/change-password/', PasswordChangeView.as_view(), name='change-password'),
    re_path(r'^api/uploadrecipts/', UploadReceiptView.as_view(), name='uploadrecipts'),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

