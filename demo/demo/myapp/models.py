from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    username = models.CharField(max_length=256, unique=False, blank=True, null=True, default="anon")
    email = models.EmailField(max_length=256, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    def __str__(self):
        return self.email


class DoctorPatientFile(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='doctor_files', on_delete=models.CASCADE)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='patient_files', on_delete=models.CASCADE, blank=True, null=True)
    
    reference_number = models.CharField(max_length=100, unique=True) # this is different to django's auto-generated id
    
    age = models.IntegerField(verbose_name='Age (years)')
    sex = models.IntegerField(verbose_name='Sex', choices=[(1, 'Male'), (0, 'Female')], default=1)
    cp = models.IntegerField(verbose_name='Chest Pain Type', choices=[(1, 'Typical Angina'), (2, 'Atypical Angina'), (3, 'Non-Anginal Pain'), (4, 'Asymptomatic')])  
    trestbps = models.IntegerField(verbose_name='Resting Blood Pressure (mm Hg) on admission to the hospital')
    chol = models.FloatField(verbose_name='Total Serum Cholesterol (mg/dl)')
    fbs = models.IntegerField(verbose_name='Fasting Blood Sugar > 120 mg/dl?', choices=[(1, 'True'), (0, 'False')], default=1)
    restecg = models.IntegerField(verbose_name='Resting Electrocardiographic Results', choices=[(0, 'Normal'), (1, 'Abnormal - ST-T wave'), (2, 'Abnormal - Left Ventricular Hypertrophy')])
    thalach = models.IntegerField(verbose_name='Maximum Heart Rate Achieved')
    exang = models.IntegerField(verbose_name='Exercise Induced Angina?', choices=[(1, 'Yes'), (0, 'No')], default=0)
    oldpeak = models.FloatField(verbose_name='ST Depression Induced by Exercise Relative to Rest')
    slope = models.IntegerField(verbose_name='Slope of the Peak Exercise ST Segment', choices=[(1, 'Upsloping'), (2, 'Flat'), (3, 'Downsloping')])
    ca = models.FloatField(verbose_name='Number of Major Vessels (0-3) Colored by Fluoroscopy')
    thal = models.IntegerField(verbose_name='Thalassemia', choices=[(3, 'Normal'), (6, 'Fixed Defect'), (7, 'Reversible Defect')])

    image = models.ImageField(verbose_name="Electrocardiogram (ECG)", upload_to='images/', blank=True, null=True)
    video = models.FileField(verbose_name="Echocardiogram", upload_to='videos/', blank=True, null=True)

    diagnosis = models.CharField(max_length=255)  # CharField for shorter entries
    prognosis = models.TextField() # TextField for longer entries

    def __str__(self):
        return f"Doctor-Patient File: {self.doctor.first_name} {self.doctor.last_name} - {self.patient.first_name} {self.patient.last_name}" if self.doctor and self.patient else f"Doctor-Patient File: {self.doctor.first_name} {self.doctor.last_name}" if self.doctor else "Doctor-Patient File: anon"

