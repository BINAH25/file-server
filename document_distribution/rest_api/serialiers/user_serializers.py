from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import *
User = get_user_model()


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email_address',
        ]
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email_address',
            'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        # CLEAN ALL VALUES
        email_address = validated_data['email_address'].lower()
        password = validated_data['password']
        # CREATE A NEW  USER
        user = User.objects.create(
            username=email_address,
            email_address=email_address,
        )
        user.set_password(password)
        user.save()
        return user

class CodeEmailSerializer(serializers.Serializer):
    email_address = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=254)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=254)
    new_password = serializers.CharField(max_length=254)
    
class ResetPasswordSerializer(serializers.Serializer):
    email_address = serializers.CharField(max_length=254)
    
class ResetPasswordDoneSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=254)
    new_password = serializers.CharField(max_length=254)
