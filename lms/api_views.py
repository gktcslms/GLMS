from .models import Blog
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAdminUser
from .models import Course, Course_Module, Custom_User, Trainer_Model

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blogs to be viewed or edited.
    """
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Custom_UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blogs to be viewed or edited.
    """
    permission_classes = (IsAdminUser,)    
    queryset = Custom_User.objects.all()
    serializer_class = Custom_UserSerializer


class BlogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blogs to be viewed or edited.
    """
    permission_classes = (IsAdminUser,)    
    queryset = Blog.objects.all().order_by('-created')
    serializer_class = BlogSerializer


class Trainer_ModelViewSet(viewsets.ModelViewSet):
    queryset = Trainer_Model.objects.all()
    serializer_class = Trainer_ModelSerializer
    

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blogs to be viewed or edited.
    """
    #permission_classes = (IsAdminUser,)    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class Course_ModuleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blogs to be viewed or edited.
    """
    #permission_classes = (IsAdminUser,)    
    queryset = Course_Module.objects.all()
    serializer_class = Course_ModuleSerializer

class Answer_OptionsViewSet(viewsets.ModelViewSet):
    queryset = Answer_Options.objects.all()
    serializer_class = Answer_OptionsSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class Quiz_QuestionViewSet(viewsets.ModelViewSet):
    queryset = Quiz_Question.objects.all()
    serializer_class = Quiz_QuestionSerializer	

