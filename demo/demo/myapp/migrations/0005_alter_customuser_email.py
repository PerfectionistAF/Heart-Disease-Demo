# Generated by Django 5.0.3 on 2024-04-24 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_doctorpatientfile_delete_usersubmission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=256, unique=True),
        ),
    ]
