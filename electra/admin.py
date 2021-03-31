from django.contrib import admin
from .models import Question, Response, Point, Profile

# Register your models here.

admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Point)
admin.site.register(Profile)
