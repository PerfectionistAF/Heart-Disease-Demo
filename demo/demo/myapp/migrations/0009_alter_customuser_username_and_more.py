# Generated by Django 5.0.3 on 2024-04-28 02:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_doctorpatientfile_image_doctorpatientfile_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, default='anon', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='doctorpatientfile',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_files', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='doctorpatientfile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Electrocardiogram (ECG)'),
        ),
        migrations.AlterField(
            model_name='doctorpatientfile',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_files', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='doctorpatientfile',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/', verbose_name='Echocardiogram'),
        ),
    ]
