# Generated by Django 5.0.1 on 2024-02-22 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0022_alter_parent_educational_attainment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_description', models.TextField()),
                ('status_date_added', models.DateField()),
                ('case_status_history', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='status_history', to='case.case')),
            ],
        ),
    ]
