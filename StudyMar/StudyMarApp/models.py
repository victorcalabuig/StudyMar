from django.db import models

# Create your models here.

class User(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

	def __str__(self):
		return self.username


class Exam(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	exam_name = models.CharField(max_length=200)
	exam_date = models.DateTimeField()
	exam_weight = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return self.exam_name


class Plan(models.Model):
	BY_OBJECTIVES = 'OB'
	BY_TIME = 'TM'

	PROGRESS_UNIT_CHOICES = [
		(BY_OBJECTIVES, 'Por objetivos'),
		(BY_TIME, 'Por tiempo'),
	]

	exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
	plan_name = models.CharField(max_length=100)
	plan_description = models.CharField(max_length=500)
	plan_start_date = models.DateTimeField()
	plan_end_date = models.DateTimeField()

	exam_progress_unit = models.CharField(
		max_length=2,
		choices=PROGRESS_UNIT_CHOICES,
		default=BY_OBJECTIVES,
	)

	create_timetable = models.BooleanField(default=False)
	use_spacing = models.BooleanField(default=False)
	session_design = models.BooleanField(default=False)

	MIXED = 'MX'
	BLOCK = 'BL'

	SESSION_DESIGN_CHOICES = [
		(MIXED, "Sesion mixta"),
		(BLOCK, "'Full block'"),
	]

	session_style = models.CharField(
		max_length=2,
		choices=SESSION_DESIGN_CHOICES,
		null=True,
		blank=True,
	)

	fixed_timetable = models.BooleanField(default=True)

	def __str__(self):
		return self.plan_name + " - " + self.exam.exam_name



class Areas(models.Model):
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
	area_name = models.CharField(max_length=100)
	area_description = models.CharField(max_length=500)
	area_weight = models.IntegerField()
	area_priority = models.IntegerField()

	BY_OBJECTIVES = 'OB'
	BY_TIME = 'TM'

	PROGRESS_UNIT_CHOICES = [
		(BY_OBJECTIVES, 'Por objetivos'),
		(BY_TIME, 'Por tiempo'),
	]

	area_progress_unit = models.CharField(
		max_length=2,
		choices=PROGRESS_UNIT_CHOICES,
		default=BY_OBJECTIVES,
	)

	PAGES = 'PG'
	EXERCISES = 'EX'
	TOPICS = 'TP'
	SLIDES = 'SL'
	SUBTOPICS = 'ST'
	TIME = 'TM'

	AREA_UNIT_CHOICES = [
		(PAGES, 'paginas'),
		(EXERCISES, 'ejercicios'),
		(TOPICS, 'temas'),
		(SLIDES, 'diapositivas'),
		(SUBTOPICS, 'subtemas'),
		(TIME, 'tiempo'),
	]

	area_unit = models.CharField(
		max_length=2,
		choices=AREA_UNIT_CHOICES,
		default=PAGES,
	)

	content_quantity = models.IntegerField(null=True, blank=True)
	laps = models.IntegerField(default=1)
	mixable = models.BooleanField(default=True)

	def __str__(self):
		exam = Exam.objects.get(id=self.plan.exam_id)
		return self.area_name + " de " + self.plan.plan_name + " - " + exam.exam_name



class TimeSlot(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

	MONDAY = 'MO'
	TUESTDAY = 'TU'
	WEDNESDAY = 'WE'
	THURSDAY = 'TH'
	FRIDAY = 'FR'
	SATURDAY = 'SA'
	SUNDAY = 'SU'

	WEEK_DAY_CHOICES = [
		(MONDAY, 'lunes'),
		(TUESTDAY, 'martes'),
		(WEDNESDAY, 'miercoles'),
		(THURSDAY, 'jueves'), 
		(FRIDAY, 'viernes'), 
		(SATURDAY, 'sabado'),
		(SUNDAY, 'domingo'),
	]

	week_day = models.CharField(
		max_length=2,
		choices=WEEK_DAY_CHOICES,
	)

	time_slot_start = models.TimeField()
	time_slot_end = models.TimeField()

	def __str__(self):
		return self.week_day + " - " + str(self.time_slot_start) + " - asignada al plan: " + self.plan.plan_name

