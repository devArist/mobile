from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phonenumber']


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'user']