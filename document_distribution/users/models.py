"""Models for user creation"""
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from users.managers import UserManager

# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    """User creation model"""
    email_address = models.EmailField(
        verbose_name='email', max_length=200, unique=True)
    first_name = models.CharField(max_length=200, blank=True, unique=False,null=True)
    other_names = models.CharField(max_length=200, blank=True, unique=False,null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = []

    class Meta:
        """Pre displayed field"""
        ordering = ("email_address",)

    def __str__(self):
        return f"{self.email_address}"

    def has_perm(self, perm, obj=None):
        """When user registraion has permission, then it is a superuser"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Has permission to access the model, like create a super user"""
        return self.is_superuser

class CodeEmail(models.Model):
    """Code email model for temporary storing users until they redeem their account"""
    code = models.IntegerField(blank=True,null=True)
    email_address = models.EmailField(max_length=254, unique=False,blank=False)
    first_name = models.CharField(max_length=200, blank=True, unique=False,null=True)
    other_names = models.CharField(max_length=200, blank=True, unique=False,null=True)
    password = models.CharField(max_length=200, blank=True, unique=False,null=True)
    updated_at= models.DateTimeField(auto_now=True)
    class Meta:
        """Pre displayed field"""
        ordering = ("email_address",)
        
    def __str__(self):
        return self.email_address


from django.contrib.auth.backends import ModelBackend
class EmailBackend(ModelBackend):
    """custom authentication backend"""
    def authenticate(self, request,
                    email_address=None, password=None, **kwargs):
        """custom authentication from django contrib"""
        try:
            user = User.objects.get(
                email_address=email_address)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
