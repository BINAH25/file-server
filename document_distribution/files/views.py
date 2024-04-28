from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from files.models import *
from files.forms import *
from utils.function import generate_activation_code
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from users.models import *
from django.contrib.auth import login, logout

# Create your views here.

class DashboardView(PermissionRequiredMixin,View):
    template_name = "admin/dashboard.html"
    permission_required = [
        "files.add_file",
        "files.view_file",
    ]
    def get(self, request, *args, **kwargs):
        files = File.objects.all().order_by('-created_at')
        files_count = File.objects.all().count()
        users_count = User.objects.all().count()
        context = {
            'files':files,
            'files_count':files_count,
            'users_count':users_count
        }
        return render(request, self.template_name,context)
    
        

class UploadFile(View):
    form_class = FileForm
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.uploaded_by = request.user
            new_file.save()
            messages.success(request, "File Uploaded Successfully")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            for field, error in form.errors.items():
                message = f"{field.title()}: {strip_tags(error)}"
                messages.error(request, message)
                return redirect(request.META.get("HTTP_REFERER"))


def file_delete(request, pk):
    file = File.objects.get(id=pk)
    if request.method == 'POST':
        file.delete()
        messages.success(request, "File Deleted Successfully")
        return redirect('files:dashboard')
    context = {
        'file':file
    }
    return render(request, "admin/delete.html",context)

class ChangePasswordView(View):
    template_name = "admin/account.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        current_password = request.POST['current']
        new_password = request.POST['new_password']
        try:
            if not user.check_password(current_password):
                messages.error(request, "Wrong Current Password")
                return redirect(request.META.get("HTTP_REFERER"))
            else:
                user.set_password(new_password)
                user.save()
                user = EmailBackend.authenticate(self=self,request=request,email_address=user.email_address,password=new_password)
                login(request,user)
                messages.success(request, "Password Changed Successfully")
                return redirect(request.META.get("HTTP_REFERER"))
        except KeyError:
            messages.error(request, "Password Change Failed")
            return redirect(request.META.get("HTTP_REFERER"))
        return render(request, self.template_name)