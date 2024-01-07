from django.urls import path
from . import views

#urlConf
urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('hello/',views.say_hello),
    path('receipt/',views.generate_receipt),
    path('upload_file/',views.upload_file)
]