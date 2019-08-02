from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import User
from django.urls import reverse



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
	return HttpResponse("You are in the home page of the user %s." % username)