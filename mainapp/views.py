from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView

# Create your views here.

class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html', context=None)


class DashboardPageView(TemplateView):	
	template_name = "dashboard.html"


class TestDataView(TemplateView):

	def get(self, request, **kwargs):

		context = {
			'data': [
				{
                    'name': 'Celeb 1',
                    'worth': '3567892'
                },
                {
                    'name': 'Celeb 2',
                    'worth': '23000000'
                },
                {
                    'name': 'Celeb 3',
                    'worth': '1000007'
                },
                {
                    'name': 'Celeb 4',
                    'worth': '456789'
                }
			]
		}
		return render(request, 'testdata.html', context)


class DashboardFullView(TemplateView):

    def get(self, request, **kwargs):
        
        return render(request, 'dashboard/dashboardfull.html', context=None)
		
