from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
#Add no of objects limit in django
#Add a primary key or some shit dumbass
class Email(models.Model):
    subject = models.CharField(max_length=255)
    sender = models.EmailField(max_length=75)
    app_password = models.CharField(max_length=16, validators=[MinLengthValidator(16)])
    body = models.TextField()