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

# Create your views here.

class DashboardView(PermissionRequiredMixin,View):
    template_name = "admin/dashboard.html"
    permission_required = [
        "files.add_file",
        "files.view_file",
    ]
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
        

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

