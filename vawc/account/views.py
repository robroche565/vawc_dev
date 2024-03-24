from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse

from account.models import *

# Create your views here.
def request_passkey (request):
  email = request.POST.get('requester')
  
  existing_passkey_reset = Passkey_Reset.objects.filter(email=email).exists()
  print(existing_passkey_reset)
  
  message = ''
  
  if existing_passkey_reset:
    message =  'Passkey request already exists for this email.'
  else:
    message = 'Passkey request created successfully.'
    passkey_reset_instance = Passkey_Reset(
              email=email,
              status='pending',
              date=timezone.now()
    )
    passkey_reset_instance.save()

  return JsonResponse({'success': True, 'message': message})

  