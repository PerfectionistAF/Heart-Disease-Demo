# Generated by Django 5.0.3 on 2024-04-28 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_doctorpatientfile_ca_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorpatientfile',
            name='chol',
            field=models.FloatField(verbose_name='Total Serum Cholesterol (mg/dl)'),
        ),
        migrations.AlterField(
            model_name='doctorpatientfile',
            name='cp',
            field=models.IntegerField(choices=[(1, 'Typical Angina'), (2, 'Atypical Angina'), (3, 'Non-Anginal Pain'), (4, 'Asymptomatic')], max_length=256, verbose_name='Chest Pain Type'),
        ),
        migrations.AlterField(
            model_name='doctorpatientfile',
            name='exang',
            field=models.IntegerField(choices=[(1, 'Yes'), (0, 'No')], default=0, verbose_name='Exercise Induced Angina?'),
        ),
        migrations.AlterField(
            model_name='doctorpatientfile',
            name='fbs',
            field=models.IntegerField(choices=[(1, 'True'), (0, 'False')], default=1, verbose_name='Fasting Blood Sugar > 120 mg/dl?'),
        ),
        migrations.AlterField(
            model_name='doctorpatientfile',
            name='restecg',
            field=models.IntegerField(choices=[(0, 'Normal'), (1, 'Abnormal - ST-T wave'), (2, 'Abnormal - Left Ventricular Hypertrophy')], max_length=256, verbose_name='Resting Electrocardiographic Results'),
        ),
        migrations.AlterField(
            model_name='doctorpatientfile',
            name='sex',
            field=models.IntegerField(choices=[(1, 'Male'), (0, 'Female')], default=1, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='doctorpatientfile',
            name='slope',
            field=models.IntegerField(choices=[(1, 'Upsloping'), (2, 'Flat'), (3, 'Downsloping')], max_length=256, verbose_name='Slope of the Peak Exercise ST Segment'),
        ),
        migrations.AlterField(
            model_name='doctorpatientfile',
            name='thal',
            field=models.IntegerField(choices=[(3, 'Normal'), (6, 'Fixed Defect'), (7, 'Reversible Defect')], max_length=256, verbose_name='Thalassemia'),
        ),
    ]
