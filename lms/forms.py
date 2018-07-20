from __future__ import unicode_literals
from lms.models import *
from django.forms import ModelForm
from django import forms
import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
#from .users import UserModel, UsernameField
from registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from lms.validators import *
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .validators import validate_email, existing_email_validator, invalid_email
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingField
import os


class Course_ModuleForm(forms.ModelForm):
    class Meta:
        model = Course_Module
        exclude = ('part_of',)
    def clean_video(self):
        ALLOWED_EXTENSIONS = ['.mp4', '.avi', '.wmv', '.flv']
        video = self.cleaned_data.get('video', False)
        if video:
            ext = os.path.splitext(video.name)[1]

            if (str(ext) in ALLOWED_EXTENSIONS):
                pass
            else:
                raise ValidationError("Please select a Video of type mp4, avi, wmv or flv.")

    def clean_Presentation(self):
        ALLOWED_EXTENSIONS = ['.doc', '.docs', '.pdf', '.ppt', '.pptx', '.rtf', '.txt', '.odt']
        Presentation = self.cleaned_data.get('Presentation', False)
        if Presentation:
            ext = os.path.splitext(Presentation.name)[1]

            if (str(ext) in ALLOWED_EXTENSIONS):
                pass
            else:
                raise ValidationError("Please select a file of type doc, docs, pdf, ppt, pptx, rtf, txt or odt.")

    def clean_Assignment(self):
        ALLOWED_EXTENSIONS = ['.doc', '.docs', '.pdf', '.ppt', '.pptx', '.rtf', '.txt', '.odt']
        Assignment = self.cleaned_data.get('Assignment', False)
        if Assignment:
            ext = os.path.splitext(Assignment.name)[1]

            if (str(ext) in ALLOWED_EXTENSIONS):
                pass
            else:
                raise ValidationError("Please select a file of type doc, docs, pdf, ppt, pptx, rtf, txt or odt,")
# Course_ModuleFormSet = forms.inlineformset_factory(Course_Module, form=Course_ModuleForm, extra=1)
Course_ModuleFormSet = forms.modelformset_factory(Course_Module, form=Course_ModuleForm, extra=1, can_order=True, can_delete=True)

class AddCourseForm(forms.Form):
    thumbnail = forms.ImageField(required=False)    
    course_name = forms.CharField(max_length=200)
    description = forms.CharField(required=True, widget=forms.Textarea)
    objectives = forms.CharField(required=True, widget=forms.Textarea)
    prerequisite = forms.CharField(required=True, widget=forms.Textarea)
    requirements = forms.CharField(required=True, widget=forms.Textarea)  




class trainerform(ModelForm):
    class Meta:
        model = add_instructor
        fields=['f_name', 'l_name', 'mobile', 'email','country','state','city', 'course_name', 'linkedin_profile', 'about_course', 'about_yourself','upload_profile']
		
class job_seeker_form(ModelForm):
    class Meta:
        model = job_seeker
        fields=['name', 'mobile', 'email','country','state','city', 'qualification','skills', 'career_interest', 'about_yourself', 'upload_resume']

class learner_enquiry_form(ModelForm):
    class Meta:
        model = learner_enquiry
        fields=['name', 'mobile', 'email','country','state','city', 'qualification','course_interest', 'message']
		
class vendor_enquiry_form(ModelForm):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'DD/MM/YYYY'}), input_formats=('%d/%m/%Y','%d-%m-%Y'))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'DD/MM/YYYY'}), input_formats=('%d/%m/%Y','%d-%m-%Y'))
    class Meta:
        model = vendor_enquiry
        fields=['name', 'mobile', 'email', 'company','country','state','city', 'requirement','document', 'from_date', 'to_date']

class client_enquiry_form(ModelForm):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'DD/MM/YYYY'}), input_formats=('%d/%m/%Y','%d-%m-%Y'))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'DD/MM/YYYY'}), input_formats=('%d/%m/%Y','%d-%m-%Y'))
    class Meta:
        model = client_enquiry
        fields=['name', 'mobile', 'email', 'company','country','state','city', 'requirement','document', 'from_date', 'to_date']

class searchform(forms.Form):
    s = forms.CharField(max_length=200)


#class loginform(ModelForm):
#    class Meta:
#        model = login
#        fields = ['username' , 'password']


class Custom_registeration_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]
		
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address....."))
            messages.info(request, "This email address is already in use.")
        return self.cleaned_data['email']
		
class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.

    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]
		
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address....."))
        return self.cleaned_data['email']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password',]

class userprofileForm(ModelForm):
    class Meta:
        model = userprofile
        fields = ['mobile', 'linkedin_id', 'picture','city', 'des'] 
		
#class UserProfileForm(ModelForm):
#    class Meta:
#		model = UserProfile
#		fields = ['mobile', 'linkedin_id',]	


class login_form(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'id': 'custom_login_username'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'id': 'custom_login_password'}))


class CommonRegistrationForm(forms.Form):
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)
    mobile = PhoneNumberField(widget=PhoneNumberPrefixWidget(), required=True)
    email = forms.EmailField(required=True, validators=[validate_email, existing_email_validator])  
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    REGISTRATION_CHOICES = (
        ('Learner', 'Learner'),
        ('Trainer', 'Trainer'),
        ('Vendor', 'Vendor'),
        ('Client', 'Client'),
        ('Job Seeker', 'Job Seeker'),
    )
    register_as = forms.ChoiceField(choices=REGISTRATION_CHOICES, widget=forms.RadioSelect(), required=True, label='Register As')


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label="Email", validators=[invalid_email])  
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "publish"
        ]

class CreateBlogForm(forms.Form):
    title = forms.CharField(max_length=120)
    image = forms.ImageField(required=True)
    content = forms.CharField(widget=CKEditorUploadingWidget())
    draft = forms.BooleanField(required=False)
    class Meta:
        widgets = {
            'content' : CKEditorUploadingWidget(),
        }