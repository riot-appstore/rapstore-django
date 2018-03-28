from django.db import models
import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
import requests

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Transaction(models.Model):
    uuid = models.UUIDField(default=uuid.uuid1, editable=False, unique=True)
    pass

class Board(models.Model):
    internal_name = models.CharField(max_length=255)
    flash_program = models.CharField(max_length=32)
    display_name = models.CharField(max_length=255)
    transaction = models.ForeignKey('Transaction')

class Module(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    group_identifier = models.CharField(max_length=255)
    transaction = models.ForeignKey('Transaction')

fs = FileSystemStorage(location='/apps')
#Represents external applications (to be uploaded)
class Application(models.Model):
    author = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True, blank=True)
    licences = models.CharField(max_length=255, null=True, blank=True) 
    project_page = models.URLField(max_length=255, null=True, blank=True)
    app_tarball = models.FileField(storage=fs)
    app_repo_url = models.URLField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction = models.ForeignKey('Transaction')

    class Meta:
        permissions = (('has_dev_perm','Has dev permissions'),)

    def download_tar(self, link):
        # get the remote repo from app_repo_url and create the command string
        print("*********************printing link now***************")
        print(link)
        r = requests.get(link, verify=False)
        with open("/apps/master2.tar.gz", "wb") as f:
            f.write(r.content)

        reopen = open("/apps/master2.tar.gz", "rb")
        self.app_tarball = File(reopen)

        # could also use Django file storage functions to directly save the file to fs
        # wget the remote repo, check the command was executed correctly and we have the tar, and attach it to app_folder
