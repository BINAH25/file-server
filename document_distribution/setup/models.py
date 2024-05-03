from django.db import models

# Create your models here.

class SetupPerm(models.Model):

    class Meta:
        managed = False
        default_permissions = ()
        permissions = [
            # File
            ("view_file", "Can view file"),
            ("add_file", "Can add file"),
            ("edit_file", "Can edit file"),
            ("delete_file", "Can delete file"),

        ]
