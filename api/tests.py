from django.test import TestCase
from .models import UcsSystem
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


# Create your tests here.

class ModelTestCase(TestCase):
	""" Test suit for Analyzer model """
	def setUp(self):
		""" Define test client and other vars """
		user = User.objects.create(username="makten")
		self.ipAddress = "192.168.145.134"
		self.ucssystem = UcsSystem(ipAddress=self.ipAddress, owner=user)


	def test_model_can_be_created(self):
		"""Test the model creation """
		old_count = UcsSystem.objects.count()

		self.ucssystem.save()
		new_count = UcsSystem.objects.count()		
		self.assertNotEqual(old_count, new_count)

	def test_model_returns_readable_representation(self):
		"""Test a readable string is returned for model instance """
		self.assertEquals(str(self.ucssystem), self.ipAddress)






class ViewTestCase(TestCase):
	"""Test suit for the api views"""

	def setUp(self):
		"""Define the test client and oterh vars"""
		user = User.objects.create(username='makten')

		# Init client and force it to use auth
		self.client = APIClient()
		self.client.force_authenticate(user=user)

		# User model not seriazable so we use id/pk
		self.ucs_data = {'ipAddress': '192.168.145.134', 'subnet': '255.255.255.0', 'owner': user.id}
		
		self.response = self.client.post(
				reverse('create'),
				self.ucs_data,
				format='json'
			)



	def test_api_can_create_a_ucssystem(self):
		"""Test the api has model creation capability"""		
		self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

	def test_authorization_is_enforced(self):
		"""Test that the api has user authorization """
		new_client = APIClient()
		res = new_client.get('/ucssystems/', kwargs={'pk': 1}, format="json")	
		print(res.status_code)	
		# self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


	def test_api_can_get_a_ucssystem(self):
		"""Test api for getting a model"""
		ucssystem = UcsSystem.objects.get(id=3)	

		response = self.client.get(
				'/ucssystems/',
				kwargs={'pk': ucssystem.id},				
				format = 'json'
			)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertContains(response, ucssystem)



	def test_api_can_update_ucssystem(self):
		"""Test api can update a ml model"""
		ucssystem = UcsSystem.objects.get()
		change_ucssystem = {'ipAddress': '192.168.145.124'}

		res = self.client.put(
				reverse('details', kwargs={'pk': ucssystem.id}),
				change_ucssystem, format='json'
			)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		


	def test_api_can_delete_ucssystem(self):
		"""Api model deletion"""
		ucssystem = UcsSystem.objects.get()

		response = self.client.delete(
				reverse('details', kwargs={'pk': ucssystem.id}),
				format='json',
				follow=True
			)

		self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
