'''
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
    from django.contrib.auth import authenticate, login, logout, get_user_model
    User = get_user_model()

    # Create your views here.
'''
''''
class Register(View):
    template_name = "user/register.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
     #Registering a users and make them temporal
    def post(self, request, *args, **kwargs):
        
        email_address = request.POST.get("email_address")
        password = request.POST.get("password")
        
        if len(password) < 4:
            messages.error(request, "Password Must be at least 4 characters")
            return redirect(request.META.get("HTTP_REFERER"))
        
        # Validate email address format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
            messages.error(request, "Invalid email address format")
            return redirect(request.META.get("HTTP_REFERER"))

        
        if User.objects.filter(email_address=email_address):
            messages.error(request, "Email Already Exist")
            return redirect(request.META.get("HTTP_REFERER"))
        
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
                messages.success(request, "Email Verification Code Sent to Email")
                return redirect("users:verify")
            except Exception as e:
                messages.error(request,f"Error sending email: {e}, try again")
                return redirect(request.META.get("HTTP_REFERER"))
        
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
            return redirect("users:verify")
        except Exception as e:
            messages.error(request,f"Error sending email: {e}, try again")
            return redirect(request.META.get("HTTP_REFERER"))
    
        return render(request, self.template_name)
    

class CodeVerificationView(View):
    template_name = "user/code_verification.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    #Verifying users account to make it permanent
    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")
        # Check if code is not numeric
        if not code.isdigit():
            messages.error(request, "The code must be numeric")
            return redirect(request.META.get("HTTP_REFERER"))
        try:
            code_email = CodeEmail.objects.get(code=code)
            user = User.objects.create_user(username=code_email.email_address, email_address=code_email.email_address, password=code_email.password)
            user.save()
            user = authenticate(request, email_address=code_email.email_address, password=code_email.password)
            if user is not None:
                login(request,user)
                code_email.delete()
                messages.success(request, "Email Verified")
                return redirect('files:user-dashboard')
            else:
                return redirect('/')
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
            user = authenticate(request, email_address=email_address, password=password)
            
            if user is not None and user.is_staff and user.is_superuser:
                login(request, user)
                return redirect('files:dashboard')
            if user is not None:
                login(request,user)
                return redirect('files:user-dashboard')
            else:
                messages.error(request,"Invalid Login Details")
                return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request,"User Not Found")
            return redirect(request.META.get("HTTP_REFERER"))
        
        return render(request, self.template_name)
    
    
class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')
    
    
    
class ResetPasswordView(View):
    template_name = "user/reset_password.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    
    def post(self, request, *args, **kwargs):
        email_address = request.POST['email_address']
        #For sending Password Reset Verification Code again after the first attempt
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
                messages.success(request, "Password Reset Verification Code Sent to Email")
                return redirect('users:password_reset_done')
            except Exception as e:
                messages.error(request,f"Error sending email: {e}, try again")
                return redirect(request.META.get("HTTP_REFERER"))
            
            #For sending password reset verification code to user for first time       
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
                messages.success(request, "Password Reset Verification Code Sent to Email")
                return redirect('users:password_reset_done')
            except Exception as e:
                messages.error(request,f"Error sending email: {e}, try again")
                return redirect(request.META.get("HTTP_REFERER"))     
        else:
            messages.error(request, "User Not Found")
            return redirect(request.META.get("HTTP_REFERER"))
        return render(request, self.template_name)

    
class PasswordResetDone(View):
    template_name = "user/password_reset_done.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
        # Verifying the code  reseting the password
    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")
        password = request.POST.get("password")
        if len(password) < 4:
            messages.error(request, "Password Must be at least 4 characters")
            return redirect(request.META.get("HTTP_REFERER"))
        
        try: 
            code_email = CodeEmail.objects.get(code=code)
            user = User.objects.get(email_address=code_email.email_address)
            user.set_password(password)
            user.save()
            code_email.delete()
            messages.success(request, "Password Reset Successfully")
            return redirect('/')
            
        except CodeEmail.DoesNotExist:
            messages.error(request, "Invalid or Wrong Password Verification Code Entered")
            return redirect(request.META.get("HTTP_REFERER"))

        return render(request, self.template_name)
    
    
class DeleteAccount(View):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id")
        try:
            user =  User.objects.get(id=user_id)
            user.delete()
            messages.success(request, "User Account Deleted  Successfully")
            return redirect('/')
        except User.DoesNotExist:
            messages.error(request, "User Not Found")
            return redirect(request.META.get("HTTP_REFERER"))
''' 