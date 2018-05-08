# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 FU Berlin and HAW Hamburg
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from django.db import models
import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

import hashlib
import requests


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User)
    location = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)


@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created=False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if(hasattr(instance, 'userprofile')):
            instance.userprofile.save()


class Transaction(models.Model):
    uuid = models.UUIDField(default=uuid.uuid1, editable=False, unique=True)
    pass


class Board(models.Model):
    internal_name = models.CharField(max_length=255)
    flash_program = models.CharField(max_length=32)
    display_name = models.CharField(max_length=255)
    storage_flash_support = models.BooleanField(default=False)
    transaction = models.ForeignKey('Transaction')

    def __str__(self):
        return self.internal_name


class Module(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    group_identifier = models.CharField(max_length=255)
    transaction = models.ForeignKey('Transaction')

    def __str__(self):
        return self.name


isalphavalidator = RegexValidator(r'^[-\w_]+$', message='Name must be alphanumeric, hyphen or underscore only. No spaces allowed', code='Invalid name')

fs = FileSystemStorage(location='/apps')
# Represents external applications (to be uploaded)
class Application(models.Model):
    SOURCE_CHOICES = (
        ('R', 'RIOT_REPO'),
        ('E', 'EXTERNAL'),
    )
    author = models.ForeignKey(User)
    name = models.CharField(max_length=255, unique=True, validators=[isalphavalidator])
    description = models.TextField(max_length=65535, null=True, blank=True)
    licenses = models.CharField(max_length=255, null=True, blank=True) 
    project_page = models.URLField(max_length=255, null=True, blank=True)
    app_repo_url = models.URLField(max_length=255, null=True, blank=True)
    download_count = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=1, choices=SOURCE_CHOICES, default='E')

    def __str__(self):
        return self.name

    class Meta:
        permissions = (('has_dev_perm', 'Has dev permissions'),)

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


class ApplicationInstance(models.Model):
    application = models.ForeignKey(Application)
    version_code = models.PositiveIntegerField(default=0)
    version_name = models.CharField(max_length=255)
    app_tarball = models.FileField(storage=fs)
    app_tarball_md5 = models.CharField(max_length=16, editable=False, null=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        permissions = (('has_dev_perm','Has dev permissions'),)
        unique_together = ('version_code', 'application',)
        

class Feedback(models.Model):
    date = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    pass
