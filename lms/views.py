from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth.models import Group
from django.core import signing
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib import messages
import logging
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from templated_mail.mail import BaseEmailMessage
from notifications.models import Notification
from notifications.signals import notify
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
import json

#from django.core.context_processors import csrf
from registration.forms import RegistrationForm
from django.forms import ModelForm
from registration.forms import RegistrationFormUniqueEmail

# Create your views here.(New GLMS)
def detail(request):
    return HttpResponse("You're looking at question")

def home(request):
    return render(request, "home.html")

def helpview(request):
    return render(request, "help.html")

def learner_helpview(request):
    return render(request, "learner_help.html")

def trainer_helpview(request):
    return render(request, "trainer_help.html")

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def tempview(request, course_id=None):
    learner = False
    learner_id = -1
    allow_access = False
    if request.user.is_authenticated:
        print("Authenticated")
        try:
            custom_user = Custom_User.objects.get(user = request.user)
            if str(custom_user.primary_registration_type) == "Learner":
                learner = True
                print("A Learner")
        except:
            pass
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all().order_by('order')
    if learner == True:
        try:
            student = Learner_Model.objects.get(user=custom_user)
            learner_id = student.id
            print("Student")
        except Exception as e:
            student = None
            print("Not a student.")
        if student != None:
            if course in student.courses_subscribed.all():
                allow_access = True
                print("Subscriber")
            else:
                print("Not a Subscriber")
                allow_access = False
        else:
            allow_access = False
    else:
        print("Not a Learner")
        allow_access = False   
    context = {"course": course, "allow_access": allow_access, "modules": modules, "learner_id": learner_id}
    return render(request, "temp.html", context)	

def privacyview(request):
    return render(request, 'privacy.html', locals())	

def termsview(request):
    return render(request, 'terms.html', locals())

def pythonview(request):
    return render(request, 'python.html', locals())
	
def surendra_profileview(request):
    return render(request,"surendra_profile2.html")

def send_surendra_profile_doc(request):
    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/shashi/SRC/static/surendra_profile.docx" # Select your file here.
    download_name ="surendra_profile.docx"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response

def contactview(request):
    return render(request, 'contactus.html', locals())

def courseview(request):
    course = Course.objects.all()
    return render(request, 'course.html', locals())

def custom_user_creation(request):
    current_site = str(get_current_site(request))
    form = CommonRegistrationForm(request.POST or None)
    #context = {"form": form}
    if form.is_valid():
        instance = form
        first_name = instance.cleaned_data.get("first_name")
        last_name = instance.cleaned_data.get("last_name")
        mobile = instance.cleaned_data.get("mobile")
        email = instance.cleaned_data.get("email")
        password = instance.cleaned_data.get("password")
        register_as = instance.cleaned_data.get("register_as")
        u, created = User.objects.get_or_create(email=email)
        if created == False:
            if u.is_active:
                return HttpResponseRedirect('/already_registered')
            else:
                return HttpResponseRedirect('/activation_pending')
        else:
            # Save User Model
            u.is_active = False
            u.is_staff = False
            u.is_superuser = False
            u.first_name = first_name
            u.last_name = last_name
            u.set_password(password)
            u.username = email
            u.save()
            # Save the Custom User Model
            custom_user = Custom_User.objects.create(user=u, mobile=mobile, primary_registration_type=register_as)
            custom_user.save()
            group = Group.objects.get(name=register_as)		
            u.groups.add(group)	
            if str(custom_user.primary_registration_type) == "Trainer":
                new_trainer = Trainer_Model.objects.create(user=custom_user)
                new_trainer.save()
            elif str(custom_user.primary_registration_type) == "Learner":
                new_trainer = Learner_Model.objects.create(user=custom_user)
                new_trainer.save()				
            # Encrypt Activation Link
            salt = settings.SECRET_KEY
            ak = signing.dumps(u.email, salt)
            # Send Activation Link to the newly registered user
            #send_mail('Activate yor Account for GKTCS LMS', 
            #"Welcome %s %s! Click the link below to activate yor Account "%(u.first_name,u.last_name) + " http://" + current_site +'/authentication/activate_user/?ak=' + ak, 
            #settings.EMAIL_HOST_USER,
            #[u.email], 
            #fail_silently=True)
            name = first_name+ " " +last_name
            user = User.objects.get(email=email)
            qs = User.objects.filter(email__in=['surendra.panpaliya@gmail.com', 'sanket.lolge@gmail.com'])
            notify.send(user, recipient=qs, verb='New Registeration! Name: '+ name + ' (Registered as a '+register_as+').')
            subject = 'New registration details'
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email,"sanket.lolge@gmail.com","surendra@gktcs.com"]
            activation_link = "https://" + current_site +'/authentication/activate_user/?ak=' + ak
            contact_message = " Name: %s, Mobile: %s, Email ID: %s, Registered As: %s, "%(name,mobile,email,register_as) + " Activation Link: http://" + current_site +'/authentication/activate_user/?ak=' + ak
            #send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
            context = {'activation_link': activation_link,'name':name,'mobile':mobile,'email':email,'register_as':register_as }
            BaseEmailMessage(context = context, template_name='email/activation.html').send(to=['sanket.lolge@gmail.com',"surendra@gktcs.com",email,from_email])
            #messages = [(subject, message, from_email, [recipient]) for recipient in recipient_list]
            return HttpResponseRedirect('/accounts/register/complete/')
        #c = {"form": form}
    return render(request, "user_creation.html", {"form": form})

def activate_user(request):
    salt = settings.SECRET_KEY
    ak = request.GET.get('ak')
    # Change below line max_age according to your settings.py file
    decrypt = signing.loads(ak, salt)
    u = User.objects.get(email=decrypt)
    try:
        if u.is_active == False:
            u.is_active = True
            u.save()
            return HttpResponseRedirect('/accounts/activate/complete/')
            # return render(request, "activation_successful.html", {})
        else:
            messages.info(request, "Your account is already activate. Login to continue.")
            return HttpResponseRedirect("/authentication/login/")
    except:
        return HttpResponseRedirect('/accounts/activate/failed/')



