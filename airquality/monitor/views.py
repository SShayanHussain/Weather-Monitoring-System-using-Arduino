from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import SensorData
import json
from datetime import timedelta


def dashboard(request):
    """
    Renders the dashboard with the most recent sensor reading.
    """
    current_data = SensorData.objects.latest('timestamp')
    return render(request, 'dashboard.html', {'current_data': current_data})


def get_all_data(request):
    """
    Returns the last 50 sensor readings as JSON for chart rendering.
    """
    try:
        all_data = SensorData.objects.all().order_by('-timestamp')[:50]
        data_points = []

        for entry in reversed(all_data):
            data_points.append({
                'timestamp': entry.timestamp.strftime('%H:%M:%S'),
                'temperature': entry.temperature,
                'humidity': entry.humidity,
                'air_quality': entry.air_quality,  # Include air quality
            })

        return JsonResponse(data_points, safe=False)

    except Exception as e:
        print(f"[ERROR] get_all_data: {e}")
        return JsonResponse({'status': 'error', 'message': 'Error fetching data'}, status=500)


@csrf_exempt
def receive_data(request):
    """
    Receives data from ESP32 via POST and stores it in the database.
    Expected JSON: {"temperature": float, "humidity": float, "air_quality": int}
    """
    if request.method == 'POST':
        try:
            if request.content_type != 'application/json':
                return JsonResponse({'status': 'error', 'message': 'Content-Type must be application/json'}, status=400)

            data = json.loads(request.body)
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            air_quality = data.get('air_quality')

            if temperature is not None and humidity is not None and air_quality is not None:
                SensorData.objects.create(
                    temperature=temperature,
                    humidity=humidity,
                    air_quality=air_quality
                )
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Missing temperature, humidity, or air_quality'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"[ERROR] receive_data: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)

from django.shortcuts import render

def about(request):
    return render(request, 'about.html')

def live(request):
    return render(request, 'live.html')




def get_latest_data(request):
    latest_entry = SensorData.objects.latest('timestamp')
    data = {
        'temperature': latest_entry.temperature,
        'humidity': latest_entry.humidity,
        'air_quality': latest_entry.air_quality,
    }
    return JsonResponse(data)

