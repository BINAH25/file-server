from django.db import models
from users.models import User

# Create your models here.
class File(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='files/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    downloads = models.IntegerField(default=0)
    emails_sent = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.title