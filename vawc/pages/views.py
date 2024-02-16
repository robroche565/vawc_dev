from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import auth
from django.conf import settings
import uuid
from django.core.mail import send_mail, EmailMultiAlternatives 
from django.template.loader import render_to_string
from django.conf import settings
import random
import string
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
import json
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
# Create your views here.

#models
from case.models import *
from account.models import *

def home_view (request):
    return render(request, 'landing/home.html')

def login_view (request):
    return render(request, 'login/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def admin_dashboard_view (request):
    return render(request, 'super-admin/dashboard.html')

@login_required
def admin_graph_view (request):
    return render(request, 'super-admin/graph_report.html')

@login_required
def barangay_dashboard_view (request):
    return render(request, 'barangay-admin/dashboard.html')

@login_required
def barangay_case_view(request):
    cases = Case.objects.all()  # Retrieve all cases from the database
    return render(request, 'barangay-admin/case/case.html', {'cases': cases})


def send_otp_email(email, otp):
    subject = 'One-Time Password Verification'
    message = (
        f'--------------------------\n'
        f'One-Time Password Verification\n'
        f'--------------------------\n\n'
        f'Your One-Time Password (OTP) is: {otp}\n\n'
        f'Please use this OTP to verify your account.\n\n'
        f'This OTP will expire in 5 minutes.\n\n'
        f'--------------------------\n'
        f'This email was sent automatically. Please do not reply.'
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def login_with_otp(request):
    if request.method == 'POST':
        email = request.POST.get('barangay-email')
        passkey = request.POST.get('barangay-passkey')
        # Check if the user exists
        user = CustomUser.objects.filter(email=email).first()
        if user:
            # Validate passkey
            user_authenticated = authenticate(request, username=email, password=passkey)
            if user_authenticated:
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['user_email'] = email  # Store user email in session for later retrieval
                otp_expiry = timezone.now() + timezone.timedelta(minutes=5)
                request.session['otp_expiry'] = otp_expiry.isoformat()  # Convert datetime to string
                send_otp_email(email, otp)
                return JsonResponse({'success': True, 'message': 'OTP has been sent to your email.'})
            else:
                print('Invalid passkey. Please try again.')
                return JsonResponse({'success': False, 'message': 'Invalid passkey. Please try again.'})
        else:
            print('Account not found.')
            return JsonResponse({'success': False, 'message': 'Account not found.'})
    return render(request, 'login/login.html')


def verify_otp(request):
    if request.method == 'POST':
        otp_entered = ''
        for i in range(1, 7):  # Iterate through OTP fields from 1 to 6
            otp_entered += request.POST.get(f'otp_{i}', '')

        otp_saved = None
        otp_expiry_str = None

        # Check all possible OTP fields
        for i in range(1, 4):  # Adjust the range based on your maximum OTP fields
            otp_saved = request.session.get('otp')
            otp_expiry_str = request.session.get('otp_expiry')
            user_email = request.session.get('user_email')
            print(user_email)
            if otp_saved and otp_expiry_str:
                otp_expiry = timezone.datetime.fromisoformat(otp_expiry_str)
                if timezone.now() < otp_expiry and otp_entered == otp_saved:
                    user = CustomUser.objects.filter(email=user_email).first()
                    if user:
                        login(request, user)  # Logging in the user
                        request.session.pop('otp')
                        request.session.pop('otp_expiry')
                        request.session.pop('user_email')

                        # Fetch the account type of the user
                        account_type = Account.objects.filter(user=user).first().type

                        # Print a success message
                        print("User logged in successfully")
                        print(account_type)

                        # Return success along with account type
                        return JsonResponse({'success': True, 'message': 'Login successful.', 'account_type': account_type, 'otp_expiry': otp_expiry_str})
                    else:
                        return JsonResponse({'success': False, 'message': 'User not found.'})
                elif timezone.now() >= otp_expiry:
                    return JsonResponse({'success': False, 'message': 'Code is already expired.', 'otp_expiry': otp_expiry_str})
                else:
                    break
        # If OTP is incorrect
        return JsonResponse({'success': False, 'message': 'OTP Inputted is not Correct.', 'otp_expiry': otp_expiry_str})

    return JsonResponse({'success': False, 'message': 'Invalid request.'}, encoder=DjangoJSONEncoder)

def resend_otp(request):
    if request.method == 'GET':
        user_email = request.session.get('user_email')  # Corrected key
        if user_email:
            try:
                user = CustomUser.objects.get(email=user_email)
                otp = generate_otp()  # Assuming you have a function to generate OTP
                request.session['otp'] = otp
                otp_expiry = timezone.now() + timezone.timedelta(minutes=5)
                request.session['otp_expiry'] = otp_expiry.isoformat()
                send_otp_email(user_email, otp)  # Assuming you have a function to send OTP email
                return JsonResponse({'success': True, 'message': 'OTP resent successfully.'})
            except ObjectDoesNotExist:
                return JsonResponse({'success': False, 'message': 'User not found.'})
        else:
            return JsonResponse({'success': False, 'message': 'User email not found in session.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


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
            'date_added': timezone.now(),
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
        'date_of_birth': post_data.get(f'{prefix}date-of-birth_{index}'),
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
        'date_of_birth': post_data.get(f'perp-date-of-birth_{index}'),
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


@login_required
def view_case(request, case_id):
    try:
        # Retrieve the case object from the database based on the case_id
        case = Case.objects.get(id=case_id)
        # Retrieve related objects such as contact persons, evidence, victims, perpetrators, and parents
        contact_persons = Contact_Person.objects.filter(case_contact=case)
        evidences = Evidence.objects.filter(case=case)
        victims = Victim.objects.filter(case_victim=case)
        perpetrators = Perpetrator.objects.filter(case_perpetrator=case)
        parents = Parent.objects.filter(victim_parent__in=victims)

        # Render the view-case.html template with the case and related objects as context
        return render(request, 'barangay-admin/case/view-case.html', {
            'case': case,
            'contact_persons': contact_persons,
            'evidence': evidences,
            'victims': victims,
            'perpetrators': perpetrators,
            'parents': parents,
        })
    except Case.DoesNotExist:
        # Handle case not found appropriately, for example, return a 404 page
        return HttpResponseNotFound("Case not found")

@require_POST
def save_victim_data(request, victim_id):
    try:
        victim = get_object_or_404(Victim, id=victim_id)

        # Update victim data
        victim.first_name = request.POST.get('victim_first_name_' + str(victim_id))
        victim.middle_name = request.POST.get('victim_middle_name_' + str(victim_id))
        victim.last_name = request.POST.get('victim_last_name_' + str(victim_id))
        victim.suffix = request.POST.get('victim_suffix_name_' + str(victim_id))
        victim.sex = request.POST.get('victim_sex_' + str(victim_id))
        victim.type_of_disability = request.POST.get('victim_type_of_disability_' + str(victim_id))
        victim.date_of_birth = request.POST.get('victim_date_of_birth_' + str(victim_id))
        victim.civil_status = request.POST.get('victim_civil_status_' + str(victim_id))
        victim.contact_number = request.POST.get('victim_contact_number_' + str(victim_id))
        victim.telephone_number = request.POST.get('victim_telephone_number_' + str(victim_id))
        victim.educational_attainment = request.POST.get('victim_educational_attainment_' + str(victim_id))
        victim.occupation = request.POST.get('victim_occupation_' + str(victim_id))
        victim.nationality = request.POST.get('victim_nationality_' + str(victim_id))
        victim.religion = request.POST.get('victim_religion_' + str(victim_id))
        victim.house_information = request.POST.get('victim_house_information_' + str(victim_id))
        victim.street = request.POST.get('victim_street_' + str(victim_id))
        victim.barangay = request.POST.get('victim_barangay_' + str(victim_id))
        victim.province = request.POST.get('victim_province_' + str(victim_id))
        victim.city = request.POST.get('victim_city_' + str(victim_id))
        victim.region = request.POST.get('victim_region_' + str(victim_id))

        # Save victim data
        victim.save()

        return JsonResponse({'success': True, 'message': 'Victim data saved successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@require_POST
def save_perpetrator_data(request, perpetrator_id):
    try:
        perpetrator = get_object_or_404(Perpetrator, id=perpetrator_id)
        
        # Update perpetrator data
        perpetrator.first_name = request.POST.get('perpetrator_first_name_' + str(perpetrator_id))
        perpetrator.middle_name = request.POST.get('perpetrator_middle_name_' + str(perpetrator_id))
        perpetrator.last_name = request.POST.get('perpetrator_last_name_' + str(perpetrator_id))
        perpetrator.suffix = request.POST.get('perpetrator_suffix_name_' + str(perpetrator_id))
        perpetrator.identifying_marks = request.POST.get('perpetrator_identifying_marks_' + str(perpetrator_id))
        perpetrator.alias = request.POST.get('perpetrator_alias_' + str(perpetrator_id))
        perpetrator.relationship_to_victim = request.POST.get('perp-relationship-victim_' + str(perpetrator_id))
        perpetrator.sex = request.POST.get('perpetrator_sex_' + str(perpetrator_id))
        perpetrator.type_of_disability = request.POST.get('perpetrator_type_of_disability_' + str(perpetrator_id))
        perpetrator.date_of_birth = request.POST.get('perpetrator_date_of_birth_' + str(perpetrator_id))
        perpetrator.civil_status = request.POST.get('perpetrator_civil_status_' + str(perpetrator_id))
        perpetrator.contact_number = request.POST.get('perpetrator_contact_number_' + str(perpetrator_id))
        perpetrator.telephone_number = request.POST.get('perpetrator_telephone_number_' + str(perpetrator_id))
        perpetrator.educational_attainment = request.POST.get('perpetrator_educational_attainment_' + str(perpetrator_id))
        perpetrator.occupation = request.POST.get('perpetrator_occupation_' + str(perpetrator_id))
        perpetrator.nationality = request.POST.get('perpetrator_nationality_' + str(perpetrator_id))
        perpetrator.religion = request.POST.get('perpetrator_religion_' + str(perpetrator_id))
        perpetrator.house_information = request.POST.get('perpetrator_house_information_' + str(perpetrator_id))
        perpetrator.street = request.POST.get('perpetrator_street_' + str(perpetrator_id))
        perpetrator.barangay = request.POST.get('perpetrator_barangay_' + str(perpetrator_id))
        perpetrator.province = request.POST.get('perpetrator_province_' + str(perpetrator_id))
        perpetrator.city = request.POST.get('perpetrator_city_' + str(perpetrator_id))
        perpetrator.region = request.POST.get('perpetrator_region_' + str(perpetrator_id))

        # Save perpetrator data
        perpetrator.save()

        return JsonResponse({'success': True, 'message': 'Perpetrator data saved successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def add_parent(request, case_id, victim_id):
    case = Case.objects.get(id=case_id)
    victim = Victim.objects.get(id=victim_id)
    return render(request, 'barangay-admin/case/add-parent.html', {
            'victim': victim,
            'case': case,  # Include the 'case' variable in the context
        })