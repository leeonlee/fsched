from django.db import models

class Department(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Attribute(models.Model):
	letter = models.CharField(max_length=10)
	desc = models.CharField(max_length=255)
	
	def __str__(self):
		return '%s - %s' %(self.letter, self.desc)
		
class Course(models.Model):
	name = models.CharField(max_length=255)
	crn = models.CharField(max_length=20)
	start = models.TimeField()
	end = models.TimeField()
	department = models.ForeignKey('Department')
	attributes = models.ManyToManyField('Attribute', null=True, blank=True)
	days = models.CharField(max_length=20)
	location = models.CharField(max_length=255)
	credits = models.IntegerField()
	instructor = models.CharField(max_length=255)
	desc = models.CharField(max_length=255)
	sec = models.CharField(max_length=255, null=True, blank=True)
	secNum = models.CharField(max_length=255, null=True, blank=True)

	def __str__(self):
		return '%s %s' %(self.department, self.name)

	class Meta:
		ordering = ['name',]
