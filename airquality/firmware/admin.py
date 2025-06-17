from django.contrib import admin
from .models import Firmware

@admin.register(Firmware)
class FirmwareAdmin(admin.ModelAdmin):
    list_display = ('version', 'is_latest', 'uploaded_at')
    list_filter = ('is_latest', 'uploaded_at')