def my_login(request):
    try:
        next = request.GET.get('next')
    except Exception as e:
        print (e)
    form = LoginForm(request.POST or None)
    context ={"form":form}
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        try:
            user = User.objects.get(email=email)
            username = user.username
        except:
            return HttpResponseRedirect('/authentication/register/')
        try:
            #user = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
        except:
            return HttpResponseRedirect("/")
        if user is not None:
        #if user:
            if user.is_active:
                try:
                    user = authenticate(username=username, password=password)
                except:
                    messages.info(request, 'Invalid passowrd...')
                    return HttpResponseRedirect("/authentication/login/")
                login(request, user)
                try:
                    custom_user = Custom_User.objects.get(user = user)
                except:
                    return HttpResponseRedirect("/")
                qs = User.objects.filter(email__in=['surendra.panpaliya@gmail.com', 'sanket.lolge@gmail.com'])
                first_name = request.user.first_name
                last_name = request.user.last_name
                name = first_name+ " " +last_name
                if custom_user is not None:
                    if str(custom_user.primary_registration_type) == "Trainer":
                        if next:
                            notify.send(user, recipient=qs, verb=name +' (Trainer) Login.')
                            return HttpResponseRedirect(next) 
                        notify.send(user, recipient=qs, verb=name +' (Trainer) Login.')					
                        return HttpResponseRedirect("/trainer_dashboard/")
                    if str(custom_user.primary_registration_type) == "Learner":
                        if next:
                            notify.send(user, recipient=qs, verb=name +' (Learner) Login.')
                            return HttpResponseRedirect(next) 
                        notify.send(user, recipient=qs, verb=name +' (Lrainer) Login.')
                        return HttpResponseRedirect("/learner_dashboard/")
                    if str(custom_user.primary_registration_type) == "Vendor":
                        if next:
                            notify.send(user, recipient=qs, verb=name +' (Vendor) Login.')
                            return HttpResponseRedirect(next)
                        notify.send(user, recipient=qs, verb=name +' (Vendor) Login.')
                        return HttpResponseRedirect("/vendor_dashboard/")
                    if str(custom_user.primary_registration_type) == "Job Seeker":
                        if next:
                            notify.send(user, recipient=qs, verb=name +' (Job Seeker) Login.')
                            return HttpResponseRedirect(next) 
                        notify.send(user, recipient=qs, verb=name +' (Job Seeker) Login.')
                        return HttpResponseRedirect("/job_seeker_dashboard/")
                    if str(custom_user.primary_registration_type) == "Client":
                        if next:
                            notify.send(user, recipient=qs, verb=name +' (Client) Login.')
                            return HttpResponseRedirect(next) 
                        notify.send(user, recipient=qs, verb=name +' (Client) Login.')
                        return HttpResponseRedirect("/client_dashboard/")
            else:
                messages.info(request, "Your account activation pending. Please check your email account for activation link")
                return HttpResponseRedirect("/authentication/login/")
            return HttpResponseRedirect("/")
        else:
            messages.info(request, 'Invalid account...')
            context ={"form":form}      
    return render(request, "my_login.html", context)

                  

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def baseview(request):
    return render(request, "base.html")

@login_required(login_url='/authentication/login/')
@permission_required('lms.add_hadoop')
def basic_registraion_details_view(request):
	context = Custom_User.objects.all()
	return render(request, 'basic_registraion_details.html', {"context": context})

def send_python_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/python_content.pdf" # Select your file here.
    download_name ="python_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_jython_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/jython_content.pdf" # Select your file here.
    download_name ="jython_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_python_data_science_content(request):
    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/python_data_science.pdf" # Select your file here.
    download_name ="python_data_science.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response

def send_python_machine_learning_content(request):
    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/python_machine_learning.pdf" # Select your file here.
    download_name ="python_machine_learning.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_python_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/python_content.pdf" # Select your file here.
    download_name ="python_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_django_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/django_content.pdf" # Select your file here.
    download_name ="django_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_pyspark_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/pyspark_content.pdf" # Select your file here.
    download_name ="pyspark_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_ror_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/ror_content.pdf" # Select your file here.
    download_name ="Ruby_on_Rails_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_hadoop_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/hadoop_content.pdf" # Select your file here.
    download_name ="Data_science_hadoop_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_appium_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/appium_content.pdf" # Select your file here.
    download_name ="appium_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_r_programming_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/r_programming_content.pdf" # Select your file here.
    download_name ="r_programming_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_ansible_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/ansible_content.pdf" # Select your file here.
    download_name ="ansible_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_mongodb_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/mongodb_content.pdf" # Select your file here.
    download_name ="mongodb_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_ruby_devops_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/ruby_devops_content.pdf" # Select your file here.
    download_name ="ruby_devops_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_sparkscala_content(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/pdf/sparkscala_content.pdf" # Select your file here.
    download_name ="sparkscala_content.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_python_file(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/Python.pdf" # Select your file here.
    download_name ="Python.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
	
