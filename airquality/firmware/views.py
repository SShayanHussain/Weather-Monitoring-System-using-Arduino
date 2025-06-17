import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import JsonResponse
from .forms import FirmwareUploadForm
from .models import Firmware
from django.core.files.storage import default_storage


def upload_firmware(request):
    if request.method == 'POST':
        form = FirmwareUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            filename = 'aqm.ino.bin'  # Fixed name so ESP32 always gets the latest

            # Path to static/firmware/
            static_firmware_path = os.path.join(settings.BASE_DIR, 'firmware', 'static', 'firmware')
            os.makedirs(static_firmware_path, exist_ok=True)
            file_path = os.path.join(static_firmware_path, filename)

            # Remove old file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)

            # Save new file
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Update DB
            Firmware.objects.all().update(is_latest=False)
            firmware = form.save(commit=False)
            firmware.file.name = f'firmware/{filename}'  # Fake the path to keep DB consistent
            firmware.is_latest = True
            firmware.save()

            return JsonResponse({'success': 'Firmware uploaded successfully'})
    else:
        form = FirmwareUploadForm()

    return render(request, 'upload.html', {'form': form})


def check_firmware(request):
    latest = Firmware.objects.filter(is_latest=True).first()
    if latest:
        return JsonResponse({
            "version": latest.version,
            "url": request.build_absolute_uri('/static/firmware/aqm.ino.bin')
        })
    return JsonResponse({"error": "No firmware found"}, status=404)

def upload(request):
    return render(request, 'upload.html')

