from django.contrib import admin

from .models import User, Exam

# Register your models here.

admin.site.register(User)
admin.site.register(Exam)