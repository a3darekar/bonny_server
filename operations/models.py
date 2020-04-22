from __future__ import unicode_literals

from datetime import datetime, timedelta
import pytz
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone

from fcm_django.models import FCMDevice
from phonenumber_field.modelfields import PhoneNumberField
from .twilio_credentials import client
from .choices import *

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class HealthCare(models.Model):
	"""docstring for HealthCare"""
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=140)
	email = models.EmailField(unique=True)
	contact = PhoneNumberField(help_text="Please use the following format: <em>+91__________</em>.", null=True)
	lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
	lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)
	region = models.PositiveIntegerField(default=1)

	class Meta:
		verbose_name = 'Primary Health Care'
		verbose_name_plural = 'Primary Health Cares'

	def __str__(self):
		return self.name


class Parent(models.Model):
	"""Parent credentials for login and contact"""
	user = models.ForeignKey(User, 
		help_text="Create a new user to add as a Parent or Guardian. This would be used as login credentials.",
		 on_delete=models.CASCADE)
	email = models.EmailField('email address', unique=True)
	first_name = models.CharField('first name', max_length=30, blank=True)
	last_name = models.CharField('last name', max_length=30, blank=True)
	address = models.CharField(max_length=200)
	contact = PhoneNumberField(help_text="Please use the following format: <em>+91__________</em>.", null=True)
	unique_id = models.CharField('Aadhaar ID', max_length=13, validators=[
		RegexValidator(regex='^.{12}$', message='Length has to be 12', code='nomatch')])

	USERNAME_FIELD = 'user'
	# REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'contact']
	REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

	class Meta:
		verbose_name = 'parent'
		verbose_name_plural = 'parents'
		unique_together = ('user', 'id')

	def __str__(self):
		return self.get_full_name()

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.first_name

	def save(self, *args, **kwargs):
		if not self.pk:
			super(Parent, self).save()
			user = self.user
			user.first_name = self.first_name
			user.last_name = self.last_name
			user.email = self.email
			user.save()
		super(Parent, self).save()

	def notify(self, title, body, text_notifications=False):
		device = FCMDevice.objects.filter(device_id=self.user.username)
		if device:
			device.send_message(title, body)

		## TODO: Uncomment in deployment 
		# if text_notifications:
		# 	message = client.messages.create(
		# 		to=self.contact,
		# 		from_="+13373074483",
		# 		# TODO: Change From No.
		# 		body="%s \n %s " % (title, body)
		# 	)


class Clinitian(models.Model):
	"""Clinician access"""
	user = models.ForeignKey(User,
								help_text="Create a new user to add as a  Clinitian. This would be used as login credentials.",
								on_delete=models.SET(get_sentinel_user))
	email = models.EmailField('Email Address', unique=True)
	first_name = models.CharField('First Name', max_length=30, blank=True)
	last_name = models.CharField('Last Name', max_length=30, blank=True)
	contact = PhoneNumberField(help_text="Please use the following format: <em>+91__________</em>.", null=True)
	unique_id = models.CharField('Aadhaar ID', max_length=13, validators=[
		RegexValidator(regex='^.{12}$', message='Length has to be 12', code='nomatch')])
	HealthCare = models.ForeignKey(HealthCare, on_delete=models.PROTECT)

	USERNAME_FIELD = 'user'
	REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'contact']

	def __str__(self):
		return self.get_full_name()

	def save(self, *args, **kwargs):
		if not self.pk:
			super(Clinitian, self).save()
			user = self.user
			user.first_name = self.first_name
			user.last_name = self.last_name
			user.email = self.email
			user.save()
		super(Clinitian, self).save()

	class Meta:
		verbose_name = 'Clinician'
		verbose_name_plural = 'Clinicians'

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.first_name


