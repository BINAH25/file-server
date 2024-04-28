from django import forms
from files.models import *


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title','description','file']