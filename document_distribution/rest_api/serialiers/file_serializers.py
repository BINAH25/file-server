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
        
class SearchSerializer(serializers.Serializer):
    keyword = serializers.CharField(max_length=254)
    
class SendFileSerializer(serializers.Serializer):
    email_address = serializers.EmailField(max_length=254)
    file_id = serializers.CharField(max_length=254)
