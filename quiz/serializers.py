from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers


class Answer_OptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer_Option
        fields = ('url', 'id', 'text')


class Quiz_QuestionSerializer(serializers.HyperlinkedModelSerializer):
    possible_answers = Answer_OptionSerializer(many=True)
    correct = Answer_OptionSerializer()
    class Meta:
        model = Course_Quiz_Question
        fields = ('url', 'id', 'quiz', 'text', 'possible_answers', 'selected', 'correct')

    def create(self, validated_data):
        possible_answers_data = validated_data.pop('possible_answers')
        selected_answers_data = validated_data.pop('selected')
        correct_answers_data = validated_data.pop('correct')
        quiz_question = Course_Quiz_Question.objects.create(**validated_data)
        if possible_answers_data:
            for answer in possible_answers_data:
                answer, created  = Answer_Option.objects.get_or_create(text=answer['text'])     
                if (answer.text == correct_answers_data['text']):
                    quiz_question.correct = answer 
                    quiz_question.save()                              
                quiz_question.possible_answers.add(answer)
        return quiz_question

    def update(self, instance, validated_data):
        instance.quiz = validated_data.get('quiz', instance.quiz)
        instance.text = validated_data.get('text', instance.text)
        try:
            correct_answer = validated_data.pop('correct')
            print("\n"*10)
            print(correct_answer)
            if correct_answer:
                correct_answer, created  = Answer_Option.objects.get_or_create(text=correct_answer['text'])
                instance.correct = correct_answer
        except Exception as e:
            print(e)
        try:
            selected_answer = validated_data.pop('selected')
            print(selected_answer)
        except Exception as e:
            print(e)
        try:
            possible_answers = validated_data.pop('possible_answers')
            # print(possible_answers)
            if possible_answers:
                possible_answers_list = []
                for pa in possible_answers:
                    print(pa)
                    answer, created  = Answer_Option.objects.get_or_create(text=pa['text'])
                    possible_answers_list.append(answer)        
                instance.possible_answers.set(possible_answers_list)
        except Exception as e:
            print(e)
        print("\n"*10)
        print(instance.possible_answers)
        instance.save()
        return instance 


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    questions = Quiz_QuestionSerializer(many=True, required=False)
    class Meta:
        model = Course_Quiz
        fields = ('url', 'id', 'quiz_name', 'time_limit', 'allow_quiz', 'questions')

