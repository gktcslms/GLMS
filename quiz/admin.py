from django.contrib import admin
from .models import *
# Register your models here.

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'taken_quiz')
    list_filter = ('quiz', 'score', 'taken_quiz')

class CandidateQuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'quiz_question', 'selected', 'correct')

admin.site.register(Answer_Option)
admin.site.register(Quiz)
admin.site.register(Quiz_Question)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(CandidateQuestionAnswer, CandidateQuestionAnswerAdmin)