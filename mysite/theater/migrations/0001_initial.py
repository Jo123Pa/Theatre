# Generated by Django 4.0.6 on 2022-07-12 16:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Vardas')),
                ('last_name', models.CharField(max_length=100, verbose_name='Pavardė')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Įveskite knygos žandrą', max_length=200, verbose_name='Pavadinimas')),
            ],
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Pavadinimas')),
                ('author', models.CharField(max_length=200, verbose_name='Autorius')),
                ('summary', models.TextField(max_length=500, verbose_name='Aprašymas')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='covers', verbose_name='Cover')),
                ('actor', models.ManyToManyField(help_text='Pasirinkite spektaklio aktorius', to='theater.actor')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='theater.genre')),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, help_text='A unique ID for a performance')),
                ('performance_date', models.DateField(blank=True, null=True, verbose_name='Pasirodymas')),
                ('status', models.CharField(blank=True, choices=[('Yra laisvų vietų', 'Yra laisvų vietų'), ('Nėra laisvų vietų', 'Nėra laisvų vietų')], default='Yra laisvų vietų', help_text='Statusas', max_length=20)),
                ('performance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='theater.performance')),
            ],
            options={
                'ordering': ['performance_date'],
            },
        ),
    ]
