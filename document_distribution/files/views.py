from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from files.models import *
from files.forms import *
from django.utils.html import strip_tags
from django.conf import settings
from django.shortcuts import get_object_or_404,HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from users.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db.models import Sum
from django.db.models import Q

# Create your views here.

class DashboardView(PermissionRequiredMixin,View):
    template_name = "admin/dashboard.html"
    # Permission needed for accessing the admin dashboard
    permission_required = [
        "files.add_file",
        "files.view_file",
    ]
    
    # Get all files, users, downloads 
    def get(self, request, *args, **kwargs):
        files = File.objects.all().order_by('-created_at')
        files_count = File.objects.all().count()
        users_count = User.objects.all().count()
        total_downloads = File.objects.aggregate(total_downloads=Sum('downloads'))['total_downloads']
        context = {
            'files':files,
            'files_count':files_count,
            'users_count':users_count,
            'total_downloads':total_downloads
        }
        return render(request, self.template_name,context)
    
        

class UploadFile(View):
    form_class = FileForm
    """For uploading file by the admin"""
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
    """For deleting file """
    file = File.objects.get(id=pk)
    if request.method == 'POST':
        file.delete()
        messages.success(request, "File Deleted Successfully")
        return redirect('files:dashboard')
    context = {
        'file':file
    }
    return render(request, "admin/delete.html",context)


def download_file(request, pk):
    """For downloading file and increase file download for each file by 1"""
    file_instance = get_object_or_404(File, id=pk)
    file_instance.downloads += 1
    file_instance.save()
    
    response = HttpResponse(file_instance.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
    return response
    return redirect(request.META.get("HTTP_REFERER"))


class AccounView(View):
    template_name = "admin/account.html"
    
    @method_decorator(login_required(login_url="/"))
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class ChangePasswordView(View):
    @method_decorator(login_required(login_url="/"))
    def post(self, request, *args, **kwargs):
        """For changing password"""
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
                user = authenticate(request, email_address=user.email_address, password=new_password)
                login(request,user)
                messages.success(request, "Password Changed Successfully")
                return redirect(request.META.get("HTTP_REFERER"))
        except KeyError:
            messages.error(request, "Password Change Failed")
            return redirect(request.META.get("HTTP_REFERER"))
    
    
class UserDashboard(View):
    template_name = "user/user_dashboard.html"
    @method_decorator(login_required(login_url="/"))
    def get(self, request, *args, **kwargs):
        files = File.objects.all().order_by('-created_at')
        context = {
            'files':files
        }
        return render(request, self.template_name,context)
    
    
class UserAccounView(View):
    template_name = "user/account.html"
    
    @method_decorator(login_required(login_url="/"))
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    
class SearchView(View):
    template_name = "user/search.html"
    @method_decorator(login_required(login_url="/"))
    def post(self, request, *args, **kwargs):
        kw = request.POST['keyword']
        files = File.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw) | Q(type__icontains=kw))
        context = {
            'files':files
        }
        return render(request, self.template_name, context)
    