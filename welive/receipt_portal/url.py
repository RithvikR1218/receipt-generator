from django.urls import path
from . import views

#urlConf
urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('hello/',views.say_hello),
    path('api/receipt/generate',views.generate_receipt),
    path('upload_file/',views.upload_file),
    path('api/email/',views.send_email),
    path('api/receipt/delete',views.delete_receipt)
]