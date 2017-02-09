from django.db import models

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