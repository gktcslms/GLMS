from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')

class Custom_UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Custom_User
        fields = ('url','user', 'mobile', 'primary_registration_type')

class BlogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blog
        fields = ('url', 'title', 'blogger', 'image', 'content', 'draft', 'likes')
class Trainer_ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trainer_Model
        fields = ('url', 'user', 'city', 'state', 'country', 'profile_picture', 'courses_tutoring', 'describe_yourself', 'linked_in_url', 'cv')

class Learner_ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Learner_Model
        fields = ('url', 'user', 'profile_picture', 'courses_subscribed')

class Answer_OptionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer_Options
        fields = ('url', 'text')



class Quiz_QuestionSerializer(serializers.HyperlinkedModelSerializer):
    possible_answers = Answer_OptionsSerializer(many=True)
    correct = Answer_OptionsSerializer()
    class Meta:
        model = Quiz_Question
        fields = ('url', 'quiz', 'q_type', 'text', 'possible_answers', 'selected', 'correct')

    def create(self, validated_data):
        possible_answers_data = validated_data.pop('possible_answers')
        selected_answers_data = validated_data.pop('selected')
        correct_answers_data = validated_data.pop('correct')
        quiz_question = Quiz_Question.objects.create(**validated_data)
        if possible_answers_data:
            for answer in possible_answers_data:
                answer, created  = Answer_Options.objects.get_or_create(text=answer['text'])     
                if (answer.text == correct_answers_data['text']):
                    quiz_question.correct = answer 
                    quiz_question.save()                              
                quiz_question.possible_answers.add(answer)
        return quiz_question

    def update(self, instance, validated_data):
        instance.quiz = validated_data.get('quiz', instance.quiz)
        instance.q_type = validated_data.get('q_type', instance.q_type)
        instance.text = validated_data.get('text', instance.text)
        instance.order = validated_data.get('order', instance.order)
        try:
            correct_answer = validated_data.pop('correct')
            if correct_answer:
                correct_answer, created  = Answer_Options.objects.get_or_create(text=correct_answer['text'])
                instance.correct = correct_answer
        except:
            pass
        try:
            selected_answer = validated_data.pop('selected')
        except:
            pass
        try:
            possible_answers = validated_data.pop('possible_answers')
            if possible_answers:
                possible_answers_list = []
                for pa in possible_answers:
                    answer, created  = Answer_Options.objects.get_or_create(text=pa['text'])
                    possible_answers_list.append(answer)        
                instance.possible_answers = possible_answers_list
        except:
            pass
        instance.save()
        return instance 



class QuizSerializer(serializers.HyperlinkedModelSerializer):
    questions = Quiz_QuestionSerializer(many=True)
    class Meta:
        model = Quiz
        fields = ('url', 'id', 'quiz_name', 'module_referred', 'questions')


class Course_ModuleSerializer(serializers.HyperlinkedModelSerializer):
    video = serializers.FileField(max_length=None, use_url=True, required=False)
    quiz = QuizSerializer(many=True, required=False)
    class Meta:
        model = Course_Module
        fields = ('id', 'url', 'part_of', 'name', 'video', 'Presentation', 'Assignment', 'labsession', 'reference1', 'reference2', 'reference3', 'topics', 'order', 'quiz', 'allow_preview')

    def create(self, validated_data):
        quiz_data = validated_data.pop('quiz')
        module = Course_Module.objects.create(**validated_data)
        for qd in quiz_data:
            Quiz.objects.create(module_referred = module, **qd)
        return module

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.part_of = validated_data.get('part_of', instance.part_of)
        instance.video = validated_data.get('video', instance.video)
        instance.Presentation = validated_data.get('Presentation', instance.Presentation)
        instance.Assignment = validated_data.get('Assignment', instance.Assignment)
        instance.labsession = validated_data.get('labsession', instance.labsession)
        instance.reference1 = validated_data.get('reference1', instance.reference1)
        instance.reference2 = validated_data.get('reference2', instance.reference2)
        instance.reference3 = validated_data.get('reference3', instance.reference3)
        instance.topics = validated_data.get('topics', instance.topics)
        instance.order = validated_data.get('order', instance.order)
        instance.allow_preview = validated_data.get('allow_preview', instance.allow_preview)
        try:
            quiz_data = validated_data.get('quiz')
        except:
            pass
        if quiz_data:
            # instance.quiz.clear()
            Quiz.objects.bulk_create(
               [
                 Quiz(module_referred=instance, **quiz)
                 for quiz in quiz_data
               ],
            )
        instance.save()
        return instance 


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    modules = Course_ModuleSerializer(many=True)
    class Meta:
        model = Course
        fields = ('url', 'id', 'thumbnail', 'course_by', 'course_name', 'description','objectives', 'prerequisite', 'requirements', 'modules', 'fees')

class LearnerQuestionAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LearnerQnA
        fields = ('quiz_question', 'learner', 'chosen_option')

    def to_representation(self, instance):
        self.fields['quiz_question'] = Quiz_QuestionSerializer()
        self.fields['learner'] = Learner_ModelSerializer()
        self.fields['chosen_option'] = Answer_OptionsSerializer()
        return super(LearnerQuestionAnswerSerializer, self).to_representation(instance)
