from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Answer_Option(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Answer Option"
        verbose_name_plural = "Answer Options"


class Quiz(models.Model):
    quiz_name = models.CharField(max_length=200)
    time_limit = models.IntegerField(default=1)

    def __str__(self):
        return self.quiz_name

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizes"


class Quiz_Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='questions')
    text = models.CharField(max_length=200)
    possible_answers = models.ManyToManyField(Answer_Option)
    selected = models.ForeignKey(Answer_Option, related_name="selected", default=None, on_delete=models.CASCADE, blank=True, null=True)
    correct = models.ForeignKey(Answer_Option, related_name="correct", default=None, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Quiz Question"
        verbose_name_plural = "Quiz Questions"


class Candidate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, default=None, null=True)
    score = models.IntegerField(default=0)
    taken_quiz = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"


class CandidateQuestionAnswer(models.Model):
    quiz_question = models.ForeignKey(Quiz_Question, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    selected = models.ForeignKey(Answer_Option, related_name="selected_answer", default=None, on_delete=models.CASCADE, blank=True, null=True)
    correct = models.ForeignKey(Answer_Option, related_name="correct_answer", default=None, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.candidate.user.username

    class Meta:
        verbose_name = "Candidate QnA"
        verbose_name_plural = "Candidate QnA's"
