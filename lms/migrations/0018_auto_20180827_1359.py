# Generated by Django 2.0.6 on 2018-08-27 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0017_submitted_assignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submitted_assignment',
            name='upload_assignment',
            field=models.FileField(upload_to='documents/submitted_assignments/'),
        ),
    ]
