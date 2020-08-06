from django.contrib import admin
from .models import messageModel

# Register your models here.
class messageModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_created')
    search_fields = ('name', 'email', 'subject', 'description')

admin.site.register(messageModel, messageModelAdmin)