def send_hadoop_file(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/Hadoop.pdf" # Select your file here.
    download_name ="BigData&Hadoop.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response	
	
def send_ruby_file(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/ruby.pdf" # Select your file here.
    download_name ="Ruby On Rails.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response	

def send_angularjs_file(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/angularjs.pdf" # Select your file here.
    download_name ="AngularJS.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response	
def send_android_file(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/android.pdf" # Select your file here.
    download_name ="Android.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response	

def send_data_science_file(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/data_science.pdf" # Select your file here.
    download_name ="Data Science.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response	
	
def send_r_prog_file(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/r_prog.pdf" # Select your file here.
    download_name ="R Programming.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response		
	
def send_appium_file(request):

    import os, tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes

    filename = "/home/gktcs/public_html/GLMS/public/static/appium.pdf" # Select your file here.
    download_name ="Appium.pdf"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response			

@login_required(login_url='/authentication/login/')
def myprofileview(request, user_id, template_name='myprofile.html'):
    u = userprofile.objects.all()
    try:
        if request.user.is_superuser:
            up = get_object_or_404(userprofile, user_id=user_id)
        else:
            up = get_object_or_404(userprofile, user_id=user_id, user=request.user)   
    except:
        up = userprofile(user=request.user)    
    form = userprofileForm(request.POST or None, instance=up)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.picture = request.FILES.get('picture', save_it.picture)
        save_it.save()
    return render(request, template_name, {'form':form})

@login_required(login_url='/authentication/login/')
def learner_profileview(request, user_id, template_name='learner_profile.html'):
    u = userprofile.objects.all()
    try:
        if request.user.is_superuser:
            up = get_object_or_404(userprofile, user_id=user_id)
        else:
            up = get_object_or_404(userprofile, user_id=user_id, user=request.user)   
    except:
        up = userprofile(user=request.user)    
    form = userprofileForm(request.POST or None, instance=up)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.picture = request.FILES.get('picture', save_it.picture)
        save_it.save()
    return render(request, template_name, {'form':form})

def search_titles(request):
    if request.method == "POST" and request.POST:
        search_text = request.POST['search_text']
    else:
        search_text = ''
    course = Course.objects.filter(course_name__contains=search_text.title())
    #course = Course.objects.filter(course_name__contains='Pyt')
    return render(request, "ajax_search.html", {"course": course})
	
def search_course(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''
    course = Course.objects.filter(course_name__contains=search_text.title())
    return render(request, "ajax_search.html", {"course": course})

@login_required(login_url='/authentication/login/')
def instructor_addview(request):
	form = trainerform(request.POST or None, request.FILES)
	form.fields['linkedin_profile'].required = False
	linkedin_profile = " "
	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()
		f_name = form.cleaned_data.get("f_name")
		l_name = form.cleaned_data.get("l_name")
		mob = form.cleaned_data.get("mobile")
		mobile = str(mob)
		email = form.cleaned_data.get("email")
		course_name = form.cleaned_data.get("course_name")
		linkedin_profile = form.cleaned_data.get("linkedin_profile")
		about_course = form.cleaned_data.get("about_course")
		about_yourself = form.cleaned_data.get("about_yourself")
		name = f_name+ " " +l_name
		subject = 'Trainer Enquiry Details'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"sanket.lolge@gmail.com","surendra@gktcs.com"]
		contact_message = " Name: %s Mobile: %s Email ID: %s, Course Name: %s, Linkedin ID: %s, About course: %s, About Trainer:%s"%(name,mobile,email,course_name,linkedin_profile,about_course,about_yourself)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, "Thank You. We will get back to you shortly")
		return HttpResponseRedirect("/")
	else:
		form = trainerform(request.POST or None, request.FILES)
	return render(request, 'instructor_add.html', locals())

@login_required(login_url='/authentication/login/')
def vendor_enquiry_form_view(request):
	form = vendor_enquiry_form(request.POST or None, request.FILES)
	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()
		name = form.cleaned_data.get("name")
		mob = form.cleaned_data.get("mobile")
		mobile = str(mob)
		email = form.cleaned_data.get("email")
		company = form.cleaned_data.get("company")
		requirement = form.cleaned_data.get("requirement")
		from_date = form.cleaned_data.get("from_date")
		to_date = form.cleaned_data.get("to_date")
		subject = 'Vendor Enquiry Details'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"sanket.lolge@gmail.com","surendra@gktcs.com"]
		contact_message = " Name: %s Mobile: %s Email ID: %s, Company: %s, Requirement: %s, From Date: %s, To Date:%s"%(name,mobile,email,company,requirement,from_date,to_date)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, "Thank You. We will get back to you shortly")
		return HttpResponseRedirect("/")
	else:
		form = vendor_enquiry_form(request.POST or None)
	return render(request, 'vendor_enquiry_form.html',locals())
	
@login_required	(login_url='/authentication/login/')
def client_enquiry_form_view(request):
	form = client_enquiry_form(request.POST or None, request.FILES)
	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()
		name = form.cleaned_data.get("name")
		mob = form.cleaned_data.get("mobile")
		mobile = str(mob)
		email = form.cleaned_data.get("email")
		company = form.cleaned_data.get("company")
		requirement = form.cleaned_data.get("requirement")
		from_date = form.cleaned_data.get("from_date")
		to_date = form.cleaned_data.get("to_date")
		subject = 'Client Enquiry Details'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"sanket.lolge@gmail.com"]
		contact_message = " Name: %s Mobile: %s Email ID: %s, Company: %s, Requirement: %s, From Date: %s, To Date:%s"%(name,mobile,email,company,requirement,from_date,to_date)
		context = {"contact_message":contact_message}
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		#ids = ['sanket.lolge@gmail.com','sanketlolge2@gmail.com']
		#for id in ids:
		#	BaseEmailMessage(template_name='email/activation.html').send(to=[id])
		#messages = [(subject, message, from_email, [recipient]) for recipient in recipient_list]
		messages.success(request, "Thank You. We will get back to you shortly")
		return HttpResponseRedirect("/")
	else:
		form = client_enquiry_form(request.POST or None)
	return render(request, 'client_enquiry_form.html',locals())
	
@login_required(login_url='/authentication/login/')
def learner_enquiry_form_view(request):
	form = learner_enquiry_form(request.POST or None, request.FILES)
	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()
		name = form.cleaned_data.get("name")
		mob = form.cleaned_data.get("mobile")
		mobile = str(mob)
		email = form.cleaned_data.get("email")
		city = form.cleaned_data.get("city")
		qualification = form.cleaned_data.get("qualification")
		course_interest = form.cleaned_data.get("course_interest")
		message = form.cleaned_data.get("message")
		subject = 'Learner Enquiry Details'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"sanket.lolge@gmail.com","surendra@gktcs.com"]
		contact_message = " Name: %s Mobile: %s Email ID: %s, City: %s, Qualification: %s, Course Interest: %s, Message:%s"%(name,mobile,email,city,qualification,course_interest,message)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, "Thank You. We will get back to you shortly")
		return HttpResponseRedirect("/")
	else:
		form = learner_enquiry_form(request.POST or None)
	return render(request, 'learner_enquiry_form.html',locals())

@login_required(login_url='/authentication/login/')
def support_form_view(request):
	form = support_form(request.POST or None, request.FILES)
	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()
		name = form.cleaned_data.get("name")
		mob = form.cleaned_data.get("mobile")
		mobile = str(mob)
		email = form.cleaned_data.get("email")
		sub = form.cleaned_data.get("subject")
		message = form.cleaned_data.get("message")
		subject = 'Support Enquiry Details'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"sanket.lolge@gmail.com","surendra@gktcs.com"]
		contact_message = " Name: %s Mobile: %s Email ID: %s, Subject: %s, Message:%s"%(name,mobile,email,sub,message)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, "Thank You. We will get back to you shortly")
		return HttpResponseRedirect("/")
	else:
		form = support_form(request.POST or None)
	return render(request, 'support_form.html',locals())

@login_required(login_url='/authentication/login/')
def job_seeker_form_view(request):
	form = job_seeker_form(request.POST or None, request.FILES)
	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()
		name = form.cleaned_data.get("name")
		mob = form.cleaned_data.get("mobile")
		mobile = str(mob)
		email = form.cleaned_data.get("email")
		city = form.cleaned_data.get("city")
		qualification = form.cleaned_data.get("qualification")
		skills = form.cleaned_data.get("skills")
		career_interest = form.cleaned_data.get("career_interest")
		about_yourself = form.cleaned_data.get("about_yourself")
		subject = 'Job Seeker Enquiry Details'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"sanket.lolge@gmail.com","surendra@gktcs.com"]
		contact_message = " Name: %s Mobile: %s Email ID: %s, City: %s, Qualification: %s, Skills: %s, Career Interest:%s, About Self:%s"%(name,mobile,email,city,qualification,skills,career_interest,about_yourself)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, "Thank You. We will get back to you shortly")
		return HttpResponseRedirect("/")
	else:
		form = job_seeker_form(request.POST or None)
	return render(request, 'job_seeker_form.html',locals())

