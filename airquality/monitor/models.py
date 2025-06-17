from django.db import models

class SensorData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    air_quality = models.FloatField(default=0.0)  # <-- Add a default value here
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temp: {self.temperature}, Hum: {self.humidity}, AQ: {self.air_quality}, Time: {self.timestamp}"

