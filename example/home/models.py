from django.db import models

class QRData(models.Model):
    data_info = models.CharField(max_length=100)