@login_required(login_url='/authentication/login/')
def learner_profileview(request, user_id, template_name='learner_profile.html'):
    u = userprofile.objects.all()
    try:
        if request.user.is_superuser:
            up = get_object_or_404(userprofile, user_id=user_id)
        else:
            up = get_object_or_404(userprofile, user_id=user_id, user=request.user)   
    except:
        up = userprofile(user=request.user)    
    form = userprofileForm(request.POST or None, instance=up)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.picture = request.FILES.get('picture', save_it.picture)
        save_it.save()
    return render(request, template_name, {'form':form})

def invalid_trainer_view(request):
    return render(request, 'invalid_trainer.html',locals())
	
@login_required(login_url='/authentication/login/')
@permission_required('lms.view_vendor_enquiry')	
def vendor_enquiry_view(request):
    v = vendor_enquiry.objects.all()
    return render(request, 'vendor_enquiry.html',locals())

@login_required(login_url='/authentication/login/')
@permission_required('lms.view_general_enquiry')	
def general_enquiry_view(request):
    v = Enquiry.objects.all()
    return render(request, 'general_enquiry.html',locals())

@login_required(login_url='/authentication/login/')
@permission_required('lms.view_vendor_enquiry')	
def job_seeker_enquiry_view(request):
    v = job_seeker.objects.all()
    return render(request, 'job_seeker_enquiry.html',locals())

@login_required(login_url='/authentication/login/')
def notifications_view(request):
    notifications = Notification.objects.all()
    return render(request, 'notifications.html',locals())
	
@login_required(login_url='/authentication/login/')
@permission_required('lms.view_learner_enquiry')	
def learner_enquiry_view(request):
    v = learner_enquiry.objects.all()
    return render(request, 'learner_enquiry.html',locals())

@login_required(login_url='/authentication/login/')
@permission_required('lms.view_support')	
def support_view(request):
    v = support.objects.all()
    return render(request, 'support.html',locals())
	
@login_required(login_url='/authentication/login/')
@permission_required('lms.view_learner_enquiry')	
def client_enquiry_view(request):
    v = client_enquiry.objects.all()
    return render(request, 'client_enquiry.html',locals())

@login_required(login_url='/authentication/login/')
def pythoncorpview(request):
	#form = QuestionForm(request.POST or None)
	if request.method == "POST":
		#a = []
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mobile = ''
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'Python Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		#contact_message = " Client Details--> Name: %s , Email Id: %s , Contact Number: %s , City: %s -->Selected Modules: %s"%(name,email,mobile,city,m)
		contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "PythonCorporate.html")

@login_required(login_url='/authentication/login/')
def jython2_corporate_view(request):
	#form = QuestionForm(request.POST or None)
	if request.method == "POST":
		#a = []
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mob = request.user.userprofile.mobile
		mobile = str(mob)
		city = request.user.userprofile.city
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		#name = request.POST.get("Name")
		#email = request.POST.get("Email")
		#remark = request.POST.get("Remark")
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'Jython Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		#contact_message = " Name: %s , Email Id: %s , Remark: %s ,--> Selected Modules: %s"%(name,email,remark,b)
		contact_message = " Client Details--> Name: %s , Email Id: %s , Contact Number: %s , City: %s -->Selected Modules: %s"%(name,email,mobile,city,m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "jython_corporate.html")

@login_required(login_url='/authentication/login/')
def jython_corporate_view(request):
	if request.method == "POST":
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mobile = ''
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'Jython Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "jython_corporate.html")

@login_required(login_url='/authentication/login/')
def django_corporate_view(request):
	if request.method == "POST":
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mobile = ''
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'Django Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "django_corporate.html")

@login_required(login_url='/authentication/login/')
def pyspark_corporate_view(request):
	if request.method == "POST":
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mobile = ''
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'Pyspark Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "pyspark_corporate.html")
@login_required(login_url='/authentication/login/')
def ruby_on_rails_corporate_view(request):
	if request.method == "POST":
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mobile = ''
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'Ruby on Rails Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "ruby_on_rails_corporate.html")
	
@login_required(login_url='/authentication/login/')
def hadoop_corporate_view(request):
	if request.method == "POST":
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mobile = ''
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'Hadoop Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "hadoop_corporate.html")

@login_required(login_url='/authentication/login/')
def appium_corporate_view(request):
	if request.method == "POST":
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mobile = ''
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'Appium Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "appium_corporate.html")
	
@login_required(login_url='/authentication/login/')
def r_programming_corporate_view(request):
	if request.method == "POST":
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mobile = ''
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'R Programming Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "r_programming_corporate.html")

@login_required(login_url='/authentication/login/')
def ansible_corporate_view(request):
	if request.method == "POST":
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mobile = ''
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'Ansible Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "ansible_corporate.html")

@login_required(login_url='/authentication/login/')
def mongodb_corporate_view(request):
	if request.method == "POST":
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mobile = ''
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'MongoDB Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "mongodb_corporate.html")

@login_required(login_url='/authentication/login/')
def devops_corporate_view(request):
	if request.method == "POST":
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mobile = ''
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'DevOps Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "devops_corporate.html")

@login_required(login_url='/authentication/login/')
def sparkscala_corporate_view(request):
	if request.method == "POST":
		mob = 1
		city = "-"
		first_name = request.user.first_name
		last_name = request.user.last_name
		name = first_name+ " " +last_name
		email = str(request.user.email)
		mobile = ''
		c = request.POST.getlist('checks')
		m = u", ".join(c)
		new_selection = select_module(name = name, email = email, contact = mobile, city = city, modules = m)
		new_selection.save()
		subject = 'Spark with Scala Modules'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
		contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
		send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
		messages.success(request, 'Thank you, we will get back to you shortly')
		return HttpResponseRedirect("/")
	return render(request, "sparkscala_corporate.html")

@login_required(login_url='/authentication/login/')
@permission_required('lms.view_module_enquiry')	
def module_enquiryview(request):
	modules = select_module.objects.all()
	return render(request, 'module_enquiry.html',locals())

