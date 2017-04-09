from django.conf.urls import url
from mainapp import views


urlpatterns = [
	url(r'^$', views.dashboardfull, name='home'),
	url(r'^dashboard/', views.dashboard, name='dashboard'),
	url(r'^data/', views.TestDataView.as_view(), name='data'),
	url(r'^dashboardfull/', views.DashboardFullView.as_view(), name='dashboardfull'),
]