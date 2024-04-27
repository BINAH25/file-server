from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from users.models import *
from utils.function import generate_activation_code
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
import re
from django.shortcuts import get_object_or_404

# Create your views here.

class Register(View):
    template_name = "user/register.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    ''' Registering a users and make them temporal'''
    def post(self, request, *args, **kwargs):
        
        email_address = request.POST.get("email_address")
        password = request.POST.get("password")
        
        # Validate email address format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
            messages.error(request, "Invalid email address")
            return redirect(request.META.get("HTTP_REFERER"))

        
        if User.objects.filter(email_address=email_address):
            messages.error(request, "Email Already Exist")
            return redirect(request.META.get("HTTP_REFERER"))
        
        if CodeEmail.objects.filter(email_address=email_address):
            messages.error(request, "Email Already Exist Verify Your Account to Login")
            return redirect("users:verify")
        
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
            messages.success(request, "Email Verification Code Sent to Email")
            return redirect(request.META.get("HTTP_REFERER"))
        except Exception as e:
            print(f"Error sending email: {e}")
    
        return render(request, self.template_name)
    

class CodeVerificationView(View):
    template_name = "user/code_verification.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    ''' Verifying users account to make it permanent'''
    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")
        try:
            
            code_email = CodeEmail.objects.get(code=code)
            user = User.objects.create_user(email_address=code_email.email_address)
            user.set_password(code_email.password)
            user.save()
            code_email.delete()
            messages.success(request, "Email Verified")
            return redirect(request.META.get("HTTP_REFERER"))
            
        except CodeEmail.DoesNotExist:
            messages.error(request, "Invalid or Wrong Code Entered")
            return redirect(request.META.get("HTTP_REFERER"))

        return render(request, self.template_name)
    
    

    
class LoginView(View):
    template_name = "user/login.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request,*args, **kwargs):
        email_address = request.POST['email_address']
        password = request.POST['password']
        if User.objects.filter(email_address=email_address): 
            user = EmailBackEnd.authenticate(request,email_address=email_address,password=password)
            if user !=None:
                login(request,user)
                messages.success(request, "Email Verified")
                return redirect(request.META.get("HTTP_REFERER"))
            else:
                messages.error(request,"Invalid Login Details")
                return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request,"User Not Found")
            return redirect(request.META.get("HTTP_REFERER"))
        
        return render(request, self.template_name)

    

    
    
    