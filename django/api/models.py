from django.db import models
import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

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

class Application(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    group_identifier = models.CharField(max_length=255)
    transaction = models.ForeignKey('Transaction')

    class Meta:
        permissions = (('has_dev_perm','Has dev permissions'),)

class Module(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    group_identifier = models.CharField(max_length=255)
    transaction = models.ForeignKey('Transaction')
