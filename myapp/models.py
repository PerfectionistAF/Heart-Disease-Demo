from django.db import models

# Create your models here.

class UserSubmission(models.Model):
    reference_number = models.CharField(max_length=100, unique=True) # this is different to django's auto-generated id
    diagnosis = models.CharField(max_length=255)  # CharField for shorter entries
    prognosis = models.TextField() # TextField for longer entries