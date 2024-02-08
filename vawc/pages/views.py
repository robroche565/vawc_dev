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

@require_POST
def add_case(request):
    if request.method == 'POST':
        type_of_case = request.POST.get('type_of_case')
        # Calculate the next available unique case number
        latest_case_number = Case.objects.aggregate(Max('case_number'))['case_number__max']
        next_case_number = 1 if latest_case_number is None else latest_case_number + 1

        # Ensure the generated case number is unique
        while Case.objects.filter(case_number=next_case_number).exists():
            next_case_number += 1

        # Convert the case number to a 5-digit string with leading zeros
        next_case_number_str = str(next_case_number).zfill(5)

        if type_of_case == 'Impacted':
            # Parse form data for Case
            date_latest_incident = request.POST.get('date-latest-incident')
            incomplete_date = request.POST.get('incomplete-date')
            place_of_incident = request.POST.get('place-incident')
            incident_street = request.POST.get('incident-street')
            incident_barangay = request.POST.get('incident-barangay')
            incident_province = request.POST.get('incident-province')
            incident_city = request.POST.get('incident-city')
            incident_region = request.POST.get('incident-region')
            incident_description_of_evidence = request.POST.get('incident-desc')
            incident_service_information = request.POST.get('service')

            # Create Case instance and save to database
            case_instance = Case.objects.create(
                case_number=next_case_number_str,
                date_latest_incident=date_latest_incident,
                incomplete_date=incomplete_date,
                place_of_incident=place_of_incident,
                street=incident_street,
                barangay=incident_barangay,
                province=incident_province,
                city=incident_city,
                region=incident_region,
                description_of_evidence=incident_description_of_evidence,
                service_information=incident_service_information,
                date_added=timezone.now()
            )
            # Handle file upload for evidence
            if 'evidence_file' in request.FILES:
                for file in request.FILES.getlist('evidence_file'):
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # Use MEDIA_ROOT as the base location
                    # Generate a unique filename using UUID
                    unique_filename = str(uuid.uuid4()) + os.path.splitext(file.name)[-1]
                    filename = fs.save(unique_filename, file)
                    evidence_instance = Evidence.objects.create(case=case_instance, file=filename)
            
            # Parse form data for Victim
            victim_first_name = request.POST.get('victim-firstname')
            victim_middle_name = request.POST.get('victim-middlename')
            victim_last_name = request.POST.get('victim-lastname')
            victim_suffix = request.POST.get('victim-Suffix')
            victim_sex = request.POST.get('victim-sex')
            victim_age = request.POST.get('victim-age')
            victim_civil_status = request.POST.get('victim-civilstatus')
            victim_nationality = request.POST.get('victim-nationality')
            victim_contact_number = request.POST.get('victim-contact-number')
            victim_tel_number = request.POST.get('victim-tel-number')
            victim_house_info = request.POST.get('victim-house-info')
            victim_street = request.POST.get('victim-street')
            victim_barangay = request.POST.get('victim-barangay')
            victim_province = request.POST.get('victim-province')
            victim_city = request.POST.get('victim-city')
            victim_region = request.POST.get('victim-region')

            # Create Victim instance with case_victim set to the newly created Case instance and save to database
            victim_instance = Victim.objects.create(
                case_victim=case_instance,
                first_name=victim_first_name,
                middle_name=victim_middle_name,
                last_name=victim_last_name,
                suffix=victim_suffix,
                sex=victim_sex,
                age=victim_age,
                civil_status=victim_civil_status,
                nationality=victim_nationality,
                contact_number=victim_contact_number,
                telephone_number=victim_tel_number,
                house_information=victim_house_info,
                street=victim_street,
                barangay=victim_barangay,
                province=victim_province,
                city=victim_city,
                region=victim_region
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
        elif type_of_case == 'Behalf':
            # Parse form data for Case
            date_latest_incident = request.POST.get('date-latest-incident')
            incomplete_date = request.POST.get('incomplete-date')
            place_of_incident = request.POST.get('place-incident')
            incident_street = request.POST.get('incident-street')
            incident_barangay = request.POST.get('incident-barangay')
            incident_province = request.POST.get('incident-province')
            incident_city = request.POST.get('incident-city')
            incident_region = request.POST.get('incident-region')
            incident_description_of_evidence = request.POST.get('incident-desc')
            incident_service_information = request.POST.get('service')

            # Create Case instance and save to database
            case_instance = Case.objects.create(
                case_number=next_case_number_str,
                date_latest_incident=date_latest_incident,
                incomplete_date=incomplete_date,
                place_of_incident=place_of_incident,
                street=incident_street,
                barangay=incident_barangay,
                province=incident_province,
                city=incident_city,
                region=incident_region,
                description_of_evidence=incident_description_of_evidence,
                service_information=incident_service_information,
                date_added=timezone.now()
            )
            # Handle file upload for evidence
            if 'evidence_file' in request.FILES:
                for file in request.FILES.getlist('evidence_file'):
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # Use MEDIA_ROOT as the base location
                    # Generate a unique filename using UUID
                    unique_filename = str(uuid.uuid4()) + os.path.splitext(file.name)[-1]
                    filename = fs.save(unique_filename, file)
                    evidence_instance = Evidence.objects.create(case=case_instance, file=filename)
            
            # Parse form data for Victim
            victim_first_name = request.POST.get('victim-firstname')
            victim_middle_name = request.POST.get('victim-middlename')
            victim_last_name = request.POST.get('victim-lastname')
            victim_suffix = request.POST.get('victim-Suffix')
            victim_sex = request.POST.get('victim-sex')
            victim_age = request.POST.get('victim-age')
            victim_civil_status = request.POST.get('victim-civilstatus')
            victim_nationality = request.POST.get('victim-nationality')
            victim_contact_number = request.POST.get('victim-contact-number')
            victim_tel_number = request.POST.get('victim-tel-number')
            victim_house_info = request.POST.get('victim-house-info')
            victim_street = request.POST.get('victim-street')
            victim_barangay = request.POST.get('victim-barangay')
            victim_province = request.POST.get('victim-province')
            victim_city = request.POST.get('victim-city')
            victim_region = request.POST.get('victim-region')

            # Create Victim instance with case_victim set to the newly created Case instance and save to database
            victim_instance = Victim.objects.create(
                case_victim=case_instance,
                first_name=victim_first_name,
                middle_name=victim_middle_name,
                last_name=victim_last_name,
                suffix=victim_suffix,
                sex=victim_sex,
                age=victim_age,
                civil_status=victim_civil_status,
                nationality=victim_nationality,
                contact_number=victim_contact_number,
                telephone_number=victim_tel_number,
                house_information=victim_house_info,
                street=victim_street,
                barangay=victim_barangay,
                province=victim_province,
                city=victim_city,
                region=victim_region
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
            # Parse form data for contact Person
            contact_first_name = request.POST.get('contact-firstname')
            contact_middle_name = request.POST.get('contact-midname')
            contact_last_name = request.POST.get('contact-lastname')
            contact_suffix = request.POST.get('contact-Suffix')
            contact_relationship = request.POST.get('relationship')
            contact_street = request.POST.get('contact-street')
            contact_barangay = request.POST.get('contact-barangay')
            contact_city = request.POST.get('contact-city')
            contact_province = request.POST.get('contact-province')
            contact_contact_number = request.POST.get('contact-number')
            contact_tel_number = request.POST.get('contact-tel')
            
        # Create Contact Person instance with case_Contact Person set to the newly created Case instance and save to database
        contact_person_instance = Contact_Person.objects.create(
            case_contact=case_instance,
            first_name=contact_first_name,
            middle_name=contact_middle_name,
            last_name=contact_last_name,
            suffix=contact_suffix,
            relationship=contact_relationship,
            street=contact_street,
            barangay=contact_barangay,
            city=contact_city,
            province=contact_province,
            contact_number=contact_contact_number,
            telephone_number=contact_tel_number
        )

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    #return redirect('home')  # Replace 'success_page' with the name of your success page URL pattern
