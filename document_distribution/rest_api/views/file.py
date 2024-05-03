from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_api.serialiers.file_serializers import *
from utils.function import *
from django.contrib.auth import get_user_model
from users.models import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives
from rest_api.permissions import APILevelPermissionCheck
import re
User = get_user_model()


class UploadFileAPI(generics.GenericAPIView):
    """ check for require permission for uploading file"""
    permission_classes = [permissions.IsAuthenticated,APILevelPermissionCheck]
    required_permissions = [ "setup.add_file"]
    
    serializer_class = UploadSerializer
    def post(self, request,*args, **kwargs):
        """ for uploading file"""
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            new_file = serializers.save(uploaded_by=request.user) 
            return Response(
                    {
                        "status": "success",
                        "detail": "File Uploaded Successfully",
                    },
                    status=status.HTTP_201_CREATED,
                )
        else:
            return Response(
                {"status": "failure", "detail": serializers.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllFilesAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    serializer_class = FileSerializer
    def get(self, request,*args, **kwargs):
        files = File.objects.all().order_by('-created_at')
        serializers = self.serializer_class(files,many=True)
        return Response(
            {"status": "success", "detail": serializers.data},
            status=200
        )
        
class DeleteFileAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,APILevelPermissionCheck]
    required_permissions = [ "setup.delete_file"]
    def delete(self, request, pk, *args, **kwargs):
        try:
            file = File.objects.get(id=pk)
            file.delete()
            return Response(
                {
                    "status": "success",
                    "detail": "File Deleted Successfully",
                },
                status=status.HTTP_200_OK,
            )
        except File.DoesNotExist:
            return Response(
                {"status": "error", "detail":"File Not Found"},
                status=200
            )