from django.db import models
from django.conf import settings

class File(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    downloads = models.IntegerField(default=0)
    emails_sent = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']  