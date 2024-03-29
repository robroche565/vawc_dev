# Generated by Django 5.0.1 on 2024-03-12 18:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_number', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('type_of_case', models.CharField(blank=True, default='Pending', max_length=30, null=True)),
                ('service_information', models.CharField(blank=True, max_length=20, null=True)),
                ('date_latest_incident', models.CharField(blank=True, max_length=150, null=True)),
                ('incomplete_date', models.BooleanField(default=False, null=True)),
                ('place_of_incident', models.CharField(blank=True, max_length=150, null=True)),
                ('street', models.CharField(blank=True, max_length=150, null=True)),
                ('barangay', models.CharField(blank=True, max_length=150, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=250, null=True)),
                ('description_of_incident', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Close', 'Close')], default='Active', max_length=20)),
                ('date_added', models.DateField(blank=True, null=True)),
                ('checkbox_ra_9262', models.BooleanField(default=False)),
                ('checkbox_sexual_abuse', models.BooleanField(default=False)),
                ('checkbox_psychological_abuse', models.BooleanField(default=False)),
                ('checkbox_physical_abuse', models.BooleanField(default=False)),
                ('checkbox_economic_abuse', models.BooleanField(default=False)),
                ('checkbox_others', models.BooleanField(default=False)),
                ('others_input', models.CharField(blank=True, max_length=100, null=True)),
                ('checkbox_ra_8353', models.BooleanField(default=False)),
                ('checkbox_rape_by_sexual_intercourse', models.BooleanField(default=False)),
                ('checkbox_rape_by_sexual_assault', models.BooleanField(default=False)),
                ('checkbox_art_336', models.BooleanField(default=False)),
                ('checkbox_acts_of_lasciviousness', models.BooleanField(default=False)),
                ('checkbox_ra_7877', models.BooleanField(default=False)),
                ('checkbox_verbal', models.BooleanField(default=False)),
                ('checkbox_physical', models.BooleanField(default=False)),
                ('checkbox_use_of_objects', models.BooleanField(default=False)),
                ('checkbox_a_7610', models.BooleanField(default=False)),
                ('checkbox_engage_prostitution', models.BooleanField(default=False)),
                ('checkbox_sexual_lascivious_conduct', models.BooleanField(default=False)),
                ('checkbox_ra_9775', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Contact_Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('suffix', models.CharField(blank=True, max_length=10, null=True)),
                ('relationship', models.CharField(blank=True, max_length=50, null=True)),
                ('street', models.CharField(blank=True, max_length=150, null=True)),
                ('barangay', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=100, null=True)),
                ('telephone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=250, null=True)),
                ('case_contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_person', to='case.case')),
            ],
        ),
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidence', to='case.case')),
            ],
        ),
        migrations.CreateModel(
            name='Perpetrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_to_victim', models.CharField(blank=True, max_length=100, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('suffix', models.CharField(blank=True, max_length=10, null=True)),
                ('identifying_marks', models.CharField(blank=True, max_length=250, null=True)),
                ('alias', models.CharField(blank=True, max_length=100, null=True)),
                ('sex', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.CharField(blank=True, max_length=150, null=True)),
                ('educational_attainment', models.CharField(blank=True, max_length=50, null=True)),
                ('type_of_disability', models.CharField(blank=True, max_length=50, null=True)),
                ('civil_status', models.CharField(blank=True, max_length=100, null=True)),
                ('occupation', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=100, null=True)),
                ('telephone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('religion', models.CharField(blank=True, max_length=50, null=True)),
                ('nationality', models.CharField(blank=True, max_length=50, null=True)),
                ('house_information', models.CharField(blank=True, max_length=250, null=True)),
                ('street', models.CharField(blank=True, max_length=150, null=True)),
                ('barangay', models.CharField(blank=True, max_length=150, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=250, null=True)),
                ('case_perpetrator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='perpetrator', to='case.case')),
            ],
        ),
        migrations.CreateModel(
            name='Parent_Perpetrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('suffix', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.CharField(blank=True, max_length=150, null=True)),
                ('sex', models.CharField(blank=True, max_length=100, null=True)),
                ('civil_status', models.CharField(blank=True, max_length=100, null=True)),
                ('educational_attainment', models.CharField(blank=True, max_length=150, null=True)),
                ('occupation', models.CharField(blank=True, max_length=150, null=True)),
                ('type_of_disability', models.CharField(blank=True, max_length=150, null=True)),
                ('nationality', models.CharField(blank=True, max_length=150, null=True)),
                ('religion', models.CharField(blank=True, max_length=150, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=100, null=True)),
                ('telephone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('house_information', models.CharField(blank=True, max_length=250, null=True)),
                ('street', models.CharField(blank=True, max_length=150, null=True)),
                ('barangay', models.CharField(blank=True, max_length=150, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=250, null=True)),
                ('perpetrator_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_perp', to='case.perpetrator')),
            ],
        ),
        migrations.CreateModel(
            name='Status_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_title', models.CharField(blank=True, max_length=150, null=True)),
                ('status_description', models.TextField(blank=True, null=True)),
                ('status_event_date', models.DateTimeField(blank=True, null=True)),
                ('status_date_added', models.DateTimeField(blank=True, null=True)),
                ('case_status_history', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='status_history', to='case.case')),
            ],
        ),
        migrations.CreateModel(
            name='Victim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('suffix', models.CharField(blank=True, max_length=150, null=True)),
                ('date_of_birth', models.CharField(blank=True, max_length=150, null=True)),
                ('sex', models.CharField(blank=True, max_length=100, null=True)),
                ('civil_status', models.CharField(blank=True, max_length=100, null=True)),
                ('educational_attainment', models.CharField(blank=True, max_length=50, null=True)),
                ('occupation', models.CharField(blank=True, max_length=50, null=True)),
                ('type_of_disability', models.CharField(blank=True, max_length=50, null=True)),
                ('nationality', models.CharField(blank=True, max_length=50, null=True)),
                ('religion', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=100, null=True)),
                ('telephone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('house_information', models.CharField(blank=True, max_length=250, null=True)),
                ('street', models.CharField(blank=True, max_length=150, null=True)),
                ('barangay', models.CharField(blank=True, max_length=150, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=250, null=True)),
                ('case_victim', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='case.case')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('suffix', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.CharField(blank=True, max_length=150, null=True)),
                ('sex', models.CharField(blank=True, max_length=100, null=True)),
                ('civil_status', models.CharField(blank=True, max_length=100, null=True)),
                ('educational_attainment', models.CharField(blank=True, max_length=150, null=True)),
                ('occupation', models.CharField(blank=True, max_length=150, null=True)),
                ('type_of_disability', models.CharField(blank=True, max_length=150, null=True)),
                ('nationality', models.CharField(blank=True, max_length=150, null=True)),
                ('religion', models.CharField(blank=True, max_length=150, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=100, null=True)),
                ('telephone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('house_information', models.CharField(blank=True, max_length=250, null=True)),
                ('street', models.CharField(blank=True, max_length=150, null=True)),
                ('barangay', models.CharField(blank=True, max_length=150, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=250, null=True)),
                ('victim_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='case.victim')),
            ],
        ),
        migrations.CreateModel(
            name='Witness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('case_witness', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_witness', to='case.case')),
            ],
        ),
    ]