@login_required(login_url='/authentication/login/')
@permission_required('lms.view_trainer_enquiry')	
def trainer_enquiryview(request):
	modules = add_instructor.objects.all()
	return render(request, 'trainer_enquiry.html',locals())

@login_required(login_url='/authentication/login/')
def trainer_dashboard_view(request):
    user = request.user
    try:
        cu = Custom_User.objects.get(user=user)
    except Custom_User.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/")
    try:
        trainer = Trainer_Model.objects.get(user=cu)
    except Trainer_Model.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/")
    return render(request, 'trainer_dashboard.html',locals())

@login_required(login_url='/authentication/login/')	
def learner_dashboard_view(request):
    return render(request, 'learner_dashboard.html',locals())
	
@login_required(login_url='/authentication/login/')	
def vendor_dashboard_view(request):
    return render(request, 'vendor_dashboard.html',locals())
	
@login_required(login_url='/authentication/login/')	
def client_dashboard_view(request):
    return render(request, 'client_dashboard.html',locals())

@login_required(login_url='/authentication/login/')	
def base_dashboard_view(request):
    return render(request, 'base_dashboard.html',locals())
	
@login_required(login_url='/authentication/login/')	
def job_seeker_dashboard_view(request):
    return render(request, 'job_seeker_dashboard.html',locals())
def search_course_view(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
    c = q.title()
    course = Course.objects.filter(course_name__contains=c)
    return render(request, 'search_course.html', locals())

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def edit_course(request, *args, **kwargs):
    user = request.user
    try:
        cu = Custom_User.objects.get(user=user)
    except Custom_User.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/")
    try:
        trainer = Trainer_Model.objects.get(user=cu)
    except Trainer_Model.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/") 
    if cu.primary_registration_type == 'Trainer':    
        course = Course.objects.get(course_by=trainer, id=kwargs['course_id'])
        formset = Course_ModuleFormSet(queryset = course.modules.all())
        if request.method == 'POST':
            formset = Course_ModuleFormSet(request.POST, request.FILES or None, queryset = course.modules.all())
            if formset.is_valid():
                modules = formset.save(commit=False)

                for module in modules:
                    module.part_of = course
                    module.save()
                messages.success(request, "Course Updated.")
                #return HttpResponseRedirect('/edit_course/' + str(kwargs['course_id']))
                return HttpResponseRedirect("/display_courses/")
        context = {"formset":formset, 'course':course}
        return render(request, "inline.html", context)
    else:
        return HttpResponseRedirect('/invalid_trainer/')

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def edit_course_modules(request, course_id=None, *args, **kwargs):
    user = request.user
    cu = Custom_User.objects.get(user=user)
    trainer = Trainer_Model.objects.get(user=cu)
    if cu.primary_registration_type == 'Trainer':    
        course = Course.objects.get(course_by=trainer, id=course_id)
        queryset = course.modules.all()
        return render(request, "edit_modules.html", {"course": course, "queryset": queryset})
    else:
        return HttpResponseRedirect('/invalid_trainer/')

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def display_courses(request):
    user = request.user
    try:
        cu = Custom_User.objects.get(user=user)
    except Custom_User.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/")
    try:
        trainer = Trainer_Model.objects.get(user=cu)
    except Trainer_Model.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/") 
    if cu.primary_registration_type == 'Trainer' and trainer:    
        trainer_courses = Course.objects.all().filter(course_by=trainer)
        return render(request, "display_courses.html", {"trainer_courses":trainer_courses})
    else:
        return HttpResponseRedirect("/invalid_trainer")
		
@login_required(login_url='/authentication/login/', redirect_field_name='next')
def all_courses(request):
    courses = Course.objects.all()
    return render(request, "all_courses.html", {"courses":courses})


@login_required(login_url='/authentication/login/', redirect_field_name='next')
def learner_my_courses(request):
    if request.user.is_authenticated:
        print("Authenticated")
        try:
            custom_user = Custom_User.objects.get(user = request.user)
            if str(custom_user.primary_registration_type) == "Learner":
                learner = True
                print("A Learner")
        except:
            pass
    #course = get_object_or_404(Course, id=course_id)
    if learner == True:
        try:
            student = Learner_Model.objects.get(user=custom_user)
            print("Student")
        except Exception as e:
            student = None
            print("Not a student.")
        if student != None:
            subscribed_courses = student.courses_subscribed.all()
        else:
            allow_access = False
    else:
        print("Not a Learner")
        allow_access = False   
    context = {"courses": subscribed_courses}
    return render(request, "learner_my_courses.html", context)


@login_required(login_url='/authentication/login/', redirect_field_name='next')
def add_course(request):
    user = request.user
    try:
        cu = Custom_User.objects.get(user=user)
    except Custom_User.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/")
    try:
        trainer = Trainer_Model.objects.get(user=cu)
    except Trainer_Model.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/") 
    if cu.primary_registration_type == 'Trainer' and trainer:
        if request.method == 'POST':
            form = AddCourseForm(request.POST, request.FILES or None)
            context = {"form": form}
            if form.is_valid():
                instance = form
                thumbnail = instance.cleaned_data.get('thumbnail')
                if not thumbnail:
                    thumbnail = 'images/course_thumbnails/default_course.jpg'				
                course_name = instance.cleaned_data.get('course_name')
                description = instance.cleaned_data.get('description')
                objectives = instance.cleaned_data.get('objectives')
                prerequisite = instance.cleaned_data.get('prerequisite')
                requirements = instance.cleaned_data.get('requirements')
                course_by = trainer
                new_course = Course.objects.create(
                    course_by = course_by,
                    thumbnail = thumbnail,
                    course_name = course_name,
                    description = description,
                    objectives = objectives,
                    prerequisite = prerequisite,
                    requirements = requirements
                )
                first_name = request.user.first_name
                last_name = request.user.last_name
                name = first_name+ " " +last_name
                qs = User.objects.filter(email__in=['surendra.panpaliya@gmail.com', 'sanket.lolge@gmail.com'])
                notify.send(user, recipient=qs, verb='New course added: '+course_name + ' (Trainer: '+name+').')
                messages.success(request, "Course successfully added. Please click on ADD CONTENT to add course content." )
                return HttpResponseRedirect("/display_courses/")            
            else:
                messages.error(request, 'Invalid thumbnail image or form entries.')
                form = AddCourseForm(request.POST, request.FILES or None)
                context = {"form": form}
        else:
            form = AddCourseForm(request.POST, request.FILES or None)
            context = {"form": form}
    else:
        form = AddCourseForm(request.POST, request.FILES or None)
        return HttpResponseRedirect("/invalid_trainer/")
    return render(request, "add_course.html", context)

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def update_course_details(request, course_id=None):
    user = request.user
    custom_user = get_object_or_404(Custom_User, user=user)
    if custom_user.primary_registration_type == "Trainer":
        trainer = get_object_or_404(Trainer_Model, user=custom_user)
        course = get_object_or_404(Course, id=course_id)
        if course.course_by == trainer:
            if request.method == 'POST':
                form = AddCourseForm(request.POST, request.FILES or None)
                if form.is_valid():
                    instance = form
                    if (instance.cleaned_data.get('thumbnail') != None):
                        course.thumbnail = instance.cleaned_data.get('thumbnail')
                    elif (course.thumbnail != "" and course.thumbnail != False):
                        course.thumbnail = course.thumbnail
                    else:
                        course.thumbnail = 'images/course_thumbnails/default_course.jpg'

                    course.course_name = instance.cleaned_data.get('course_name')
                    course.description = instance.cleaned_data.get('description')
                    course.objectives = instance.cleaned_data.get('objectives')
                    course.prerequisite = instance.cleaned_data.get('prerequisite')
                    course.requirements = instance.cleaned_data.get('requirements')
                    course.course_by = trainer 
                    course.save()
                    messages.success(request, "Course Successfully Updated" )
                    return HttpResponseRedirect("/display_courses/")
                context = {"text": "edit", "form":form}
            else:
                form = AddCourseForm(initial=model_to_dict(course))
                context = {"text": "edit", "form":form}            
        else:
            context = {"text": "Not authorised to edit"}
    else:
        context = {"text": "You are not a trianer."}
    return render(request, "update_course_details.html", context)

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def preview_course(request, course_id=None):
    user = request.user
    try:
        custom_user = Custom_User.objects.get(user=user)
    except Custom_User.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/")
    try:
        trainer = Trainer_Model.objects.get(user=custom_user)
    except Trainer_Model.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/") 
    if custom_user.primary_registration_type == "Trainer":
        trainer = get_object_or_404(Trainer_Model, user=custom_user)
        course = get_object_or_404(Course, id=course_id)
        if course.course_by == trainer:
            modules = Course_Module.objects.all().filter(part_of=course).order_by('order')
        else:
            return HttpResponseRedirect("/invalid_trainer/")	
    else:
        return HttpResponseRedirect("/invalid_trainer/")
    return render(request, "preview_course.html", {"trainer":trainer,"course":course, "modules":modules})

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def learner_preview_course(request, course_id=None):
    learner = False
    learner_id = -1
    allow_access = False
    if request.user.is_authenticated:
        print("Authenticated")
        try:
            custom_user = Custom_User.objects.get(user = request.user)
            if str(custom_user.primary_registration_type) == "Learner":
                learner = True
                print("A Learner")
        except:
            pass
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all().order_by('order')
    if learner == True:
        try:
            student = Learner_Model.objects.get(user=custom_user)
            learner_id = student.id
            print("Student")
        except Exception as e:
            student = None
            print("Not a student.")
        if student != None:
            if course in student.courses_subscribed.all():
                allow_access = True
                print("Subscriber")
            else:
                print("Not a Subscriber")
                allow_access = False
        else:
            allow_access = False
    else:
        print("Not a Learner")
        allow_access = False   
    context = {"course": course, "allow_access": allow_access, "modules": modules, "learner_id": learner_id}
    return render(request, "learner_preview_course.html", context)
    # course = get_object_or_404(Course, id=course_id)
    # modules = Course_Module.objects.all().filter(part_of=course).order_by('order')
    # return render(request, "learner_preview_course.html", {"course":course, "modules":modules})

def delete_course(request, course_id=None):
    user = request.user
    try:
        custom_user = Custom_User.objects.get(user=user)
    except Custom_User.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/")
    try:
        trainer = Trainer_Model.objects.get(user=custom_user)
    except Trainer_Model.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/") 
    if custom_user.primary_registration_type == "Trainer":
        trainer = get_object_or_404(Trainer_Model, user=custom_user)
        course = get_object_or_404(Course, id=course_id)
        if course.course_by == trainer:
            course.delete()
            messages.success(request, "Successfully Deleted.")
        else:
            return HttpResponseRedirect("/invalid_trainer/")	
    else:
        return HttpResponseRedirect("/invalid_trainer/")
    return redirect("my_courses")

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def my_dashboard(request, course_id=None):
    user = request.user
    custom_user = get_object_or_404(Custom_User, user=user)
    if custom_user.primary_registration_type == "Trainer":
        return HttpResponseRedirect("/trainer_dashboard/")
    else:
        return HttpResponseRedirect("/learner_dashboard/")
	
@login_required(login_url='/authentication/login/', redirect_field_name='next')
def list_blogs(request):
    blog_list = Blog.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(blog_list, 2)  #Change the number of blogs you want to see per page here
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'blogs.html', { 'blogs': blogs })

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def all_blogs(request):
    blog_list = Blog.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(blog_list, 2)  #Change the number of blogs you want to see per page here
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'all_blogs.html', { 'blogs': blogs })
	
