from django.urls import path,re_path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    re_path(r'.*admin.*$', bait_login_view, name='bait_login_view'),
]
