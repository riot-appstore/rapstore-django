from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

# Create your models here.

fs = FileSystemStorage(location='/apps')
#Represents external applications (to be uploaded)
class Application(models.Model):
    author = models.ForeignKey(User)
    elf_file = models.FileField(storage=fs)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