def view_blog(request, id=None):
    blog = get_object_or_404(Blog, id=id)
    context = {"blog":blog}
    return render(request, "view_blog.html", context)



@login_required(login_url='/authentication/login/', redirect_field_name='next')
def create_blog(request):
    user = request.user
    custom_user = get_object_or_404(Custom_User, user=user)
    if request.method == "POST":
        form = CreateBlogForm(request.POST, request.FILES or None)
        if form.is_valid():
            instance = form
            title = instance.cleaned_data.get('title')
            image = instance.cleaned_data.get('image')
            content = instance.cleaned_data.get('content')
            draft = instance.cleaned_data.get('draft')
            blogger = custom_user
            blog = Blog.objects.create(
                title = title,
                image = image,
                content = content,
                draft = draft,
                blogger = blogger
            )
            blog.save()
            return HttpResponseRedirect(blog.get_absolute_url())
        context = {"form":form}
    else:
        form = CreateBlogForm()
        context = {"form":form}
    return render(request, "create_blog.html", context)


@login_required(login_url='/authentication/login/', redirect_field_name='next')
def update_blog(request, id=None):
    user = request.user
    custom_user = get_object_or_404(Custom_User, user=user)
    blog = get_object_or_404(Blog, id=id)
    if blog.blogger != custom_user:
        return HttpResponseRedirect("not_your_blog")
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES or None)
        if form.is_valid():
            instance = form
            blog.title = instance.cleaned_data.get('title')
            if (blog.image == "" and instance.cleaned_data.get('image') == None):
                blog.image = blog.image
            elif (blog.image != "" and instance.cleaned_data.get('image') == None):
                blog.image = blog.image
            elif (blog.image != "" and instance.cleaned_data.get('image') != None):
                blog.image = instance.cleaned_data.get('image')
            elif (blog.image == "" and instance.cleaned_data.get('image') != None):
                blog.image = instance.cleaned_data.get('image')
            elif (blog.image == False):
                blog.image = ""
            else:
                blog.image = blog.image
            blog.content = instance.cleaned_data.get('content')
            blog.draft = instance.cleaned_data.get('draft')
            blog.save()
            messages.success(request, "Blog Successfully Updated.")
            return redirect("my_blogs")
        context = {"form":form}
    else:
        form = CreateBlogForm(initial=model_to_dict(blog))
        context = {"form":form}
    return render(request, "update_blog.html", context)


