from django.contrib import admin
from lms.models import *
from guardian.admin import GuardedModelAdmin

class BlogAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',)}
    list_display = ["title", "created", "updated", "publish", "draft"]
    list_display_links = ["updated"]
    list_editable = ["title"]
    list_filter = ["updated", "created", "title", "publish", "draft"]
    search_fields = ["title", "content"]
    class Meta:
        model = Blog

class Course_ModuleInline(admin.StackedInline):
    model = Course_Module

class CourseAdmin(admin.ModelAdmin):
    inlines = [
        Course_ModuleInline
    ]
    model = Course

class CourseAdmin(GuardedModelAdmin):
    model = Course

class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "course", "active"]
    class Meta:
        model = PromoCode	
# Register your models here.
admin.site.register(select_module)
admin.site.register(Custom_User)
admin.site.register(userprofile)
admin.site.register(intern_profile)
admin.site.register(jobseeker_profile)
admin.site.register(add_instructor)
admin.site.register(Trainer_Model)
admin.site.register(Learner_Model)
admin.site.register(Course, CourseAdmin)
admin.site.register(Course_Module)
admin.site.register(Topic)
admin.site.register(Answer_Options)
admin.site.register(Quiz)
admin.site.register(Quiz_Question)
admin.site.register(vendor_enquiry)
admin.site.register(client_enquiry)
admin.site.register(learner_enquiry)
admin.site.register(job_seeker)
admin.site.register(support)
admin.site.register(Blog, BlogAdmin)
admin.site.register(LearnerQnA)
admin.site.register(Subscription)
admin.site.register(submitted_assignment)
admin.site.register(CourseFeeReceipt)
admin.site.register(PromoCode, PromoCodeAdmin)