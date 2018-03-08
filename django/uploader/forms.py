from django import forms
from uploader.models import Application

class UploadFileForm(forms.ModelForm):
    class Meta:
        model=Application
        fields=('name', 'description', 'licences', 'project_page', 'app_tarball', 'app_repo_url') 
