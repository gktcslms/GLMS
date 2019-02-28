from django.contrib.auth.models import User
from .models import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from django.shortcuts import get_list_or_404, get_object_or_404


class Answer_OptionViewSet(viewsets.ModelViewSet):
    queryset = Answer_Option.objects.all()
    serializer_class = Answer_OptionSerializer



class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer



class Quiz_QuestionViewSet(viewsets.ModelViewSet):
    queryset = Quiz_Question.objects.all()
    serializer_class = Quiz_QuestionSerializer
