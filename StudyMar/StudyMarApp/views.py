from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import User, Exam, Session
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

	initial_session = Session(pages_studied=0, time_taken=0, speed=time_estimate, 
		session_date=timezone.now(), username_id=user.id, exam_id=new_exam.id)
	initial_session.save()


	return HttpResponseRedirect(reverse('StudyMarApp:home', args=(user.username,)))




def registerSession(request, username):

	user = User.objects.get(username=username)
	latest_exam_list = Exam.objects.filter(username_id=user.id)




	template = loader.get_template('StudyMarApp/registerSession.html')
	context = {'user':user, 'latest_exam_list':latest_exam_list}

	return HttpResponse(template.render(context, request))

def saveSession(request, username): 
	user = User.objects.get(username=username)

	username_id = user.id
	exam_id = request.POST['exam_id']
	pages_studied = request.POST['pages_studied']
	time_taken = request.POST['time_taken']
	session_date = request.POST['session_date']

	if (pages_studied=="" or time_taken=="" or session_date=="" 
		or exam_id==""):
		error_message = "Fill in ALL the fields!"
		template = loader.get_template('StudyMarApp/registerSession.html')
		latest_exam_list = Exam.objects.filter(username_id=user.id)
		context = {'user':user, 'latest_exam_list':latest_exam_list, 
		'error_message':error_message}
		return HttpResponse(template.render(context, request))

	else:
		speed = int(time_taken) / int(pages_studied)

		new_session = Session(pages_studied=pages_studied, time_taken=time_taken, 
			speed=speed, session_date=session_date, exam_id=exam_id, username_id=username_id)
		new_session.save()
		return HttpResponseRedirect(reverse('StudyMarApp:home', args=(user.username,)))









def detail(request, username, course):

	user = User.objects.get(username=username)
	exam = Exam.objects.get(course_name=course)
	latest_session_list = Session.objects.filter(username_id=user.id).filter(
		exam_id=exam.id)
	past_speeds = []
	total_pages_studied = []
	total_dedicated_time = []
	for session in latest_session_list:
		past_speeds.append(session.speed)
		total_pages_studied.append(session.pages_studied)
		total_dedicated_time.append(session.time_taken)

	# calculate days left and study days (7 day margin)
	exam_date = exam.exam_date
	days_left_exam = (exam_date - timezone.now()).days
	days_left_study = days_left_exam - 7


	# calculate new average study speed
	avg_speed = sum(past_speeds) / len(past_speeds)

	# calculate pages left
	total_pages_studied = sum(total_pages_studied)
	pages_left = exam.pages - total_pages_studied
	progress_percentage = int(((total_pages_studied / exam.pages) * 100) + 0.5) 

	# calculate total time necessary to study pages left
	total_study_time = pages_left * avg_speed

	# distribute that study time into available study days
	study_per_day = int(total_study_time / days_left_study)


	total_dedicated_time = int((sum(total_dedicated_time)/60) * 100) / 100





	template = loader.get_template('StudyMarApp/detail.html')
	context = {
		'user':user, 'exam':exam, 
		'latest_session_list':latest_session_list,
		'days_left_exam':days_left_exam, 'days_left_study':days_left_study,
		'avg_speed':avg_speed, 'pages_left':pages_left, 
		'total_study_time':total_study_time, 'total_pages_studied':total_pages_studied,
		'study_per_day':study_per_day, 'total_dedicated_time':total_dedicated_time,
		'progress_percentage':progress_percentage,
	}

	return HttpResponse(template.render(context, request))


	



	












	
	# exam = Exam.objects.get(course_name=course)
	
	# # total amount of study time needed (aprox.)
	# time_estimate = exam.time_estimate
	# pages = exam.pages
	# total_study_time = time_estimate * pages

	# # Days left for the exam:
	# exam_date = exam.exam_date
	# days_left = (exam_date - timezone.now()).days

	# # Days to study (days for exam - 7, which are reserved to review and practice)
	# study_days = days_left - 7

	# # Amount of time to study each day 
	# study_per_day = int(total_study_time / study_days)




	# context = {'exam':exam, 'total_study_time':total_study_time, 'days_left':days_left, 
	# 'study_days':study_days, 'study_per_day':study_per_day}
	# template = loader.get_template('StudyMarApp/detail.html')
	
	# return HttpResponse(template.render(context, request))
	
	# return HttpResponse("Estas en la vista detalle del curso %s del usuario %s, y tienes %i días para aprenderte la teoría." % (course, username, days))