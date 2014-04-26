# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import threading
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
import re
from schedulizer.models import *
import datetime
import os

USER = os.environ.get('FSCHED_USER')
PW = os.environ.get('FSCHED_PW')
BU_BRAIN = "https://ssb.cc.binghamton.edu/banner/twbkwbis.P_WWWLogin"
SELECT_TERM = "https://ssb.cc.binghamton.edu/banner/bwskfcls.p_sel_crse_search"
LOGIN_ELEMENT = "sid"
PASSWORD_ELEMENT = "PIN"
cookies = []
words = []
pointList = []
max_threads = 3
pool = threading.BoundedSemaphore(value = max_threads)

class Command(BaseCommand):

	class farmThread(threading.Thread):
		def __init__(self, counter):
			threading.Thread.__init__(self)
			self.driver = webdriver.PhantomJS()
			self.counter = counter
		def run(self):
			pool.acquire()
			print "thread_start"
			# STUFF HAPPENS HERE
			login(self.driver, USER, PW)
			subj_count = getSubjectsForNextTerm(self.driver)
			subject_html = getCoursesForSubject(self.driver, self.counter)
			soup = BeautifulSoup(subject_html)
			classes = parseSubjectHTML(soup)
			print classes
							

			self.driver.close()
			pool.release()

	def handle(self, *args, **options):
		import time
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

		subj_count = getSubjectsForNextTerm(driver)
		found = False
		counter = 0

		for i in range(1, subj_count):
			subject_html = getCoursesForSubject(driver, i)
			soup = BeautifulSoup(subject_html)
			classes = parseSubjectHTML(soup)
					
			#print classes
			for course in classes:
				if course['Time'] != 'TBA' and course['Subj'] is not None and course['Days'] is not None:
					print course['Subj'], course['Crse']
					counter += 1
					if course['Subj'] == 'CS' and course['Crse'] == '140':
						found = True
					dept, created = Department.objects.get_or_create(name=course['Subj'])
					time = course['Time'].split('-')
					start = datetime.datetime.strptime(time[0], '%I:%M %p').time()
					end = datetime.datetime.strptime(time[1], '%I:%M %p').time()
					instructor = course['Instructor']
					if instructor is None: instructor = 'TBA'
					newCourse, created = Course.objects.get_or_create(
						name = course['Crse'], 
						days = course['Days'],
						location = course['Location'],
						credits = int(course['Cred'][0]),
						department = dept,
						desc = course['Title'],
						instructor = instructor,
						crn = course['CRN'],
						start = start,
						end = end,	
					)
					result = re.search('(A|B)? ?(\w+)', course['Sec'])
					newCourse.sec, newCourse.secNum = result.groups()
					print result.groups()
					if course['Attribute'] is not None:
						print course['Attribute']
						attributes = course['Attribute'].replace('Joined Comp and Oral Comm', 'comp').replace('Both Phys Act and Wellness', 'phys')
						attributes = attributes.split(' and ')
						for attribute in attributes:
							letter, desc = attribute.split(' - ')	
							if desc == 'comp': desc = 'Joined Comp and Oral Comm'
							if desc == 'phys': desc = 'Both Phys Act and Wellness'
							att, created = Attribute.objects.get_or_create(letter=letter, desc=desc)
							newCourse.attributes.add(att)

					newCourse.save()
		print found, counter

# login to a user
def login(driver, username, password):
	driver.get(BU_BRAIN)
	time.sleep(3)
	user = driver.find_element_by_name(LOGIN_ELEMENT)
	user.send_keys(username)
	pw = driver.find_element_by_name(PASSWORD_ELEMENT)
	pw.send_keys(password)
	pw.submit()
	print driver.title + ": " + str(username)
	# wait for cookie
	time.sleep(10)
	print username + " successfully logged in"

def parseSubjectHTML(html):
	table = html.find('table', {'class' : 'datadisplaytable'})
	tbody = ""
	classes = []
	if table:
		tbody = table.tbody
		class_count = 0
		skip_header = 0
		table_values = ['Select', 'CRN', 'Subj', 'Crse', 'Sec', 'Rst', 'Cred', 'Title',
		'Days', 'Time', 'Cap', 'Act', 'Rem', 'XL Cap', 'XL Act', 'XL Rem', 'Fee', 'Instructor', 'Date',
		'Location', 'Attribute']
		class_obj = {}
		for tr in tbody:
			if len(tr) == 43:
				if skip_header > 0:
					# start here
					table_value_count = 0
					for td in tr:
						if not td.string:
							# print "---"						
							# print "None"
							# print table_values[table_value_count]
							# print "---"
							class_obj[table_values[table_value_count]] = None
							table_value_count += 1
						elif td.string.strip():
							# print "---"
							# print td.string.strip()
							# print table_values[table_value_count]
							# print "---"
							class_obj[table_values[table_value_count]] = td.string.strip()
							table_value_count += 1
						elif not td.title:
							# print "---"
							# print "None"
							# print table_values[table_value_count]
							# print "---"
							class_obj[table_values[table_value_count]] = None
							table_value_count += 1
					classes.append(class_obj)
					class_obj = {}
					table_value_count = 0
					class_count += 1
				skip_header += 1
	return classes

def getSubjectsForNextTerm(driver):
	selectNextTerm(driver)
	# should be at subject list
	subject_dropdown = driver.find_element_by_id("subj_id")
	# minus one to discount All Subjects option
	subj_count = len(subject_dropdown.find_elements_by_tag_name('option'))
	return subj_count

# returns html for chosen subject
def getCoursesForSubject(driver, option_value):
	selectNextTerm(driver)
	
	#should be at subject list
	subject_dropdown = driver.find_element_by_id("subj_id")
	subjects = subject_dropdown.find_elements_by_tag_name('option')
	
	# stupidly doesn't deselect all
	subjects[0].click()

	subjects[option_value].click()
	section_search_button = driver.find_element_by_name("SUB_BTN")
	section_search_button.click()
	return driver.page_source

def selectNextTerm(driver):
	driver.get(SELECT_TERM)
	term_dropdown = driver.find_element_by_name("p_term")
	terms = term_dropdown.find_elements_by_tag_name('option')
	terms[1].click()
	submit = driver.find_element_by_xpath("/html/body/div[3]/form/input[2]")
	submit.click()
