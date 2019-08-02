from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader



# Create your views here.


def login(request):
	# return HttpResponse('estas en la vista de login')
	template = loader.get_template('StudyMarApp/login.html')
	user = 'victor'
	context = {'user':user}
	return HttpResponse(template.render(context, request))


def auth(request):
	return HttpResponse("You are in the authentication view")

def home(request, username):
	return HttpResponse("You are in the home page of the user %s." % username)