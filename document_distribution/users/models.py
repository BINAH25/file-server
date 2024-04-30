from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager

# Create your models here.

"""Models for user creation"""
class User(AbstractUser):
    email_address = models.EmailField(
        verbose_name='email', max_length=200, unique=True)
    

    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email_address
    
"""Code email model for temporary storing users until they verified their account"""
class CodeEmail(models.Model):
    code = models.IntegerField(blank=True,null=True)
    email_address = models.EmailField(max_length=254, unique=True,blank=False)
    first_name = models.CharField(max_length=200, blank=True, unique=False,null=True)
    other_names = models.CharField(max_length=200, blank=True, unique=False,null=True)
    password = models.CharField(max_length=200, blank=True, unique=False,null=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ("email_address",)
        
    def __str__(self):
        return self.email_address

