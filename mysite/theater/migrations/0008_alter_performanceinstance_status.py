# Generated by Django 4.0.6 on 2022-07-21 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater', '0007_performanceinstance_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performanceinstance',
            name='status',
            field=models.CharField(choices=[('Yra laisvų vietų', 'Yra laisvų vietų'), ('Nėra laisvų vietų', 'Nėra laisvų vietų')], default='Yra laisvų vietų', help_text='Statusas', max_length=20),
        ),
    ]