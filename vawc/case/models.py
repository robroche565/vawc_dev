from django.db import models

# Create your models here.
class Case(models.Model):
    case_number = models.IntegerField(null=True, blank=True)
    date_latest_incident = models.DateField(null=True, blank=True)
    incomplete_date = models.BooleanField(default=False, null=True)
    place_of_incident = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=150, null=True, blank=True)
    barangay = models.CharField(max_length=150, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=250, null=True, blank=True)
    description_of_evidence = models.TextField(null=True, blank=True)
    CRISIS_INTERVENTION = 'crisis'
    ISSUANCE_ENFORCEMENT = 'issuance'
    SERVICE_CHOICES = [
        (CRISIS_INTERVENTION, 'Crisis Intervention Including Rescue'),
        (ISSUANCE_ENFORCEMENT, 'Issuance / Enforcement of Barangay Protection Order'),
    ]
    service_information = models.CharField(max_length=20, choices=SERVICE_CHOICES, null=True, blank=True)
    
    def __str__(self):
        return f"Case ID: {self.id}, Case Number: {self.case_number}"
    
class Evidence(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='evidence')
    file = models.FileField()

class Victim(models.Model):
    case_victim = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='victim',null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    suffix = models.CharField(max_length=10, null=True, blank=True)
    MALE, FEMALE = 'Male', 'Female'
    SEX_CHOICES = [(MALE, 'Male'), (FEMALE, 'Female')]
    sex = models.CharField(
        max_length=6,
        choices=SEX_CHOICES,
        null=True,
        blank=True)
    age = models.IntegerField(null=True, blank=True)
    CIVIL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('live-in', 'Live-In'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
    ]
    civil_status = models.CharField(
        max_length=10,
        choices=CIVIL_STATUS_CHOICES,
        null=True,
        blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    contact_number = models.IntegerField(default=0,null=True, blank=True)
    telephone_number = models.IntegerField(default=0,null=True, blank=True)
    house_information = models.CharField(max_length=250, null=True, blank=True)
    street = models.CharField(max_length=150, null=True, blank=True)
    barangay = models.CharField(max_length=150, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=250, null=True, blank=True)

class Perpetrator(models.Model):
    case_perpetrator = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='perpetrator',null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    suffix = models.CharField(max_length=10, null=True, blank=True)
    alias = models.CharField(max_length=100, null=True, blank=True)
    MALE, FEMALE = 'Male', 'Female'
    SEX_CHOICES = [(MALE, 'Male'), (FEMALE, 'Female')]
    sex = models.CharField(
        max_length=6,
        choices=SEX_CHOICES,
        null=True,
        blank=True)
    age = models.IntegerField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    identifying_marks = models.CharField(max_length=250, null=True, blank=True)
    house_information = models.CharField(max_length=250, null=True, blank=True)
    street = models.CharField(max_length=150, null=True, blank=True)
    barangay = models.CharField(max_length=150, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=250, null=True, blank=True)
    RELATIONSHIP_CHOICES = [
        ('currentSpouse', 'Current spouse / partner'),
        ('formerSpouse', 'Former spouse / partner'),
        ('currentFiance', 'Current fiance / dating relationship'),
        ('formerFiance', 'Former fiance / dating relationship'),
        ('employer', 'Employer / manager / supervisor'),
        ('agentOfEmployer', 'Agent of Employer'),
        ('teacher', 'Teacher / instructor / professor'),
        ('coach', 'Coach / trainer'),
        ('immediateFamily', 'Immediate family'),
        ('otherRelatives', 'Other relatives'),
        ('peopleOfAuthority', 'People of authority / service provider'),
        ('neighbors', 'Neighbors / peers / coworkers / classmates'),
        ('stranger', 'Stranger'),
    ]
    relationship_to_victim = models.CharField(
        max_length=30,
        choices=RELATIONSHIP_CHOICES,
        null=True,
        blank=True)

