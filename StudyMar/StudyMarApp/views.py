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

	new_exam = Exam(time_estimate=time_estimate, course_name=course_name, exam_date=exam_date, pages=pages, username_id=username_id)
	new_exam.save()

	return HttpResponseRedirect(reverse('StudyMarApp:home', args=(user.username,)))



def detail(request, username, course):
	# return HttpResponse("Estas en la vista detalle del curso %s del usuario %s." % (course, username))

	# Calculate available (recomended) days (exam date -10)
	exam = Exam.objects.get(course_name=course)
	days = (exam.exam_date - timezone.now()).days - 10 
	context = {'exam':exam}
	template = loader.get_template('StudyMarApp/detail.html')
	
	return HttpResponse(template.render(context, request))
	
	# return HttpResponse("Estas en la vista detalle del curso %s del usuario %s, y tienes %i días para aprenderte la teoría." % (course, username, days))

	



