from django import forms
from uploader.models import Application

class UploadFileForm(forms.ModelForm):
    fields=('test_nonpopulated_field')
    class Meta:
        model=Application
        fields=('name', 'description', 'licences', 'project_page', 'app_folder', 'app_repo_url') 
