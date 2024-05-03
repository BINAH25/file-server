from django.contrib.auth import get_user_model
from rest_framework import serializers
from files.models import *
from rest_api.serialiers.user_serializers import *
User = get_user_model()


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['title','description', 'type','file']
        
class FileSerializer(serializers.ModelSerializer):
    uploaded_by = UserLoginSerializer()
    class Meta:
        model = File
        fields ="__all__"