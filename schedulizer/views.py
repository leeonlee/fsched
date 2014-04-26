from django.shortcuts import render
from django.shortcuts import render_to_response

def index(request):
	return render_to_response('schedulizer/index.html')

def addClasses(request):
	return render_to_response('schedulizer/addClasses.html')

def finalSchedule(request):
	return render_to_response('schedulizer/finalSchedule.html')

def inputDars(request):
	return render_to_response('schedulizer/inputDars.html')
