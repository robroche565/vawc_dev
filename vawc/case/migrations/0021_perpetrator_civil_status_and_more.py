# Generated by Django 5.0.1 on 2024-02-17 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0020_alter_parent_victim_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='perpetrator',
            name='civil_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='perpetrator',
            name='type_of_disability',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
