from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from lms.models import Custom_User
from django.http import JsonResponse
import json
# Create your views here.

@login_required(login_url='/authentication/login/')
def home(request):
    custom_user = Custom_User.objects.get(user = request.user)
    if str(custom_user.primary_registration_type) == "Learner":
        base_template_name = 'learner_dashboard.html'
    if str(custom_user.primary_registration_type) == "Intern":
        base_template_name = 'intern_dashboard.html'
    if str(custom_user.primary_registration_type) == "Trainer":
        base_template_name = 'base_dashboard.html'
    quizes_available = Quiz.objects.all()
    return render(request, 'quiz_home.html', {"quizes_available": quizes_available, "base_template_name":base_template_name})


@login_required(login_url='/authentication/login/')
def manage_quizes(request):
    return render(request, 'manage_quizes.html', {})

@login_required(login_url='/authentication/login/')
def top_scorers(request, id):
	try:
		quiz = Quiz.objects.get(id=id)
		top_scorers_list = Candidate.objects.filter(quiz=quiz, taken_quiz=True).order_by('-score')
		context = {"top_scorers_list": top_scorers_list, "quiz":quiz}
	except Exception as e:
		context = {"error": e}
	return render(request, 'top_scorers.html', context)


@login_required(login_url='/authentication/login/')
def take_quiz(request, id):
    custom_user = Custom_User.objects.get(user = request.user)
    if str(custom_user.primary_registration_type) == "Learner":
        base_template_name = 'learner_dashboard.html'
    if str(custom_user.primary_registration_type) == "Intern":
        base_template_name = 'intern_dashboard.html'
    if str(custom_user.primary_registration_type) == "Trainer":
        base_template_name = 'base_dashboard.html'
    quiz = Quiz.objects.get(id=id)
    try:
        candidate_object = Candidate.objects.get(user=request.user, quiz=quiz)
        context = {"quiz":quiz, "base_template_name":base_template_name, "candidate_object":candidate_object}
    except Exception as e:
        context = {"quiz":quiz, "base_template_name":base_template_name}
        print(e)
    return render(request, 'take_quiz.html', context)    


@login_required(login_url='/authentication/login/')
def view_score(request, id):
    custom_user = Custom_User.objects.get(user = request.user)
    if str(custom_user.primary_registration_type) == "Learner":
        base_template_name = 'learner_dashboard.html'
    if str(custom_user.primary_registration_type) == "Intern":
        base_template_name = 'intern_dashboard.html'
    if str(custom_user.primary_registration_type) == "Trainer":
        base_template_name = 'base_dashboard.html'
    try:
        quiz = Quiz.objects.get(id=id)
        candidate_object = Candidate.objects.get(user=request.user, quiz=quiz, taken_quiz=True)
        all_qna = CandidateQuestionAnswer.objects.filter(candidate=candidate_object, quiz_question__quiz=quiz).order_by('id')
        # all_qna
        context = {"candidate_object": candidate_object, "all_qna": all_qna, "base_template_name":base_template_name}
    except Exception as e:
        context = {"error": e}
    return render(request, 'view_score.html', context)    


def submit_quiz(request):
    if request.method == "POST":
        posted_data = json.loads(request.body)
        quiz_question_id = posted_data["quiz_question_id"]
        user_id = posted_data["user_id"]
        chosen_answer_id = posted_data["chosen_answer_id"]
        correct_answer_id = posted_data["correct_answer_id"]
        quiz_id = posted_data["quiz_id"]
        quiz_object = Quiz.objects.get(id=quiz_id)
        quiz_question_obj = Quiz_Question.objects.get(id=quiz_question_id)
        selected_answer_object = Answer_Option.objects.get(id=chosen_answer_id)
        correct_answer_object = Answer_Option.objects.get(id=correct_answer_id)
        try:
            candidate_object = Candidate.objects.get(user=request.user, quiz=quiz_object, score=0)
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'Candidate Object does not exist or has multiple instances or has already taken test!'})
        candidate_qna_object = CandidateQuestionAnswer.objects.create(quiz_question=quiz_question_obj, 
                                                                      candidate=candidate_object, 
                                                                      selected=selected_answer_object,
                                                                      correct=correct_answer_object)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad_request'})


def create_candidate_record(request):
    if request.method == "POST":
        posted_data = json.loads(request.body)
        user_id = posted_data["user_id"]
        quiz_id = posted_data["quiz_id"]
        quiz_object = Quiz.objects.get(id=quiz_id)
        user = User.objects.get(id=user_id)
        candidate_object = Candidate.objects.create(user=user, quiz=quiz_object, score=0)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad_request'})



def submit_score(request):
    if request.method == "POST":
        try:
            posted_data = json.loads(request.body)
            score = posted_data["score"]
            user_id = posted_data["user_id"]
            quiz_id = posted_data["quiz_id"]
            quiz_object = Quiz.objects.get(id=quiz_id)
            user = User.objects.get(id=user_id)
            candidate_object = Candidate.objects.get(user=user, quiz=quiz_object, score=0, taken_quiz=False)
            candidate_object.score = score
            candidate_object.taken_quiz = True
            candidate_object.save()
        except Exception as e:
            print("\n"*20)
            print(e)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'bad_request'})

