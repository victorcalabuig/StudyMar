from django.db import models

# Create your models here.

class User(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

	def __str__(self):
		return self.username

class Exam(models.Model):
	username = models.ForeignKey(User, on_delete=models.CASCADE)
	course_name = models.CharField(max_length=100)
	exam_date = models.DateTimeField('Examination Day')
	pages = models.IntegerField()

	def __str__(self):
		return self.course_name