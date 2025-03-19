from django.contrib import admin
from .models import ExcelFile

# Register your models here.

@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'uploaded_at', 'processed')
    list_filter = ('processed', 'uploaded_at')
    search_fields = ('filename',)
    ordering = ('-uploaded_at',)
