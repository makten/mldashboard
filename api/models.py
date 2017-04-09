from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

# Create your models here.

class ModelBuilder(models.Model):
	"""The class represents a ML model."""
	name = models.CharField(max_length=255, blank=False, unique=True)
	status = models.CharField(max_length=60, blank=False, unique=False)
	upload = models.FileField(upload_to='uploads/')
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		"""Return a human readable representation of the model instance"""
		return "{}".format(self.name)


class UcsCredentials(models.Model):
	"""The class represents a UCS model."""
	username = models.CharField(max_length=255, blank=False, unique=True)
	password = models.CharField(max_length=255, blank=False, unique=True)
	name = models.CharField(max_length=255, blank=False, unique=False)
	protocal = models.CharField(max_length=60, blank=False, unique=False)
	port = models.IntegerField(blank=False, unique=False)
	timeout = models.IntegerField(blank=True, unique=False)	
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		"""Return a human readable representation of the model instance"""
		return "{}".format(self.username)



class UcsSystem(models.Model):
	"""The class represents a UCS model."""
	ipAddress = models.CharField(max_length=255, blank=False, unique=True)
	subnet = models.CharField(max_length=255, blank=True, unique=False)	
	owner = models.ForeignKey('auth.User', related_name='ucssystems', on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)


	def __str__(self):
		"""Return a human readable representation of the model instance"""
		return "{}".format(self.ipAddress)



@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)