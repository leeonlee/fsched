from django.contrib import admin
from schedulizer.models import Course, Department, Attribute

# Register your models here.
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Attribute)
