from django.contrib import admin

from .models import User, Exam, Plan, Areas, TimeSlot

# Register your models here.

admin.site.register(User)
admin.site.register(Exam)
admin.site.register(Plan)
admin.site.register(Areas)
admin.site.register(TimeSlot)

