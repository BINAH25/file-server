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
from django.shortcuts import HttpResponse
from django.db.models import Sum
from django.db.models import Q
from django.core.mail import EmailMessage
import re
from django.conf import settings
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
                status=400
            )
            
class DownloadFileAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        """For downloading file and increase file download for each file by 1"""
        try:
            file_instance = File.objects.get(id=pk)
            file_instance.downloads += 1
            file_instance.save()
            
            response = HttpResponse(file_instance.file, content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
            return response
            return Response(
                {
                    "status": "success",
                    "detail": "File Downloaded Successfully",
                },
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                {"status": "error", "detail":"File Not Found"},
                status=400
            )
            
class SearchFileAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SearchSerializer
    def post(self, request,*args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            keyword = serializers.data['keyword']
            files = File.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(type__icontains=keyword))
            file_serializers = FileSerializer(files,many=True)
            return Response(
                {"status": "success", "detail": file_serializers.data},
                status=200
            )
        else:
            return Response(
                {"status": "failure", "detail": serializers.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
            
class GetFileToSendFileViaEmailAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileSerializer
    def get(self, request, pk, *args, **kwargs):
        try:
            file = File.objects.get(id=pk)
            serializer = self.serializer_class(file,many=False)
            return Response(
                {"status": "success", "detail": serializer.data},
                status=200
            )
        except File.DoesNotExist:
            return Response(
                {"status": "failure", "detail": "File Not Found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class SendFileViaEmailAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SendFileSerializer
    def post(self,request, *args, **kwargs):
            """For getting absolute path of the and sending it to the email provided"""
            serializers = self.serializer_class(data=request.data)
            if serializers.is_valid():
                email_address = serializers.data['email_address']
                file_id = serializers.data['file_id']
                try:
                    file = File.objects.get(id=file_id)
                except File.DoesNotExist:
                    return Response(
                        {"status": "failure", "detail": "File Not Found"},
                        status=status.HTTP_400_BAD_REQUEST,
                    ) 
                file_url = file.file.url
                absolute_path = str(settings.BASE_DIR)+file_url
                # Validate email address format
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
                    return Response(
                        {"status": "failure", "detail": "Invalid email address format"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                try:
                    email = EmailMessage(
                        file.title,
                        file.description,
                        settings.EMAIL_HOST_USER,
                        [email_address]
                    )
                    email.attach_file(
                        absolute_path
                    )
                    email.send()
                    file.emails_sent += 1
                    file.save()
                    return Response(
                        {"status": "success", "detail":  f"File sent to {email_address} Successfully"},
                        status=200,
                    )
                except Exception as e:
                    return Response(
                        {"status": "error", "detail":f"Error sending email: {e}, try again"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