@login_required(login_url='/authentication/login/', redirect_field_name='next')
def delete_blog(request, id=None):
    user = request.user
    custom_user = get_object_or_404(Custom_User, user=user)
    blog = get_object_or_404(Blog, id=id)
    if blog.blogger != custom_user:
        return HttpResponseRedirect("not_your_blog")
    blog.delete()
    messages.success(request, "Successfully Deleted.")
    return redirect("my_blogs")
    

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def blog_like_toggle(request, id=None):
    obj = get_object_or_404(Blog, id=id)
    user = request.user
    if user.is_authenticated():
        custom_user = get_object_or_404(Custom_User, user=user)
        if custom_user.id: 
            if custom_user in obj.likes.all():
                obj.likes.remove(custom_user)
            else:
                obj.likes.add(custom_user)
    return HttpResponseRedirect(obj.get_absolute_url())



class BlogLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id=None, format=None):
        # id = self.kwargs.get("id")
        obj = get_object_or_404(Blog, id=id)
        user = self.request.user
        updated = False
        liked = False
        
        if user.is_authenticated():
            custom_user = get_object_or_404(Custom_User, user=user)
            if custom_user.id: 
                if custom_user in obj.likes.all():
                    obj.likes.remove(custom_user)
                    liked = False                    
                else:
                    obj.likes.add(custom_user)
                    liked = True
                updated = True
        data = {
            "updated": updated,
            "liked": liked
        }    
        return Response(data)
		
@login_required(login_url='/authentication/login/', redirect_field_name='next')
def my_blogs(request):
    user = request.user    
    custom_user = get_object_or_404(Custom_User, user=user)
    blog_list = Blog.objects.filter(blogger=custom_user)
    page = request.GET.get('page', 1)

    paginator = Paginator(blog_list, 2)  #Change the number of blogs you want to see per page here
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'my_blogs.html', { 'blogs': blogs })

def browse_courses(request):
    context = {}
    #return render(request, "browse_courses.html", context)
    return render(request, "home2.html", context)

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def browse_course_details(request, course_id=None):
    learner = False
    learner_id = -1
    allow_access = False
    if request.user.is_authenticated:
        print("Authenticated")
        try:
            custom_user = Custom_User.objects.get(user = request.user)
            if str(custom_user.primary_registration_type) == "Learner":
                learner = True
                print("A Learner")
        except:
            pass
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all().order_by('order')
    if learner == True:
        try:
            student = Learner_Model.objects.get(user=custom_user)
            learner_id = student.id
            print("Student")
        except Exception as e:
            student = None
            print("Not a student.")
        if student != None:
            if course in student.courses_subscribed.all():
                allow_access = True
                print("Subscriber")
            else:
                print("Not a Subscriber")
                allow_access = False
        else:
            allow_access = False
    else:
        print("Not a Learner")
        allow_access = False   
    context = {"course": course, "allow_access": allow_access, "modules": modules, "learner_id": learner_id}
    return render(request, "browse_course_details.html", context)

def update_cart_session(request):
    if request.method == 'POST':
        cart = json.loads(request.body)
        request.session['cart'] = cart["cart"]
        print(request.session['cart'])
        print("Added to cart successfully")
        return HttpResponse('OK')
    else:
        print("POST request not completed.")
        return HttpResponse("Not a POST Method")


@login_required(login_url='/authentication/login/', redirect_field_name='next')
def checkout(request):
    #if request.user.is_authenticated:
        #print("Authenticated")
    try:
        custom_user = Custom_User.objects.get(user = request.user)
        if str(custom_user.primary_registration_type) == "Learner":
            print("Learner")
            cart = request.session['cart']
            return render(request, "checkout.html", {"cart": cart})
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/checkout_error/')
    return HttpResponseRedirect('/checkout_error/')

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def checkout_error(request):
    return render(request, "checkout_error.html", {})

def login_as_admin(request):
    return render(request, "login_as_admin.html", {})

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def promo_code_list(request):
    user = request.user
    try:
        custom_user = Custom_User.objects.get(user=user)
    except Custom_User.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/")
    try:
        trainer = Trainer_Model.objects.get(user=custom_user)
    except Trainer_Model.DoesNotExist:
        return HttpResponseRedirect("/invalid_trainer/") 
    if custom_user.primary_registration_type == "Trainer":
        promo_list = PromoCode.objects.all()
        context = {"promo_list": promo_list}
        return render(request, "promo_list.html", context)
    else:
        return HttpResponseRedirect("/invalid_trainer/")
	
class PromoCodeCreate(CreateView):
    template_name = "promo_create.html"
    queryset = PromoCode.objects.all()
    form_class = CreatePromoForm
    success_url = reverse_lazy('list_promocode')
    def form_valid(self, form):
        messages.success(self.request, 'Promo Code Created Successfully!')
        print(form.cleaned_data)
        return super().form_valid(form)
class PromoCodeDetail(DetailView):
    context_object_name = "promo"
    template_name = "promo_detail.html"
    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(PromoCode, id=id_)
class PromoCodeUpdate(UpdateView):
    template_name = "promo_create.html"
    form_class = CreatePromoForm
    success_url = reverse_lazy('list_promocode')
    def form_valid(self, form):
        messages.success(self.request, 'Promo Code Updated Successfully!')
        print(form.cleaned_data)
        return super().form_valid(form)
    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(PromoCode, id=id_)
class PromoCodeDelete(DeleteView):
    model = PromoCode
    success_url = reverse_lazy('list_promocode')
    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(PromoCode, id=id_)
    def get(self, request, *args, **kwargs):
        messages.error(request, 'Promo Code Deleted Successfully!')
        return self.post(request, *args, **kwargs) 

