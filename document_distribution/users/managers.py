from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_superuser(self, email_address, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email_address, password, **extra_fields)

    def create_user(self, email_address, password=None, **extra_fields):
        if not email_address:
            raise ValueError('The Email Address field must be set')
        email_address = self.normalize_email(email_address)
        return self._create_user(email_address, password, **extra_fields)

    def _create_user(self, email_address, password, **extra_fields):
        user = self.model(email_address=email_address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
