# Generated by Django 2.0.6 on 2018-06-28 06:35

from django.db import migrations, models
import django.db.models.deletion
import lms.models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course_Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('video', models.FileField(blank=True, null=True, upload_to=lms.models.content_videofile_name)),
                ('Presentation', models.FileField(blank=True, null=True, upload_to=lms.models.content_pptfile_name)),
                ('Assignment', models.FileField(blank=True, null=True, upload_to=lms.models.content_assignmentfile_name)),
                ('topics', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('part_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='lms.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=200)),
                ('part_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.Course_Module')),
            ],
        ),
    ]
