"""SRC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from lms.views import *
from rest_framework import routers
from lms import api_views
import notifications.urls
from chat_bot import views as chat_bot_views

router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'custom_users', api_views.Custom_UserViewSet)
router.register(r'blogs', api_views.BlogViewSet)
router.register(r'courses', api_views.CourseViewSet)
router.register(r'courses_modules', api_views.Course_ModuleViewSet)
#router.register(r'courses_modules', api_views.Course_ModuleViewSet)
router.register(r'trainers', api_views.Trainer_ModelViewSet)
router.register(r'learners', api_views.Learner_ModelViewSet)
router.register(r'answer_options', api_views.Answer_OptionsViewSet)
router.register(r'quiz', api_views.QuizViewSet)
router.register(r'quiz_questions', api_views.Quiz_QuestionViewSet)
router.register(r'paginated_courses', api_views.PaginatedViewSet)
router.register(r'learner_qa/(?P<quiz_id>[0-9]+)', api_views.LearnerQuestionAnswerList, base_name="learner_qa")
router.register(r'learner_qa', api_views.LearnerQuestionAnswerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('detail22/', detail, name="detail"),
    path('detail/', detail, name="detail"),
    path('surendra/',surendra_profileview,name="surendra_profile"),
    path('surendra_docx/', send_surendra_profile_doc,name="surendra_doc"),
    path('contact/',contactview,name="contact"),
    path('courses/',courseview,name="Courses"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('registration.backends.default.urls')),
    path('authentication/register/', custom_user_creation, name='custom_user_creation'),
    path('authentication/activate_user/', activate_user, name='activate_user'),
    path('authentication/login/', my_login, name='my_login'),
    path('authentication/logout/', logout_view, name='logout'),
    path('base/',baseview,name="base"),
    path('help/',helpview,name="help"),
    path('learner_help/',learner_helpview,name="learner_help"),
    path('trainer_help/',trainer_helpview,name="trainer_help"),
    url(r'^learner_profile/(?P<user_id>\d+)$', learner_profileview, name="learner_profile"),
    url(r'^learner_dashboard/',learner_my_courses,name='learner_dashboard'),
    url(r'^support/',support_view,name="support"),
    re_path('myprofile/(?P<user_id>\d+)$', myprofileview, name="myprofile"),
    path('instructor/add/',instructor_addview,name="instructor_add"),
    path('python/',pythonview,name="python"),
    path('privacy/',privacyview,name="privacy"),
    path('terms/',termsview,name="terms"),
    #path('temp/',tempview),
    #url(r'^surendra_pdf', send_surendra_profile,name="surendra_pdf"),
    path('python.pdf', send_python_file),
    path('hadoop.pdf', send_hadoop_file),
    path('ruby.pdf', send_ruby_file),
    path('angularjs.pdf', send_angularjs_file),
    path('android.pdf', send_android_file),
    path('data_science.pdf', send_data_science_file),
    path('r_prog.pdf', send_r_prog_file),
    path('appium.pdf', send_appium_file),
    path('ror_content.pdf/',send_ror_content,name="ror_content.pdf"),
    path('pyspark_content.pdf/',send_pyspark_content,name="pyspark_content.pdf"),
    path('python_content.pdf/',send_python_content,name="python_content.pdf"),
    path('jython_content.pdf/',send_jython_content,name="jython_content.pdf"),
    path('python_data_science_content.pdf/',send_python_data_science_content,name="python_data_science.pdf"),
    path('python_machine_learning_content.pdf/',send_python_machine_learning_content,name="python_machine_learning_content.pdf"),
    path('django_content.pdf/',send_django_content,name="django_content.pdf"),
    path('hadoop_content.pdf/',send_hadoop_content,name="hadoop_content.pdf"),
    path('appium_content.pdf/',send_appium_content,name="appium_content.pdf"),
    path('ansible_content.pdf/',send_ansible_content,name="ansible_content.pdf"),
    path('r_programming_content.pdf/',send_r_programming_content,name="r_programming_content.pdf"),
    path('mongodb_content.pdf/',send_mongodb_content,name="mongodb_content.pdf"),
    path('ruby_devops_content.pdf/',send_ruby_devops_content,name="ruby_devops_content.pdf"),
    path('sparkscala_content.pdf/',send_sparkscala_content,name="sparkscala_content.pdf"),
    path('search/', search_titles,name="search"),
    path('pythoncorporate/',pythoncorpview,name="pythoncorp"),
    path('jythoncorporate/',jython_corporate_view,name="jythoncorp"),
    path('djangocorporate/',django_corporate_view,name="djangocorp"),
    path('pysparkcorporate/',pyspark_corporate_view,name="pysparkcorp"),
    path('hadoopcorporate/',hadoop_corporate_view,name="hadoopcorp"),
    path('appiumcorporate/',appium_corporate_view,name="appiumcorp"),
    path('ruby_on_railscorporate/',ruby_on_rails_corporate_view,name="ruby_on_railscorp"),
    path('r_programmingcorporate/',r_programming_corporate_view,name="r_programmingcorp"),
    path('ansiblecorporate/',ansible_corporate_view,name="ansiblecorp"),
    path('mongodbcorporate/',mongodb_corporate_view,name="mongodbcorp"),
    path('devopscorporate/',devops_corporate_view,name="devopscorp"),
    path('sparkscalacorporate/',sparkscala_corporate_view,name="sparkscalacorp"),
    #url(r'^select_option/',select_optionview,name="select_option"),
    path('module_enquiry/',module_enquiryview,name="module_enquiry"),
    path('trainer_form/',instructor_addview,name="instructor_add"),
    path('trainer_enquiry/',trainer_enquiryview,name="trainer_enquiry"),
    path('vendor_enquiry_form/',vendor_enquiry_form_view,name="vendor_enquiry_form"),
    path('vendor_enquiry/',vendor_enquiry_view,name="vendor_enquiry"),
    path('client_enquiry_form/',client_enquiry_form_view,name="client_enquiry_form"),
    path('client_enquiry/',client_enquiry_view,name="client_enquiry"),
    path('learner_enquiry_form/',learner_enquiry_form_view,name="learner_enquiry_form"),
    path('learner_enquiry/',learner_enquiry_view,name="learner_enquiry"),
    path('support_form/',support_form_view,name="support_form"),
    path('support/',support_view,name="support"),
    path('general_enquiry/',general_enquiry_view,name="general_enquiry"),
    path('jobs_form/',job_seeker_form_view,name="job_seeker_form"),
    path('jobs_enquiry/',job_seeker_enquiry_view,name="job_seeker_enquiry"),
    path('trainer_dashboard/',display_courses,name='trainer_dashboard'),
    path('my_dashboard/',my_dashboard,name='my_dashboard'),
    path('vendor_dashboard/',vendor_dashboard_view,name='vendor_dashboard'),
    path('client_dashboard/',client_dashboard_view,name='client_dashboard'),
    path('base_dashboard/',base_dashboard_view,name='base_dashboard'),
    path('job_seeker_dashboard/',job_seeker_dashboard_view,name='job_seeker_dashboard'),
    path('basic_registraion_details/',basic_registraion_details_view,name='basic_registraion_details'),
    re_path('edit_course/(?P<course_id>\d+)',edit_course, name='edit_course'),
    path('add_course/', add_course, name='add_course'),
    re_path('display_courses/',display_courses, name='my_courses'),
    path('all_courses/',all_courses, name='all_courses'),
    re_path('edit_course_modules/(?P<course_id>\d+)', edit_course_modules, name='edit_course_modules'),
    re_path('update_course_details/(?P<course_id>\d+)', update_course_details, name='update_course_details'),
    re_path('preview_course/(?P<course_id>\d+)', preview_course, name='preview_course'),
    re_path('learner_previewcourse/(?P<course_id>\d+)', learner_preview_course, name='learner_preview_course'),
    re_path('temp/(?P<course_id>\d+)', tempview, name='tempview'),
    re_path('delete_course/(?P<course_id>\d+)', delete_course, name='delete_course'),
    path('invalid_trainer/',invalid_trainer_view,name='invalid_trainer'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('blogs', list_blogs, name='list_blogs'),
    path('all_blogs/', all_blogs, name='all_blogs'),
    re_path('view_blog/(?P<id>\d+)/', view_blog, name='view_blog'),
    re_path('view_blog/like/(?P<id>\d+)/',  blog_like_toggle, name='like_toggle'),
    re_path('api/view_blog/like/(?P<id>\d+)/',  BlogLikeAPIToggle.as_view(), name='api_like_toggle'),
    path('create_blog/', create_blog, name='create_blog'),
    re_path('update_blog/(?P<id>\d+)/', update_blog, name='update_blog'),
    re_path('delete_blog/(?P<id>\d+)/', delete_blog, name='delete_blog'),
    path('my_blogs/', my_blogs, name='my_blogs'),
    path('submit_assignment/', submit_assignment_form_view, name='submit_assignment'),
    path('submitted_assignments/', submitted_assignment_view, name='submitted_assignments'),
    path('my_assignments/', my_assignments_view, name='my_assignments'),
    url(r'session_security/', include('session_security.urls')),
    url(r'^home2/', browse_courses, name='browse_courses'),
    url(r'^update_cart_session/', update_cart_session, name='update_cart_session'), 
    url(r'^checkout/', checkout, name='checkout'),         
    url(r'^checkout_error/', checkout_error, name='checkout_error'),
    url(r'^learner_my_courses/', learner_my_courses, name='learner_my_courses'),
    url(r'^browse_course_details/(?P<course_id>\d+)', browse_course_details, name='browse_course_details'),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^notifications/', notifications_view, name='notifications_show'),
    url(r'^list_promocode/', promo_code_list, name='list_promocode'),         
    url(r'^update_promocode/(?P<id>\d+)', PromoCodeUpdate.as_view(), name='update_promocode'),         
    url(r'^create_promocode/', PromoCodeCreate.as_view(), name='create_promocode'),       
    url(r'^detail_promocode/(?P<id>\d+)', PromoCodeDetail.as_view(), name='detail_promocode'),         
    url(r'^delete_promocode/(?P<id>\d+)', PromoCodeDelete.as_view(), name='delete_promocode'),
    url(r'^apply_promo/', apply_promo, name='apply_promo'),	
    #url(r'^login_as_admin/', login_as_admin, name='login_as_admin'), 
    url(r'^provide_acess_on_payment/', provide_acess_on_payment, name='provide_acess_on_payment'),
    url(r'^my_receipts/', my_receipts, name='my_receipts'),
    path('chat/', chat_bot_views.chat, name='chat_view'),
    path('ajax_chat/', chat_bot_views.ajax_chat, name='ajax_chat_view'),
    url(r'/$',home,name="home"),
    path('',home,name="home"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
