from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView
from .views import DetailsView
from api import views


urlpatterns = {
	url(r'^mlmodel/$', CreateView.as_view(), name='create'),
	url(r'^mlmodel/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name='details'),
	url(r'^api/users/$', views.UserProfile.as_view()),
	url(r'^api/user/(?P<pk>[0-9]+)/$', views.UserDetailsView.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)