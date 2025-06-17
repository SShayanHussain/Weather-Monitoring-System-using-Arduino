# firmware/models.py
import os
import shutil
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Firmware(models.Model):
    version = models.PositiveIntegerField()
    file = models.FileField(upload_to='firmware_temp/')  # Temporary folder
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_latest = models.BooleanField(default=False)

    def __str__(self):
        return self.version

@receiver(post_save, sender=Firmware)
def move_firmware_to_static(sender, instance, **kwargs):
    src = instance.file.path
    dst_dir = os.path.join(settings.BASE_DIR, 'static', 'firmware')
    dst_file = os.path.join(dst_dir, 'aqm.ino.bin')

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Remove old file
    if os.path.exists(dst_file):
        os.remove(dst_file)

    # Move the uploaded file and rename it
    shutil.copyfile(src, dst_file)
