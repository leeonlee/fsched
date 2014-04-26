from django.core.management.base import BaseCommand, CommandError
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

USER = os.environ.get('FSCHED_USER')
PW = os.environ.get('FSCHED_PW')
BU_BRAIN = "https://ssb.cc.binghamton.edu/banner/twbkwbis.P_WWWLogin"
SELECT_TERM = "https://ssb.cc.binghamton.edu/banner/hwskzdar.P_CheckAudit"
LOGIN_ELEMENT = "sid"
PASSWORD_ELEMENT = "PIN"
cookies = []
words = []
pointList = []

class Command(BaseCommand):
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
