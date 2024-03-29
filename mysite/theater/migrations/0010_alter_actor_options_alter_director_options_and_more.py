# Generated by Django 4.0.6 on 2022-07-26 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater', '0009_alter_actor_first_name_alter_actor_last_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actor',
            options={'verbose_name': 'actor', 'verbose_name_plural': 'actors'},
        ),
        migrations.AlterModelOptions(
            name='director',
            options={'verbose_name': 'director', 'verbose_name_plural': 'directors'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'genre', 'verbose_name_plural': 'genres'},
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'verbose_name': 'performance', 'verbose_name_plural': 'performances'},
        ),
        migrations.AlterModelOptions(
            name='performanceinstance',
            options={'ordering': ['performance_date'], 'verbose_name': 'performanceinstance', 'verbose_name_plural': 'performanceinstances'},
        ),
        migrations.AlterField(
            model_name='performanceinstance',
            name='status',
            field=models.CharField(choices=[('available', 'available'), ('not available', 'not available')], default='available', help_text='status', max_length=20),
        ),
    ]
