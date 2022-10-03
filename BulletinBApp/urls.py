from django.urls import path
from .views import IndexView, AdCreate, AdView, AdDetail, Register, EmailVerify


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', AdCreate.as_view(), name='ad_list'),
    path('ads/', AdView.as_view(), name='ad_list'),
    path('ad/,<int:post_id>', AdDetail, name='ad'),
    path('register/', Register.as_view(), name='register'),
    path('register/confirm/', EmailVerify.as_view(), name='confirm'),
]
