# Generated by Django 5.0.1 on 2024-02-06 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0002_perpetrator_case_perpetrator_victim_case_victim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='date_latest_incident',
            field=models.DateField(blank=True, null=True),
        ),
    ]
