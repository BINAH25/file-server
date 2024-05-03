from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_api.serialiers.user_serializers import *
from utils.function import *
from django.contrib.auth import get_user_model
from users.models import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives
import re
User = get_user_model()
# Create your views here.


def get_auth_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'user':UserLoginSerializer(user).data,
        'permission':get_all_user_permissions(user),
        'refresh': str(refresh),
        'token': str(refresh.access_token) 
    }
    
    
class SignInAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CodeEmailSerializer
    def post(self, request,*args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            email_address = serializers.data["email_address"]
            password = serializers.data["password"]
            if User.objects.filter(email_address=email_address): 
                user = authenticate(email_address=email_address,password=password)
                if not user:
                    response_data = {'message':'Invalid Credential'}
                    return Response(response_data, status=400)
                
                user_data = get_auth_for_user(user)
                return Response(user_data, status=200)
            else:
                return Response(
                    {
                        "status": "error",
                        "detail": "User Not Found",
                    },
                    status=400,
                )
        else:
            return Response(
                {"status": "failure", "detail": serializers.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

class RegistrationAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CodeEmailSerializer
    def post(self, request,*args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            email_address = serializers.data["email_address"]
            password = serializers.data["password"]
            # Validate password
            if len(password) < 4:
                return Response(
                    {"status": "failure", "detail": "Password Must be at least 4 characters"},
                    status=400,
                )
        
            # Validate email address format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
                return Response(
                    {"status": "failure", "detail": "Invalid email address format"},
                    status=400,
                )
            
            if User.objects.filter(email_address=email_address):
                return Response(
                    {"status": "failure", "detail": "Email Already Exist"},
                    status=400,
                )

            if CodeEmail.objects.filter(email_address=email_address):
                code_user = CodeEmail.objects.get(email_address=email_address)
                generated_code = generate_activation_code()
                code_user.code = generated_code
                code_user.save()
                context = {
                "generated_code": generated_code,
                }
                html_message = render_to_string("user/verify.html",context)
                plain_message = strip_tags(html_message)
                try:
                    message = EmailMultiAlternatives(
                    subject="Email Verification Code",
                    body=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email_address],
                )
                    message.attach_alternative(html_message, 'text/html')
                    message.send()
                    return Response(
                        {
                            "status": "success",
                            "detail": "email verification code send",
                            "data": {
                                "email_address": email_address,
                            },
                        },
                        status=status.HTTP_200_OK,
                    )
                except Exception as e:
                    return Response(
                        {
                            "status": "error",
                            "detail": f"Error sending email: {e}, try again",
                        },
                        status=400,
                    )
            # Generate Verification Code
            generated_code = generate_activation_code()
            context = {
                "generated_code": generated_code,
            }
            html_message = render_to_string("user/verify.html",context)
            plain_message = strip_tags(html_message)
            
            code_user = CodeEmail.objects.create(email_address=email_address, password=password,code=generated_code)
            code_user.save()
            # Send Email with verification Code  to User Email 
            try:
                message = EmailMultiAlternatives(
                subject="Email Verification Code",
                body=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email_address],
                )
                message.attach_alternative(html_message, 'text/html')
                message.send()
                return Response(
                    {
                        "status": "success",
                        "detail": "email verification code send",
                        "data": {
                            "email_address": email_address,
                        },
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {
                        "status": "error",
                        "detail": f"Error sending email: {e}, try again",
                    },
                    status=400,
                )
        else:
            return Response(
                {"status": "failure", "detail": serializers.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class EmailVerificationAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        code = request.data.get("code")
        if not code:
            return Response(
                {
                    "status": "error",
                    "detail":"the code is required",
                },
                status=400,
            )
        # Check if code is not numeric
        if not code.isdigit():
            return Response(
                {
                    "status": "error",
                    "detail": "The code must be numeric",
                },
                status=400,
            )
        try:
            code_email = CodeEmail.objects.get(code=code)
            user = User.objects.create_user(username=code_email.email_address, email_address=code_email.email_address, password=code_email.password)
            user.save()
            code_email.delete()
            user_data = get_auth_for_user(user)
            return Response(user_data, status=200)           
        except CodeEmail.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "detail":"Invalid or Wrong Code Entered",
                },
                status=400,
            )
    
class LogOutAPI(generics.GenericAPIView):
    """Logout API view to blacklist refresh token"""

    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=200)
        except Exception as e:
            return Response({"detail": "Error logging out. {e}"}, status=400)

class ChangePasswordAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def post(self, request, *args, **kwargs):
        """For changing password"""
        user = request.user
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            current_password = serializers.data["current_password"]
            new_password = serializers.data["new_password"]
            
            if len(new_password) < 4:
                return Response(
                    {"status": "failure", "detail": "Password Must be at least 4 characters"},
                    status=400,
                )
            try:
                if not user.check_password(current_password):
                    return Response(
                        {
                            "status": "failure",
                            "detail": "wrong current password",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    user.set_password(new_password)
                    user.save()
                    return Response(
                        {
                            "status": "success",
                            "detail": "Password changed successfully",
                        },
                        status=status.HTTP_200_OK,
                    )
                
            except KeyError:
                return Response(
                {"status": "failure", "detail": "change password failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"status": "failure", "detail": serializers.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

class ResetPasswordAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer
    def post(self, request, *args, **kwargs):
        """For sending  Password Reset Verification Code"""
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            email_address = serializers.data['email_address']
            if User.objects.filter(email_address=email_address) and CodeEmail.objects.filter(email_address=email_address):
                code_user = CodeEmail.objects.get(email_address=email_address)
                verification_code = generate_activation_code()
                code_user.code = verification_code
                code_user.save()
                context = {
                "verification_code": verification_code,
                }
                html_message = render_to_string("user/reset_code.html",context)
                plain_message = strip_tags(html_message)
                try:
                    message = EmailMultiAlternatives(
                    subject="Password Reset Verification Code",
                    body=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email_address],
                )
                    message.attach_alternative(html_message, 'text/html')
                    message.send()
                    return Response(
                        {
                            "status": "success",
                            "detail": "Password Reset Verification Code Sent to Email",
                            "data": {
                                "email_address": email_address,
                            },
                        },
                        status=status.HTTP_200_OK,
                    )
                except Exception as e:
                    return Response(
                        {
                            "status": "error",
                            "detail": f"Error sending email: {e}, try again",
                        },
                        status=400,
                    )
            #For sending password reset verification code to user        
            elif User.objects.filter(email_address=email_address):
                verification_code = generate_activation_code()
                code_user = CodeEmail.objects.create(email_address=email_address,code=verification_code)
                code_user.save()
                context = {
                "verification_code": verification_code,
                }
                html_message = render_to_string("user/reset_code.html",context)
                plain_message = strip_tags(html_message)
                try:
                    message = EmailMultiAlternatives(
                    subject="Password Reset Verification Code",
                    body=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email_address],
                )
                    message.attach_alternative(html_message, 'text/html')
                    message.send()
                    return Response(
                        {
                            "status": "success",
                            "detail": "Password Reset Verification Code Sent to Email",
                            "data": {
                                "email_address": email_address,
                            },
                        },
                        status=status.HTTP_201_CREATED,
                    )
                except Exception as e:
                    return Response(
                        {
                            "status": "error",
                            "detail": f"Error sending email: {e}, try again",
                        },
                        status=400,
                    )  
            else:
                return Response(
                    {
                        "status": "error",
                        "detail": "User Not Found",
                    },
                    status=400,
                )  
        else:
            return Response(
                {"status": "failure", "detail": serializers.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
            
class ResetPasswordDoneAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordDoneSerializer
    def post(self, request, *args, **kwargs):
        """For changing reseting password"""
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            code = serializers.data['code']
            new_password = serializers.data['new_password']
            if not code.isdigit():
                return Response(
                    {
                        "status": "error",
                        "detail": "The code must be numeric",
                    },
                    status=400,
                )
            if len(new_password) < 4:
                return Response(
                    {"status": "failure", "detail": "Password Must be at least 4 characters"},
                    status=400,
                )
            try: 
                code_email = CodeEmail.objects.get(code=code)
                user = User.objects.get(email_address=code_email.email_address)
                user.set_password(new_password)
                user.save()
                code_email.delete()
                return Response(
                    {
                        "status": "success",
                        "detail": "Password Reset Successfully",
                    },
                    status=status.HTTP_201_CREATED,
                )
            except CodeEmail.DoesNotExist:
                return Response(
                    {
                        "status": "error",
                        "detail": "Invalid or Wrong Password Verification Code Entered",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"status": "failure", "detail": serializers.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
            
class DeleteAccountAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        user = request.user
        try:
            user.delete()
            return Response(
                {
                    "status": "success",
                    "detail": "User Account Deleted  Successfully",
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "detail": "User Not Found",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
