from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import User, Exam
from django.urls import reverse
import datetime
from django.utils import timezone


# Create your views here.


def login(request):
	# return HttpResponse('estas en la vista de login')
	template = loader.get_template('StudyMarApp/login.html')
	user = 'victor'
	context = {'user':user}
	return HttpResponse(template.render(context, request))


def auth(request):
	# return HttpResponse("You are in the authentication view")
	# username = request.POST['username']
	try:
		user = User.objects.get(username__iexact=request.POST['username'])
	except (KeyError, User.DoesNotExist):
		template = loader.get_template('StudyMarApp/login.html')
		context = {'error_message':"There is no such username"}
		return HttpResponse(template.render(context, request))
	else:
		password = user.password
		ins_password = request.POST['password']
		if (password == ins_password):
			return HttpResponseRedirect(reverse('StudyMarApp:home', args=(user.username,)))
		else:
			context = {'error_message':"The password for the user %s is incorrect" % user.username}
			template = loader.get_template('StudyMarApp/login.html')
			return HttpResponse(template.render(context, request))

		# return HttpResponse("You are in the authentication view for the user %s." % user)



def home(request, username):
	# return HttpResponse("You are in the home page of the user %s." % username)
	user = User.objects.get(username=username)
	latest_exam_list = Exam.objects.filter(username_id=user.id)
	context = {'latest_exam_list':latest_exam_list, 'user':user}
	template = loader.get_template('StudyMarApp/home.html')
	return HttpResponse(template.render(context, request))


















def registerExam(request, username):
	# return HttpResponse("You are in the view to register a course.")
	user = User.objects.get(username=username)
	context = {'user':user}
	template = loader.get_template('StudyMarApp/registerExam.html')
	return HttpResponse(template.render(context, request))

def saveExam(request, username):
	# return HttpResponse("you are about to alter the db")
	course_name = request.POST['course_name']
	exam_date = request.POST['exam_date']
	pages = request.POST['pages']
	time_estimate = request.POST['time_estimate']


	user = User.objects.get(username=username)
	username_id = user.id

	new_exam = Exam(time_estimate=time_estimate, course_name=course_name, exam_date=exam_date, 
		pages=pages, username_id=username_id)
	new_exam.save()


	return HttpResponseRedirect(reverse('StudyMarApp:home', args=(user.username,)))




def registerSession(request, username):

	user = User.objects.get(username=username)
	latest_exam_list = Exam.objects.filter(username_id=user.id)




	template = loader.get_template('StudyMarApp/registerSession.html')
	context = {'user':user, 'latest_exam_list':latest_exam_list}

	return HttpResponse(template.render(context, request))

def saveSession(request, username): 
	# user = User.objects.get(username=username)
	# username_id = user.id

	exam_id = request.POST['exam_id']


	return HttpResponse("the selected course is %s" % exam_id)





def detail(request, username, course):
	
	exam = Exam.objects.get(course_name=course)
	
	# total amount of study time needed (aprox.)
	time_estimate = exam.time_estimate
	pages = exam.pages
	total_study_time = time_estimate * pages

	# Days left for the exam:
	exam_date = exam.exam_date
	days_left = (exam_date - timezone.now()).days

	# Days to study (days for exam - 7, which are reserved to review and practice)
	study_days = days_left - 7

	# Amount of time to study each day 
	study_per_day = int(total_study_time / study_days)




	context = {'exam':exam, 'total_study_time':total_study_time, 'days_left':days_left, 
	'study_days':study_days, 'study_per_day':study_per_day}
	template = loader.get_template('StudyMarApp/detail.html')
	
	return HttpResponse(template.render(context, request))
	
	# return HttpResponse("Estas en la vista detalle del curso %s del usuario %s, y tienes %i días para aprenderte la teoría." % (course, username, days))

	



