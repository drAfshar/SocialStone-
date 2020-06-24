from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    pass

