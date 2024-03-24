from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.core.mail import send_mail 
from django.conf import settings

from account.models import *

import secrets
import string

# Create your views here.
def request_passkey (request):
  email = request.POST.get('requester')
  
  existing_passkey_reset = Passkey_Reset.objects.filter(email=email, status="pending").exists()

  message = ''
  
  if existing_passkey_reset:
    message =  "Passkey reset request already exists for the email with status 'Pending'"
  else:
    message = 'Passkey request created successfully.'
    passkey_reset_instance = Passkey_Reset(
              email=email,
              status='pending',
              date=timezone.now()
    )
    passkey_reset_instance.save()

  return JsonResponse({'success': True, 'message': message})

def update_passkey(request):
  email = request.POST.get('email')
  action = request.POST.get('action')
  
  if action == "approve":
    status = "approved"
    passkey = generate_passkey()
    message = "Your new passkey is " + passkey
    
    user = CustomUser.objects.filter(email=email).first()  # Or use .get() if you expect only one object to match the filter
    account = user.account

    account.passkey = passkey
    account.save()
  else:
    status = "declined"
    message = "Unfortunately, your request for new passkey is " + status

  subject = "Request for new passkey is " + status
  send_email(email, subject, message)
  Passkey_Reset.objects.filter(email=email).update(status=status)

  return JsonResponse({'success': True})

def send_email(receiver, subject, message):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [receiver])
  
def generate_passkey(length=12):
    """Generate a random passkey containing only letters."""
    # Define the character set for generating passkey (only letters)
    characters = string.ascii_letters
    
    # Generate a random passkey using secrets.choice()
    passkey = ''.join(secrets.choice(characters) for _ in range(length))
    
    return passkey