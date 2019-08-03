from django.urls import path

from . import views 

app_name = 'StudyMarApp'
urlpatterns = [
	
	path('', views.login, name='login'),	

	path('auth', views.auth, name='auth'),

	path('<username>/detail/<course>', views.detail, name='detail'),

	path('<username>/home', views.home, name='home'),

	
]