class ModelTestCase(TestCase):
	""" Test suit for Analyzer model """

	def setUp(self):
		""" Define test client and other vars """
		self.model_name = "base_model"
		self.model = ModelBuilder(name=self.model_name)


	def test_model_can_be_created(self):
		"""Test the model creation """
		old_count = ModelBuilder.objects.count()
		self.model.save()
		new_count = ModelBuilder.objects.count()
		self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):
	"""Test suit for the api views"""

	def setUp(self):
		"""Define the test client and oterh vars"""
		self.client = APIClient()
		self.modelbuilder_data = {'name': 'First_ML_Model'}
		self.response = self.client.post(
				reverse('create'),
				self.modelbuilder_data,
				format='json'
			)

	def test_api_can_create_a_mlmodel(self):
		"""Test the api has model creation capability"""
		self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


	def test_api_can_get_a_mlmodel(self):
		"""Test api for getting a model"""
		mlmodel = ModelBuilder.objects.get()

		response = self.client.get(
				reverse('details'),
				kwargs={'pk': mlmodel.id},
				format = 'json'
			)

	def test_api_can_update_mlmodel(self):
		"""Test api can update a ml model"""
		mlmodel = ModelBuilder.objects.get()
		change_mlmodel = {'name': 'Model_namechange'}

		res = self.client.put(
				reverse('details', kwargs={'pk': mlmodel.id}),
				change_mlmodel, format='json'
			)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertContains(res, mlmodel)


	def test_api_can_delete_mlmodel(self):
		"""Api model deletion"""
		mlmodel = ModelBuilder.objects.get()

		response = self.client.delete(
				reverse('details', kwargs={'pk': mlmodel.id}),
				format='json',
				follow=True
			)

		self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)