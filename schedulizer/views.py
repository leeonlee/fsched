from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
import re
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
from schedulizer.models import *
import datetime
import os
from lxml import html
import time
import collections
import itertools

import courses
import course_refs

BU_BRAIN = "https://ssb.cc.binghamton.edu/banner/twbkwbis.P_WWWLogin"
SELECT_TERM = "https://ssb.cc.binghamton.edu/banner/hwskzdar.P_CheckAudit"
LOGIN_ELEMENT = "sid"
PASSWORD_ELEMENT = "PIN"
from forms import CourseForm

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

def getSchedules(classes):
	# classes = [ {"Subj" : value, "Crse" : value } ]
	dayConvert = {'M': 0, 'T': 1, 'W': 2, 'R': 3, 'F': 4}
	dbCourseSets = dict()
	
	i = 0
	for course in classes:
		courses_per = Course.objects.filter(department = Department.objects.get(name=course['Subj']), name = course['Crse'])
		dbCourseSets[(course['Subj'], course['Crse'])] = courses_per 
		i += 1

	dbSuperSet = list(itertools.chain.from_iterable(dbCourseSets.itervalues()))
	courseList = []
	crnsToDeptNamePairs = dict()
	for subj, crse in dbCourseSets:
		dbSet = dbCourseSets[(subj, crse)]
		lettersToFamilies = collections.defaultdict(lambda : ([], []))
		for dbCourse in dbSet:
			letter = dbCourse.sec or 'A'
			whichRefs = None
			if dbCourse.sec and len(dbCourse.secNum) > 1:
				whichRefs = 1
			else:
				whichRefs = 0
			crn = dbCourse.crn
			crnsToDeptNamePairs[crn] = (subj, crse)
			interval = course_refs.TimeInterval(dbCourse.start, dbCourse.end)
			meetingTimes = []
			for day in dbCourse.days:
				meetingTimes.append(course_refs.MeetingTime(dayConvert[day], interval))
			lettersToFamilies[letter][whichRefs].append(course_refs.CourseRef(crn, tuple(meetingTimes)))
		families = tuple(courses.CourseFamily(tuple(lectures), tuple(activities)) \
			for lectures, activities in lettersToFamilies.itervalues())
		courseList.append(courses.Course(subj, crse, families))

	schedules = list(courses.schedules_from_courses(*courseList))
	return [[crnsToDeptNamePairs[courseRef.number] + tuple(courseRef) \
		for courseRef in schedule] \
		for schedule in schedules \
	]

@csrf_protect
def getDars(request):
	if request.method == 'POST':
 		user = request.POST.get('username')
 		pw = request.POST.get('password')
		atts, classes = fetchDars(user, pw)
		classAttrs = []
		for att in atts:
			if att != 'MUSP':
				print att
				classAttrs = Course.objects.filter(attributes=Attribute.objects.get(letter=att))[:5]
			

		context = RequestContext(request, 
		{
			'attrs': classAttrs,
			'classes' : classes,
		})
		
		return render_to_response('schedulizer/recommend.html', context_instance=context)
		
	return render_to_response('schedulizer/getDars.html', RequestContext(request))

def recommend(request, atts, classes):
	return render_to_response('schedulizer/recommend.html')

def fetchDars(USER, PW):
	# get number of subjects in next term
	driver = webdriver.PhantomJS()
	driver.get(BU_BRAIN)
	time.sleep(3)
	user = driver.find_element_by_name(LOGIN_ELEMENT)
	user.send_keys(USER)
	pw = driver.find_element_by_name(PASSWORD_ELEMENT)
	pw.send_keys(PW)
	pw.submit()
	print driver.title + ": " + str(USER)
	# wait for cookie
	time.sleep(10)
	print USER + " successfully logged in"
	
	driver.get(SELECT_TERM)
	element = driver.find_element_by_xpath("/html/body/div[3]/table[1]/tbody/tr[4]/td[3]/a")
	element.click()
	tree = html.fromstring(driver.page_source)

	lines = [line.text.strip() for line in tree.xpath('//p') if line.text and ('require' in line.text or 'Required' in line.text)][:-1]
	lines = [line for line in lines if line[0] == '-']
	attributesNeeded = []
	classesNeeded = []
	for line in lines:
		result = re.search('\((\w+)\)', line)	
		if result is not None:
			attributesNeeded.append(result.groups()[0])
		result = re.search('(\S*) (\d{3})', line)
		if result is not None:
			classesNeeded.append(result.groups())

	print attributesNeeded
	print classesNeeded
	return attributesNeeded, classesNeeded
