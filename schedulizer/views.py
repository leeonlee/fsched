from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from forms import CourseForm
from schedulizer.models import *

def index(request):
	return render_to_response('schedulizer/index.html')

def addClasses(request):
	if request.method == 'POST':
		courses = request.POST.getlist('course')
		courseList = []
		for course in courses:
			courseList.append(Course.objects.get(id = course))
		print 'courses inputted', courseList
	form = CourseForm()
	return render_to_response('schedulizer/addClasses.html',{
		'form':form,
	}, RequestContext(request))

def finalSchedule(request):
	return render_to_response('schedulizer/finalSchedule.html')

def inputDars(request):
	if request.method == 'POST':
		print "banana"
	return render_to_response('schedulizer/inputDars.html', RequestContext(request))