@login_required(login_url='/authentication/login/', redirect_field_name='next')
def apply_promo(request):
    user = request.user
    custom_user = get_object_or_404(Custom_User, user=user)
    if str(custom_user.primary_registration_type) == "Learner":
        learner = True
        if request.method == "POST":
            form = ApplyPromoForm(request.POST)
            if form.is_valid():
                instance = form
                promo_code = instance.cleaned_data.get('promo_code')
                try:
                    promo_code = get_object_or_404(PromoCode, code=promo_code)
                    if(promo_code.active):
                        course = promo_code.course
                        student, created = Learner_Model.objects.get_or_create(user=custom_user)
                        if created == False:
                            if course in student.courses_subscribed.all():
                                messages.error(request, 'You are already subscribed to this course!')
                            else:
                                student.courses_subscribed.add(course)
                                messages.success(request, 'You can now access course ' + str(course) + ' !!!')
                                return HttpResponseRedirect("/learner_dashboard/") 
                        else:
                            student.courses_subscribed.add(course)
                            student.save()
                            messages.success(request, 'You can now access course ' + str(course) + ' !!!')
                    else:
                        messages.error(request, 'Promo Code Inactive!')
                except:
                    messages.error(request, 'Promo Code Invalid!')
        else:
            form = ApplyPromoForm()
        context = {'form':form, 'learner':learner}        
    else:
        learner = False
        context = {'learner':learner}        
    return render(request, "apply_promo.html", context)   

@login_required(login_url='/authentication/login/')
def submit_assignment_form_view(request):
    custom_user = get_object_or_404(Custom_User, user=request.user)
    if str(custom_user.primary_registration_type) == "Learner":
        learner = True
    else:
        return HttpResponseRedirect("/invalid_learner/")
    form = SubmitAssignmentForm(request.POST, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            instance = form
            company = instance.cleaned_data.get('company')
            details = instance.cleaned_data.get('assignment_details')
            upload_assignment = instance.cleaned_data.get('upload_assignment')
            first_name = request.user.first_name
            last_name = request.user.last_name
            name = first_name+ " " +last_name
            email = str(request.user.email)
            contact = str(custom_user.mobile)
            new_assignment = submitted_assignment(name = name, email = email, contact = contact, company = company, details = details, upload_assignment = upload_assignment)
            new_assignment.save()
            qs = User.objects.filter(email__in=['surendra.panpaliya@gmail.com', 'sanket.lolge@gmail.com'])
            notify.send(request.user, recipient=qs, verb= name +'(Learner) has submitted new assignment. ')
            subject = 'New assignment submitted'
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email,"sanket.lolge@gmail.com","surendra@gktcs.com"]
            contact_message = name +'(Learner) has submitted new assignment.'
            send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
            messages.success(request, "Your Assignment Has Successfully Submitted.")
            return HttpResponseRedirect("/my_assignments/")
        # subject = 'Django Modules'
        # from_email = settings.EMAIL_HOST_USER
        # to_email = [from_email,email,"surendra@gktcs.com","sanket.lolge@gmail.com"]
        # contact_message = " Client Details--> Name: %s , Email Id: %s  -->Selected Modules: %s"%(name, email, m)
        # send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
        # messages.success(request, 'Thank you, we will get back to you shortly')
        context = {"form":form}
    else:
        form = SubmitAssignmentForm()
        context = {"form":form, 'learner':learner}
    return render(request, "submit_assignment_form.html", context)

@login_required(login_url='/authentication/login/')
def submitted_assignment_view(request):
    submissions = submitted_assignment.objects.all()
    return render(request, 'submitted_assignment.html',locals())

@login_required(login_url='/authentication/login/')
def my_assignments_view(request):
    if request.user.is_authenticated:
        print("Authenticated")
        try:
            custom_user = Custom_User.objects.get(user = request.user)
            if str(custom_user.primary_registration_type) == "Learner":
                learner = True
                print("A Learner")
        except:
            pass
    #course = get_object_or_404(Course, id=course_id)
    if learner == True:
        try:
            submissions = submitted_assignment.objects.filter(email=request.user.email)
            print("Student")
        except Exception as e:
            student = None
            print("Not a student.")
    else:
        print("Not a Learner")
        allow_access = False   
    context = {"submissions": submissions}
    return render(request, "my_assignments.html", context)
	
def provide_acess_on_payment(request):
    if request.method == 'POST':
        posted_data = json.loads(request.body)
        courses_ids = posted_data["courses_ids"]
        for id in  courses_ids:
            print(id)
        user = request.user
        custom_user = get_object_or_404(Custom_User, user=user)
        refund = 0
        paid = 0
        courses_paid_for = ""
        refund_for = ""
        if str(custom_user.primary_registration_type) == "Learner":
            student, created = Learner_Model.objects.get_or_create(user=custom_user)
            if created == False:
                for id in  courses_ids:
                    course = Course.objects.get(id=id)
                    if course in student.courses_subscribed.all():
                        refund = refund + course.fees
                        paid = paid + course.fees
                        courses_paid_for = courses_paid_for + str(course) + ", "
                        refund_for = refund_for + str(course) + ", "
                    else:
                        paid = paid + course.fees
                        student.courses_subscribed.add(course)
                        courses_paid_for = courses_paid_for + str(course) + ", "
            else:
                for id in  courses_ids:
                    course = Course.objects.get(id=id)
                    paid = paid + course.fees
                    student.courses_subscribed.add(course)
                    courses_paid_for = courses_paid_for + str(course) + ", "
            student.credit_balance = student.credit_balance + refund             
            student.save()
            receipt = CourseFeeReceipt.objects.create(user=request.user, courses_paid_for=courses_paid_for, refund=refund, paid=paid, refund_for=refund_for)
            receipt.save()
        print("Granted Access Successfully")
        return HttpResponse('Access Provided 200 All Ok')
    else:
        print("POST request not completed.")
        return HttpResponse("Not a POST Method")


@login_required(login_url='/authentication/login/', redirect_field_name='next')
def my_receipts(request):
    user = request.user
    custom_user = get_object_or_404(Custom_User, user=user)
    if str(custom_user.primary_registration_type) == "Learner":
        learner = Learner_Model.objects.get(user=custom_user)
        credit_balance = learner.credit_balance
        receipts = CourseFeeReceipt.objects.filter(user=user).order_by('-created_at')
        return render(request, "my_receipts.html", {"receipts":receipts, "credit_balance":credit_balance})
    else:
        return reverse('checkout_error')