class Baby(models.Model):
	"""Basic Details of baby"""
	first_name = models.CharField('First Name', max_length=30)
	last_name = models.CharField('Last Name', max_length=30)
	tag = models.CharField(max_length=20, unique=True)
	parent = models.ForeignKey(Parent, related_name="baby", on_delete=models.PROTECT)
	place_of_birth = models.CharField('Place of Birth', max_length=120)
	weight = models.PositiveIntegerField(default=10)
	blood_group = models.CharField('Blood Group', max_length=12, choices=BloodGroup)
	gender = models.CharField('Gender', max_length=10, choices=Gender)
	birth_date = models.DateTimeField('Birth Date', default=datetime.now)
	week = models.PositiveIntegerField(default=0)
	special_notes = models.CharField('Special Notes', max_length=400, help_text='Any Medical conditions such as allergies are to be mentioned here', default="NA")
	text_notifications = models.BooleanField(default=True)
	status = models.CharField('vaccination_status', max_length=20, null=True, choices=BabyStatus)

	def __str__(self):
		return self.get_full_name()

	class Meta:
		verbose_name = 'Baby'
		verbose_name_plural = 'Babies'

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.first_name

	def age_in_weeks(self):
		days = datetime.today().date().weekday() - self.birth_date.weekday()
		return days / 7

	def save(self, *args, **kwargs):
		if self.pk:
			super(Baby, self).save()
		else:
			super(Baby, self).save()
			self.status = 'ongoing'
			# Add Vaccine with the tentative date
			vaccines = dict(Vaccinations)
			for week, vaccine in vaccines.items():
				my_dict = dict(vaccine)
				for name, Name in my_dict.items():
					v = VaccineSchedule(baby=self, vaccine=name, week=week, tentative_date=self.birth_date + timedelta(week * 7), status='pending')
					v.save()
		return self

	def dosage_complete(self, *args, **kwargs):
		while True:
			vs = VaccineSchedule.objects.filter(baby=self, week=self.week).exclude(status='administered').first()
			if vs is None:
				if self.week == 0:
					self.week = 6
					continue
				if self.week == 6:
					self.week = 10
					continue
				if self.week == 10:
					self.week = 14
					continue
				if self.week == 14:
					self.week = 24
					continue
				if self.week == 24:
					self.week = 36
					continue
				if self.week == 36:
					self.status = 'completed'
					super(Baby, self).save()
					return
			else:
				break
		super(Baby, self).save()
		return self


class VaccineSchedule(models.Model):
	"""Schedule of Vaccines in to br Administered"""
	baby = models.ForeignKey(Baby, related_name="vaccine_schedules", on_delete=models.CASCADE)
	vaccine = models.CharField('Vaccine', max_length=20, choices=Vaccinations)
	week = models.PositiveIntegerField(default=0)
	tentative_date = models.DateTimeField(default=datetime.now)
	status = models.CharField('Vaccine Status', max_length=20, choices=Vaccine_Status)

	class Meta:
		unique_together = ('baby', 'vaccine')
		verbose_name = 'Vaccine Schedule'
		verbose_name_plural = 'Vaccine Schedules'

	def get_full_name(self):
		return self.baby

	def days_from_today(self):
		return (self.tentative_date - datetime.today().replace(tzinfo=pytz.UTC)).days


class Appointment(models.Model):
	"""List of Vaccines that have been Administered"""
	baby = models.ForeignKey(Baby, related_name="vaccine_records", on_delete=models.CASCADE)
	status = models.CharField(max_length=50, choices=Appointment_status, default='scheduled')
	administered_on = models.DateTimeField(default=datetime.now)
	administered_at = models.ForeignKey(HealthCare, related_name="phc", on_delete=models.PROTECT)

	class Meta:
		verbose_name = 'Appointment'
		verbose_name_plural = 'Appointments'

	def __str__(self):
		return self.baby.first_name + str(self.pk)

	def get_full_name(self):
		return self.baby

	def days_from_today(self):
		return (datetime.today().replace(tzinfo=pytz.UTC) - self.administered_on).days



Vaccine_status = dict(Vaccine_Status)
names = dict(Vaccine_names)


