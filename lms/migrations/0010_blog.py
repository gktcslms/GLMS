# Generated by Django 2.0.6 on 2018-07-06 17:38

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0009_client_enquiry_job_seeker_learner_enquiry_vendor_enquiry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('image', models.ImageField(blank=True, upload_to='blog_pics/%Y/%m/%d/')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('draft', models.BooleanField(default=False)),
                ('publish', models.DateField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('blogger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.Custom_User')),
                ('likes', models.ManyToManyField(blank=True, related_name='blog_likes', to='lms.Custom_User')),
            ],
            options={
                'ordering': ['-created', '-updated'],
            },
        ),
    ]