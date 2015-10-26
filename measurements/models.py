from django.db import models

# Create your models here.
class Measurement(models.Model):
    datetime = models.DateTimeField()
    loop_id = models.IntegerField(blank=True, null=True, default=None)
    type = models.CharField(max_length=3)
    units = models.CharField(max_length=3, blank=True, null=True, default=None)
    sensor_id = models.CharField(max_length=4)
    val = models.IntegerField()
    val_converted = models.FloatField(blank=True, default=None, null=True)
    
    class Meta:
        unique_together = (("datetime", "type", "sensor_id"),)
