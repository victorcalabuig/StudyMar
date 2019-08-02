from django.urls import path

from . import views 

app_name = 'StudyMarApp'
urlpatterns = [
	
	path('', views.login, name='login'),	

	path('auth', views.auth, name='auth'),

	path('<username>/home', views.home, name='home'),

	
]