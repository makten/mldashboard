from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/auth/login/')
def dashboardfull(request):
	return render(request, 'dashboard/dashboardfull.html', context=None)

@login_required(login_url='/auth/login/')
def dashboard(request):
    return render(request, "dashboard.html")


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
		
