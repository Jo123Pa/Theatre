# Generated by Django 4.0.6 on 2022-07-20 16:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('theater', '0005_performanceinstance_viewer_alter_performance_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performanceinstance',
            name='viewer',
        ),
        migrations.AddField(
            model_name='performanceinstance',
            name='viewer',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
