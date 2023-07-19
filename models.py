from django.db import models

class Certificate(models.Model):
    name = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
