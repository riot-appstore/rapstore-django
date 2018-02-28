from django import forms
from uploader.models import Application

class UploadFileForm(forms.ModelForm):
    class Meta:
        model=Application
        fields=('elf_file', 'repo_url', 'name', 'description')
