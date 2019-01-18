from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime as dt
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
import datetime

# Create your models here.
class userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.BigIntegerField(blank=True, null=True)
    linkedin_id = models.CharField(max_length=60, blank=True)
    picture = models.ImageField(upload_to = 'images/profile_pics', default= 'images/profile_pics/default_pic.jpg', blank=True, null=True)
    city = models.CharField(max_length=15, blank=True) 	
    des = models.TextField(blank=True)
    
    def get_absolute_url(self):
        return reverse('myprofile', kwargs={'user_id': self.request.user.pk})

class intern_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=dt.now)
    mobile = models.BigIntegerField(blank=True, null=True)
    linkedin_id = models.CharField(max_length=60, blank=True)
    picture = models.ImageField(upload_to = 'images/profile_pics', blank=True, null=True)
    institute = models.CharField(max_length=50, blank=True) 	
    city = models.CharField(max_length=15, blank=True)	
    country = models.CharField(max_length=15, blank=True)	
    des = models.TextField(blank=True)
    resume = models.FileField(upload_to='documents/intern_resume/', blank=True)
    
    def get_absolute_url(self):
        return reverse('intern_profile', kwargs={'user_id': self.request.user.pk})

class select_module(models.Model):
    date = models.DateTimeField(default=dt.now, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    contact = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    modules = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
class add_instructor(models.Model):
    date = models.DateTimeField(default=dt.now, blank=True)
    f_name = models.CharField(max_length = 50)
    l_name = models.CharField(max_length = 50)
    mobile = models.BigIntegerField()
    email = models.EmailField()
    country = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    course_name = models.CharField(max_length = 100)
    linkedin_profile = models.CharField(max_length = 100, blank=True, null=True)
    about_course = models.TextField(max_length = 150)
    about_yourself = models.TextField(max_length = 150)
    upload_profile = models.FileField(upload_to='documents/trainers/', blank=True, null=True)

    def __str__(self):
        return self.f_name

class vendor_enquiry(models.Model):
	date = models.DateTimeField(default=dt.now, blank=True)
	name = models.CharField(max_length = 50)
	mobile = models.BigIntegerField()
	email = models.EmailField()
	company = models.CharField(max_length = 50)
	country = models.CharField(max_length=30, null=True)
	state = models.CharField(max_length=30, null=True)
	city = models.CharField(max_length=30, null=True)
	requirement = models.TextField(max_length = 200)
	document = models.FileField(upload_to='documents/', blank=True, null=True)
	from_date = models.DateField()
	to_date = models.DateField(default=datetime.date.today)

	def __str__(self):
		return self.name
		
class client_enquiry(models.Model):
    date = models.DateTimeField(default=dt.now, blank=True)
    name = models.CharField(max_length = 50)
    mobile = models.BigIntegerField()
    email = models.EmailField()
    company = models.CharField(max_length = 50)
    country = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    requirement = models.TextField(max_length = 200)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.name
		
class learner_enquiry(models.Model):
    date = models.DateTimeField(default=dt.now)
    name = models.CharField(max_length=200)
    mobile = models.BigIntegerField()
    email = models.EmailField()
    country = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    qualification = models.CharField(max_length=30)
    course_interest = models.CharField(max_length=100)
    message = models.TextField(max_length=200, null=True)
    def __str__(self):
        return self.name

class submitted_assignment(models.Model):
    date = models.DateTimeField(default=dt.now)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    company = models.CharField(max_length=30, null=True, blank=True)
    details = models.CharField(max_length=200, null=True, blank=True)
    upload_assignment = models.FileField(upload_to='documents/submitted_assignments/')
    def __str__(self):
        return self.name

class job_seeker(models.Model):
    date = models.DateTimeField(default=dt.now)
    name = models.CharField(max_length=200)
    mobile = models.BigIntegerField()
    email = models.EmailField()
    country = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    qualification = models.CharField(max_length=30)
    skills = models.CharField(max_length=100)
    career_interest = models.CharField(max_length=100)
    about_yourself = models.TextField(max_length=100)
    upload_resume = models.FileField(upload_to='documents/job_seeker/', blank=True, null=True)

    def __str__(self):
        return self.name

class support(models.Model):
    date = models.DateTimeField(default=dt.now, blank=True)
    name = models.CharField(max_length=200)
    contact = models.BigIntegerField()
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name
		
class Custom_User(models.Model):
    date = models.DateTimeField(default=dt.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = PhoneNumberField()
    REGISTRATION_CHOICES = (
        ('Intern', 'Intern'),
        ('Learner', 'Learner'),
        ('Trainer', 'Trainer'),
        ('Vendor', 'Vendor'),
        ('Client', 'Client'),
        ('Job Seeker', 'Job Seeker'),
    )
    primary_registration_type = models.CharField(max_length=15, choices=REGISTRATION_CHOICES)    
    secondary_registration_type = models.CharField(max_length=15, choices=REGISTRATION_CHOICES, blank=True)    
    tertiary_registration_type = models.CharField(max_length=15, choices=REGISTRATION_CHOICES, blank=True)    
    quaternary_registration_type = models.CharField(max_length=15, choices=REGISTRATION_CHOICES, blank=True)   
    
    def __str__(self):
        return self.user.email

class Trainer_Model(models.Model):
    date = models.DateTimeField(default=dt.now, blank=True)
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', blank=True)
    courses_tutoring = models.TextField()
    describe_yourself = models.TextField()
    linked_in_url = models.URLField()
    cv = models.FileField(upload_to='cvs/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.user.user.email


class Course(models.Model):
    thumbnail = models.ImageField(upload_to='images/course_thumbnails',default= 'images/course_thumbnails/default_course.jpg', blank=True, null=True)
    course_by = models.ForeignKey(Trainer_Model, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200)
    description = models.TextField()
    objectives = models.TextField()
    prerequisite = models.TextField()
    requirements = models.TextField()
    fees = models.PositiveIntegerField(blank=True, default=0, null=True)

    def get_absolute_url(self):
        return reverse('edit_course', kwargs={'course_id': self.id})

    def __str__(self):
        return self.course_name + "  --By " + self.course_by.user.user.get_full_name()

class Learner_Model(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', blank=True, null=True)
    courses_subscribed = models.ManyToManyField(Course, blank=True, null=True)
    credit_balance = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.user.user.email
		
def content_videofile_name(instance, filename):
    return '/'.join(['Videos', instance.part_of.course_by.user.user.get_full_name(), instance.part_of.course_name, filename])


def content_pptfile_name(instance, filename):
    return '/'.join(['PPT', instance.part_of.course_by.user.user.get_full_name(), instance.part_of.course_name, filename])

def content_assignmentfile_name(instance, filename):
    return '/'.join(['Assignments', instance.part_of.course_by.user.user.get_full_name(), instance.part_of.course_name, filename])

def content_labsessionfile_name(instance, filename):
    return '/'.join(['Lab Session', instance.part_of.course_by.user.user.get_full_name(), instance.part_of.course_name, filename])

def content_reference1file_name(instance, filename):
    return '/'.join(['Reference1', instance.part_of.course_by.user.user.get_full_name(), instance.part_of.course_name, filename])

def content_reference2file_name(instance, filename):
    return '/'.join(['Reference2', instance.part_of.course_by.user.user.get_full_name(), instance.part_of.course_name, filename])

def content_reference3file_name(instance, filename):
    return '/'.join(['Reference3', instance.part_of.course_by.user.user.get_full_name(), instance.part_of.course_name, filename])

class Course_Module(models.Model):
    part_of = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    video = models.FileField(   
        upload_to=content_videofile_name,
        blank=True,
        null=True
    )
    
    Presentation = models.FileField(   
        upload_to=content_pptfile_name,        
        blank=True,
        null=True
    )

    Assignment = models.FileField(   
        upload_to=content_assignmentfile_name,        
        blank=True,
        null=True
    )
    labsession = models.FileField(   
        upload_to=content_labsessionfile_name,        
        blank=True,
        null=True
    )
    reference1 = models.FileField(   
        upload_to=content_reference1file_name,        
        blank=True,
        null=True
    )
    reference2 = models.FileField(   
        upload_to=content_reference2file_name,        
        blank=True,
        null=True
    )
    reference3 = models.FileField(   
        upload_to=content_reference3file_name,        
        blank=True,
        null=True
    )

    topics = models.TextField(blank=True, null=True)

    order = models.IntegerField(blank=True, null=True)
    allow_preview = models.NullBooleanField(blank=True, null=True, default=False)
    def __str__(self):
        return self.name


class Topic(models.Model):
    part_of = models.ForeignKey(Course_Module, on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=200)

    def __str__(self):
        return self.topic_name

class Answer_Options(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Answer Option"
        verbose_name_plural = "Answer Options"


class Quiz(models.Model):
    quiz_name = models.CharField(max_length=200)
    module_referred = models.ForeignKey(Course_Module, related_name="quiz", on_delete=models.CASCADE)

    def __str__(self):
        return self.quiz_name

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizes"

class Quiz_Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='questions')
    q_type = models.CharField(max_length=50)
    text = models.CharField(max_length=200)
    possible_answers = models.ManyToManyField(Answer_Options)
    selected = models.ForeignKey(Answer_Options, related_name="selected", default=None, on_delete=models.CASCADE, blank=True, null=True)
    correct = models.ForeignKey(Answer_Options, related_name="correct", default=None, on_delete=models.CASCADE, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Quiz Question"
        verbose_name_plural = "Quiz Questions"


class LearnerQnA(models.Model):
    quiz_question = models.ForeignKey(Quiz_Question, on_delete=models.CASCADE)
    learner = models.ForeignKey(Learner_Model, on_delete=models.CASCADE)
    chosen_option = models.ForeignKey(Answer_Options, related_name="chosen_option", on_delete=models.CASCADE, default=None, blank=True, null=True)


class Subscription(models.Model):
    learner = models.ForeignKey(Learner_Model, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add = True, auto_now = False)
    end_date = models.DateTimeField()

class Blog(models.Model):
    blogger = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    # slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='blog_pics/%Y/%m/%d/', blank=True)
    content = RichTextUploadingField(config_name='default')
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    likes = models.ManyToManyField(Custom_User, related_name='blog_likes', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("view_blog", kwargs={"id": self.id})

    def get_like_url(self):
        return reverse("like_toggle", kwargs={"id": self.id})

    def get_api_like_url(self):
        return reverse("api_like_toggle", kwargs={"id": self.id})

    class Meta:
        ordering = ["-created", "-updated"]		

class PromoCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    active = models.NullBooleanField(blank=True, null=True, default=False)
    def get_absolute_url(self):
        return reverse('detail_promocode', kwargs={'id': self.id})
    def __str__(self):
        return self.code 

class CourseFeeReceipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    courses_paid_for = models.TextField()
    refund = models.PositiveIntegerField(default=0)
    paid = models.PositiveIntegerField(default=0)
    refund_for = models.TextField(default="", blank=True, null=True)
    def __str__(self):
        return self.user.email