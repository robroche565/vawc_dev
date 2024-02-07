from django.shortcuts import render, redirect
from django.http import JsonResponse
from case.models import *
from django.views.decorators.http import require_POST
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
import uuid
# Create your views here.

def home_view (request):
    return render(request, 'landing/home.html')

def report_violence_view (request):
    return render(request, 'landing/report_violence.html')

def impact_victim_view (request):
    return render(request, 'landing/impacted/impacted-victim.html')

@require_POST
def add_impact_victim(request):
    # Calculate the next available unique case number
    latest_case_number = Case.objects.aggregate(Max('case_number'))['case_number__max']
    next_case_number = 1 if latest_case_number is None else latest_case_number + 1

    # Ensure the generated case number is unique
    while Case.objects.filter(case_number=next_case_number).exists():
        next_case_number += 1

    # Convert the case number to a 5-digit string with leading zeros
    next_case_number_str = str(next_case_number).zfill(5)

    # Parse form data for Case
    date_latest_incident = request.POST.get('date-latest-incident')
    incomplete_date = request.POST.get('incomplete-date')
    place_of_incident = request.POST.get('place-incident')
    street = request.POST.get('incident-street')
    barangay = request.POST.get('incident-barangay')
    province = request.POST.get('incident-province')
    city = request.POST.get('incident-city')
    region = request.POST.get('incident-region')
    description_of_evidence = request.POST.get('incident-desc')
    service_information = request.POST.get('service')

    # Create Case instance and save to database
    case_instance = Case.objects.create(
        case_number=next_case_number_str,
        date_latest_incident=date_latest_incident,
        incomplete_date=incomplete_date,
        place_of_incident=place_of_incident,
        street=street,
        barangay=barangay,
        province=province,
        city=city,
        region=region,
        description_of_evidence=description_of_evidence,
        service_information=service_information
    )
    # Handle file upload for evidence
    if 'evidence_file' in request.FILES:
        for file in request.FILES.getlist('evidence_file'):
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # Use MEDIA_ROOT as the base location
            filename = fs.save(file.name, file)  # Use original filename directly
            evidence_instance = Evidence.objects.create(case=case_instance, file=filename)
    # Parse form data for Victim
    first_name = request.POST.get('victim-firstname')
    middle_name = request.POST.get('victim-middlename')
    last_name = request.POST.get('victim-lastname')
    suffix = request.POST.get('victim-Suffix')
    sex = request.POST.get('victim-sex')
    age = request.POST.get('victim-age')
    civil_status = request.POST.get('victim-civilstatus')
    nationality = request.POST.get('victim-nationality')
    contact_number = request.POST.get('victim-contact-number')
    tel_number = request.POST.get('victim-tel-number')
    house_info = request.POST.get('victim-house-info')
    street = request.POST.get('victim-street')
    barangay = request.POST.get('victim-barangay')
    province = request.POST.get('victim-province')
    city = request.POST.get('victim-city')
    region = request.POST.get('victim-region')

    # Create Victim instance with case_victim set to the newly created Case instance and save to database
    victim_instance = Victim.objects.create(
        case_victim=case_instance,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        suffix=suffix,
        sex=sex,
        age=age,
        civil_status=civil_status,
        nationality=nationality,
        contact_number=contact_number,
        telephone_number=tel_number,
        house_information=house_info,
        street=street,
        barangay=barangay,
        province=province,
        city=city,
        region=region
    )
    # Parse form data for Perpetrator
    perp_first_name = request.POST.get('perp-firstname')
    perp_middle_name = request.POST.get('perp-middlename')
    perp_last_name = request.POST.get('perp-lastname')
    perp_suffix = request.POST.get('perp-Suffix')
    perp_alias = request.POST.get('perp-alias')
    perp_sex = request.POST.get('perp-sex')
    perp_age = request.POST.get('perp-age')
    perp_nationality = request.POST.get('perp-nationality')
    perp_identifying_marks = request.POST.get('perp-identifying-marks')
    perp_house_info = request.POST.get('perp-address-info')
    perp_street = request.POST.get('perp-street')
    perp_barangay = request.POST.get('perp-barangay')
    perp_province = request.POST.get('perp-province')
    perp_city = request.POST.get('perp-city')
    perp_region = request.POST.get('perp-region')
    perp_relationship_to_victim = request.POST.get('perp-relationsip-victim')

    # Create Perpetrator instance with case_perpetrator set to the newly created Case instance and save to database
    perpetrator_instance = Perpetrator.objects.create(
        case_perpetrator=case_instance,
        first_name=perp_first_name,
        middle_name=perp_middle_name,
        last_name=perp_last_name,
        suffix=perp_suffix,
        alias=perp_alias,
        sex=perp_sex,
        age=perp_age,
        nationality=perp_nationality,
        identifying_marks=perp_identifying_marks,
        house_information=perp_house_info,
        street=perp_street,
        barangay=perp_barangay,
        province=perp_province,
        city=perp_city,
        region=perp_region,
        relationship_to_victim=perp_relationship_to_victim
    )

    return JsonResponse({'success': True})
    #return redirect('home')  # Replace 'success_page' with the name of your success page URL pattern
