# Generated by Django 5.0.1 on 2024-02-17 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0017_alter_case_place_of_incident'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='place_of_incident',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='service_information',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='type_of_case',
            field=models.CharField(default='Pending', max_length=30),
        ),
    ]
