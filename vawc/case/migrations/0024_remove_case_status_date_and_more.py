# Generated by Django 5.0.1 on 2024-02-22 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0023_status_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='status_date',
        ),
        migrations.RemoveField(
            model_name='case',
            name='status_description',
        ),
    ]