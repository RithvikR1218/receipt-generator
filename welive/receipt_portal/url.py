from django.urls import path
from . import views

#urlConf
urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('hello/',views.say_hello),
    path('api/receipt/generate/<str:file>',views.generate_receipt),
    path('upload_file/',views.upload_file),
    path('api/email/<str:dir>',views.send_email),
    path('api/receipt/delete/<str:file>',views.delete_receipt)
]