from django.db import models
import uuid

class Transaction(models.Model):
    uuid = models.UUIDField(default=uuid.uuid1, editable=False, unique=True)
    pass

class Board(models.Model):
    internal_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    description  = models.CharField(max_length=255)
    transaction = models.ForeignKey('Transaction')

class Application(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    transaction = models.ForeignKey('Transaction')

class Module(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    group_identifier = models.CharField(max_length=255)
    transaction = models.ForeignKey('Transaction')
