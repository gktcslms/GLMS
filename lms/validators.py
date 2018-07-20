from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.models import User

def validate_email(value):
    email_validator = EmailValidator()
    try:
        email_validator(value)
    except:
        raise ValidationError("Invalid Email form Form.")

def existing_email_validator(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError("This email address is already registered.")
        
def invalid_email(value):
    if User.objects.filter(email=value).exists() == False:
        raise ValidationError("Email Does not exist.")