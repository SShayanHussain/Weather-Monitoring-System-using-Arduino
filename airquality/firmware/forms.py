from django import forms
from .models import Firmware

class FirmwareUploadForm(forms.ModelForm):
    class Meta:
        model = Firmware
        fields = ['version', 'file']
