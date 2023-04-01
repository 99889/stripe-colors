from django.db import models



class UrineStrip(models.Model):
    image = models.ImageField(upload_to='images/')
    result = models.JSONField(null=True, blank=True)
