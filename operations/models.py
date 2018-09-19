# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from .choices import *
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

class HealthCare(models.Model):
	"""docstring for HealthCare Centre"""
	name 		= models.CharField(max_length = 50)
	address 	= models.CharField(max_length = 140)
	email 		= models.EmailField(('email address'), unique = True)
	contact 	= PhoneNumberField(help_text="Please use the following format: <em>+91__________</em>.")

	class Meta:
		verbose_name 		= ('Primary HealthCare Centre')
		verbose_name_plural = ('Primary HealthCare Centres')

	def __str__(self):
		return self.name


class Parent(models.Model):
	"""Parent credentials for login and contact"""
	user 			= models.OneToOneField(User, help_text="Create a new user to add as a Parent or Guardian. This would be used as login credentials.")
	email 			= models.EmailField(('email address'), unique=True)
	first_name 		= models.CharField(('first name'), max_length=30, blank=True)
	last_name 		= models.CharField(('last name'), max_length=30, blank=True)
	address 		= models.CharField(max_length=200)
	contact 		= PhoneNumberField(help_text="Please use the following format: <em>+91__________</em>.")
	unique_id		= models.CharField(('Aadhaar ID'), max_length = 12, validators=[RegexValidator(regex='^.{12}$', message='Length has to be 12', code='nomatch')])

	USERNAME_FIELD = 'user'
	REQUIRED_FIELDS = ['email', 'first_name', 'last_name', contact]

	class Meta:
		verbose_name 		= ('parent')
		verbose_name_plural = ('parents')

	def __str__(self):
		return self.get_full_name()

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.first_name



class Clinitian(models.Model):
	"""Clinitian access"""
	user 				= models.OneToOneField(User, help_text="Create a new user to add as a Clinitian. This would be used as login credentials.")
	first_name 			= models.CharField(('first name'), max_length=30, blank=True)
	last_name 			= models.CharField(('last name'), max_length=30, blank=True)
	email 				= models.EmailField(('email address'), unique=True)
	contact 			= PhoneNumberField(help_text="Please use the following format: <em>+91__________</em>.")
	unique_id			= models.CharField(('Aadhaar ID'), max_length = 12, validators=[RegexValidator(regex='^.{12}$', message='Length has to be 12', code='nomatch')])
	health_care_centre 	= models.ForeignKey(HealthCare)

	USERNAME_FIELD = 'user'
	REQUIRED_FIELDS = ['email', 'first_name', 'last_name', contact]

	def __str__(self):
		return self.get_full_name()

	def save(self):
		super(Clinitian, self).save()

	class Meta:
		verbose_name 		= ('Clinitian')
		verbose_name_plural = ('Clinitians')

	def get_full_name(self):

		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()
	
	def get_short_name(self):
		return self.first_name


class Baby(models.Model):
	"""Basic Details of baby"""
	parent 				= models.ForeignKey(Parent, related_name = "baby")
	first_name 			= models.CharField(('first name'), max_length=30)
	last_name 			= models.CharField(('last name'), max_length=30)
	tag 				= models.CharField(max_length = 20, unique = True)
	place_of_birth 		= models.CharField(('Place of Birth'),max_length = 80, unique = True)
	weight 				= models.PositiveIntegerField(default = 5)
	blood_group			= models.CharField('Blood Group', max_length = 10, choices = Blood_Group)
	gender				= models.CharField('Gender', max_length = 10, choices = gender)
	birth_date			= models.DateTimeField(('Birth Date'),default=datetime.now)
	special_notes		= models.CharField(('Special Notes'), max_length = 400, help_text = 'Any Medical details such as allergies, genetic conditions are to be mentioned here')
	text_notifications 	= models.BooleanField(default = True)

	def __str__(self):
		return self.get_full_name()

	class Meta:
		verbose_name 		= ('baby')
		verbose_name_plural = ('babies')

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()
	
	def get_short_name(self):
		return self.first_name

	def age_in_weeks(self):
		days =  datetime.today().date().weekday() - self.birth_date.weekday() 
		return days/7


	def save(self, *args, **kwargs):
		if self.pk:
			super(Baby, self).save()	
		else:
			super(Baby, self).save()
			parent = self.parent
	
		# Add Vaccine with the probable Dosage date
			Vaccine_list = dict(Vaccines)
			for week,vaccine in Vaccine_list.items():
				my_dict = dict(vaccine)
				for name, Name in my_dict.items():
					v = VaccineSchedule(baby = self, vaccine = name, week = week, administered_on = self.birth_date+timedelta(week*7), status = 'pending')
					v.save()
		return self


class VaccineRecord(models.Model):
	"""List of VaccineSchedules in to br Administered"""
	baby 				= models.ForeignKey(Baby, related_name = "vaccine_records")
	vaccine 			= models.CharField('Vaccine', max_length=20, choices=Vaccines)
	administered_on 	= models.DateField(default = datetime.now)
	administered_at		= models.ForeignKey(HealthCare)

	class Meta:
		verbose_name 		= ('Vaccination Record')
		verbose_name_plural = ('Vaccination Records')

class VaccineSchedule(models.Model):
	"""List of VaccineSchedules in to br Administered"""
	baby 						= models.ForeignKey(Baby, related_name = "vaccine_schedule")
	vaccine 					= models.CharField('Vaccine', max_length=20, choices=Vaccines)
	tentative_vaccination_date 	= models.DateField(default = datetime.now)
	status		 				= models.CharField('Vaccine Status', max_length=20, choices=Vaccine_status)
	week						= models.PositiveIntegerField(default = 0)

	class Meta:
		verbose_name 		= ('Vaccination Schedule')
		verbose_name_plural = ('Vaccination Schedules')

	# def days_from_today(self):
	# 	return self.tentative_vaccination_date - datetime.today().date()