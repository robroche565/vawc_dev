from django.shortcuts import render, redirect
from django.http import JsonResponse
from case.models import *
from django.views.decorators.http import require_POST
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
import uuid
from django.utils import timezone
# Create your views here.

def home_view (request):
    return render(request, 'landing/home.html')

def report_violence_view (request):
    return render(request, 'landing/report_violence.html')

def impact_victim_view (request):
    return render(request, 'landing/case_type/impacted-victim.html')

def behalf_victim_view (request):
    return render(request, 'landing/case_type/behalf-victim.html')

def add_case(request):
    if request.method == 'POST':
        case_data = {
            'case_number': get_next_case_number(),
            'date_latest_incident': request.POST.get('date-latest-incident'),
            'incomplete_date': request.POST.get('incomplete-date'),
            'place_of_incident': request.POST.get('place-incident'),
            'street': request.POST.get('incident-street'),
            'barangay': request.POST.get('incident-barangay'),
            'province': request.POST.get('incident-province'),
            'city': request.POST.get('incident-city'),
            'region': request.POST.get('incident-region'),
            'description_of_evidence': request.POST.get('incident-desc'),
            'service_information': request.POST.get('service'),
            'type_of_case': request.POST.get('type_of_case'),  # Collecting type of case from the form
        }
        case_instance = Case.objects.create(**case_data)

        if 'evidence_file' in request.FILES:
            handle_evidence_files(request.FILES.getlist('evidence_file'), case_instance)

        # Get dynamic victim data
        victim_instances = []
        victim_form_prefix = 'victim-'  # Adjust this prefix according to your form field names
        victim_count = int(request.POST.get('victim_count'))  # Assuming you have a hidden input for victim count
        for i in range(victim_count):
            victim_data = get_victim_data(request.POST, prefix=victim_form_prefix, index=i)
            victim_instance = Victim.objects.create(case_victim=case_instance, **victim_data)
            victim_instances.append(victim_instance)

        # Perpetrator data handling
        perpetrator_count = int(request.POST.get('perpetrator_count'))  # Assuming you have a hidden input for perpetrator count
        for i in range(perpetrator_count):
            perpetrator_data = get_perpetrator_data(request.POST, index=i)
            perpetrator_instance = Perpetrator.objects.create(case_perpetrator=case_instance, **perpetrator_data)

        contact_person_data = get_contact_person_data(request.POST)
        contact_person_instance = Contact_Person.objects.create(case_contact=case_instance, **contact_person_data)

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})



def get_next_case_number():
    latest_case_number = Case.objects.aggregate(Max('case_number'))['case_number__max']
    return 1 if latest_case_number is None else latest_case_number + 1

def handle_evidence_files(files, case_instance):
    for file in files:
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        unique_filename = str(uuid.uuid4()) + os.path.splitext(file.name)[-1]
        filename = fs.save(unique_filename, file)
        evidence_instance = Evidence.objects.create(case=case_instance, file=filename)

def get_victim_data(post_data, prefix, index):
    victim_data = {
        'first_name': post_data.get(f'{prefix}firstname_{index}'),
        'middle_name': post_data.get(f'{prefix}middlename_{index}'),
        'last_name': post_data.get(f'{prefix}lastname_{index}'),
        'suffix': post_data.get(f'{prefix}Suffix_{index}'),
        'sex': post_data.get(f'{prefix}sex_{index}'),
        'age': post_data.get(f'{prefix}age_{index}'),
        'civil_status': post_data.get(f'{prefix}civilstatus_{index}'),
        'nationality': post_data.get(f'{prefix}nationality_{index}'),
        'contact_number': post_data.get(f'{prefix}contact-number_{index}'),
        'telephone_number': post_data.get(f'{prefix}tel-number_{index}'),
        'house_information': post_data.get(f'{prefix}house-info_{index}'),
        'street': post_data.get(f'{prefix}street_{index}'),
        'barangay': post_data.get(f'{prefix}barangay_{index}'),
        'province': post_data.get(f'{prefix}province_{index}'),
        'city': post_data.get(f'{prefix}city_{index}'),
        'region': post_data.get(f'{prefix}region_{index}'),
    }
    return victim_data

def get_perpetrator_data(post_data, index):
    perpetrator_data = {
        'first_name': post_data.get(f'perp-firstname_{index}'),
        'middle_name': post_data.get(f'perp-middlename_{index}'),
        'last_name': post_data.get(f'perp-lastname_{index}'),
        'suffix': post_data.get(f'perp-Suffix_{index}'),
        'alias': post_data.get(f'perp-alias_{index}'),
        'sex': post_data.get(f'perp-sex_{index}'),
        'age': post_data.get(f'perp-age_{index}'),
        'nationality': post_data.get(f'perp-nationality_{index}'),
        'identifying_marks': post_data.get(f'perp-identifying-marks_{index}'),
        'house_information': post_data.get(f'perp-address-info_{index}'),
        'street': post_data.get(f'perp-street_{index}'),
        'barangay': post_data.get(f'perp-barangay_{index}'),
        'province': post_data.get(f'perp-province_{index}'),
        'city': post_data.get(f'perp-city_{index}'),
        'region': post_data.get(f'perp-region_{index}'),
        'relationship_to_victim': post_data.get(f'perp-relationsip-victim_{index}'),
    }
    return perpetrator_data

def get_contact_person_data(post_data):
    contact_person_data = {
        'first_name': post_data.get('contact-firstname'),
        'middle_name': post_data.get('contact-midname'),
        'last_name': post_data.get('contact-lastname'),
        'suffix': post_data.get('contact-Suffix'),
        'relationship': post_data.get('relationship'),
        'street': post_data.get('contact-street'),
        'barangay': post_data.get('contact-barangay'),
        'city': post_data.get('contact-city'),
        'province': post_data.get('contact-province'),
        'contact_number': post_data.get('contact-number'),
        'telephone_number': post_data.get('contact-tel'),
        'region': post_data.get('contact-region'),
    }
    return contact_person_data