class VaccineRecord(models.Model):
	"""docstring for VaccineRecord"""
	appointment = models.ForeignKey(Appointment, related_name="Appointment", on_delete=models.CASCADE)
	vaccine = models.CharField('Vaccine', max_length=20, choices=Vaccinations)
	status = models.CharField('Vaccine Status', max_length=20, choices=vaccine_record_status, default='scheduled')

	class Meta:
		unique_together = ("appointment", "vaccine")
		verbose_name = 'Vaccine Record'
		verbose_name_plural = 'Vaccine Records'

	def baby(self):
		return self.appointment.baby

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		if not self.pk:
			super(VaccineRecord, self).save()
			vs = VaccineSchedule.objects.filter(baby=self.appointment.baby, vaccine=self.vaccine).update(status='scheduled')
		else:
			super(VaccineRecord, self).save()
			if self.status == 'administered':
				vaccine_schedule = VaccineSchedule.objects.filter(baby=self.appointment.baby, vaccine=self.vaccine).first()
				if vaccine_schedule.status == 'scheduled':
					vaccine_schedule.status = 'administered'
					vaccine_schedule.save()
					Notification(
						baby=self.appointment.baby,
						title="Vaccination Appointment Alert!",
						body="Vaccination Administered for vaccine:- %s" % names[self.vaccine],
						receiver=self.appointment.baby.parent,
						notif_type='success'
					).save()
					vaccine_records = VaccineRecord.objects.filter(appointment=self.appointment, status='scheduled')
					if vaccine_records.exists():
						self.appointment.status = 'partial'
					else:
						self.appointment.status = 'completed'
					self.appointment.save()
					self.appointment.baby.dosage_complete()
			elif self.status == 'scheduled':
				vaccine_schedule = VaccineSchedule.objects.filter(baby=self.appointment.baby, vaccine=self.vaccine).first()
				if vaccine_schedule.status == 'pending':
					vaccine_schedule.status = 'scheduled'
					vaccine_schedule.save()
					self.appointment.baby.dosage_complete()
				Notification(
					baby=self.appointment.baby,
					title="Vaccination Appointment Alert!",
					body="Vaccination appointment Scheduled for vaccine:- %s" % names[self.vaccine],
					receiver=self.appointment.baby.parent,
					notif_type='info'
				).save()
			else:
				vaccine_schedule = VaccineSchedule.objects.filter(baby=self.appointment.baby, vaccine=self.vaccine).first()
				if vaccine_schedule.status == 'scheduled':
					vaccine_schedule.status = 'pending'
					vaccine_schedule.save()
					self.appointment.baby.dosage_complete()
					Notification(
						baby=self.appointment.baby,
						title="Vaccination Appointment Alert!",
						body="Vaccination appointment Cancelled for vaccine:- %s" % names[self.vaccine],
						receiver=self.appointment.baby.parent,
						notif_type='error'
					).save()
					vaccine_records = VaccineRecord.objects.filter(appointment=self.appointment, status='scheduled')
					if not vaccine_records.exists():
						if self.appointment.status != 'partial':
							self.appointment.status = 'cancelled'
						else:
							self.appointment.status = 'completed'
						self.appointment.save()
		self.appointment.baby.dosage_complete()
		return self


class Notification(models.Model):
	"""
	Description: FCM notification Model
	"""
	receiver = models.ForeignKey(Parent, related_name='Parent', on_delete=models.CASCADE)
	baby = models.ForeignKey(Baby, related_name='Baby', on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	body = models.CharField(max_length=300)
	status = models.BooleanField('Status', default=False)
	notif_type = models.CharField('Notification Type', max_length=40, choices=NotificationType, default='info')
	notif_time = models.DateTimeField('Notification Time', default=datetime.now)

	class Meta:
		verbose_name = 'Notification'
		verbose_name_plural = 'Notifications'

	def save(self, *args, **kwargs):
		self.notif_time = datetime.now(pytz.timezone("Asia/Kolkata"))
		if not self.pk:
			super(Notification, self).save()
			self.receiver.notify(self.title, self.body, self.baby.text_notifications)
		super(Notification, self).save()


