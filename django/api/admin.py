from django.contrib import admin
from api.models import Board
from api.models import Application
from api.models import Module
from api.models import Transaction
from api.models import UserProfile

def names(t):
    class AdminClass(admin.ModelAdmin):
        list_display=t
    return AdminClass

# Register your models here.
admin.site.register(Board, names(("internal_name",)))
admin.site.register(Application, names(("name", "description", "is_public")))
admin.site.register(Module, names(("name", "description")))
admin.site.register(Transaction, names(("uuid",)))
admin.site.register(UserProfile)
