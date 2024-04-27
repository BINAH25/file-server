from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager):
    """Registration of the user using the BaseUserManager to create a superuser"""

    def create_user(self, email_address, first_name=None,other_names=None, password=None):
        """Creation of user"""
        if not email_address:
            raise ValueError("user must have email address")

        user = self.model(
            email_address=email_address,
            first_name=first_name,other_names=other_names
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, password, first_name=None,other_names=None):
        """Creation of a superuser"""
        user = self.create_user( email_address=email_address,first_name=first_name,other_names=other_names, password=password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user