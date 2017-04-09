from django.db import models

# Create your models here.

class UcsCredentials(models.Model):
	"""The class represents a UCS model."""
	username = models.CharField(max_length=255, blank=False, unique=True)
	password = models.CharField(max_length=255, blank=False, unique=True)
	name = models.CharField(max_length=255, blank=False, unique=True)
	protocal = models.CharField(max_length=60, blank=False, unique=False)
	port = models.IntegerField(blank=False, unique=False)
	timeout = models.IntegerField(blank=True, unique=False)	
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		"""Return a human readable representation of the model instance"""
		return "{}".format(self.name)



class UcsSystem(models.Model):
	"""The class represents a UCS model."""
	ipAddress = models.CharField(max_length=255, blank=False, unique=True)
	subnet = models.CharField(max_length=255, blank=False, unique=True)	
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		"""Return a human readable representation of the model instance"""
		return "{}".format(self.name)