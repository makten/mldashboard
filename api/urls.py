from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView
from .views import DetailsView
from api import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = {
	url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^ucssystems/$', CreateView.as_view(), name='create'),
	url(r'^ucssystems/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name='details'),
	url(r'^api/users/$', views.UserProfile.as_view()),
	url(r'^api/user/(?P<pk>[0-9]+)/$', views.UserDetailsView.as_view()),
	url(r'^api/getUcsSystems/$', views.getUcsSystems),
	url(r'^api/get_blades/$', views.BladeDetails.as_view()),
	url(r'^api/get_rackunits/$', views.RackDetails.as_view()),
	url(r'^api/get_chassis/$', views.ChassisDetails.as_view()),
	url(r'^api/get_bladefaults/(?P<chs>[a-zA-Z0-9_-]+)/(?P<bld>[a-zA-Z0-9_-]+)/$', views.BladeFaults.as_view()),
	url(r'^api/getChassisStats/(?P<dn>[a-zA-Z0-9_-]+)/$', views.ChassisStats.as_view()),
	url(r'^api/get_ucsinfo/$', views.getUcsInfo, name='ucs_info'),
	url(r'^api/createUcsCredentials/$', views.createUcsCredentials, name='ucs_create_credentials'),
	url(r'^api/getUcsCredentials/$', views.getUcsCredentials, name='ucs_credentials'),
    url(r'^api/predictfaults/$', views.faultPredictor, name='fault_predictor'),


	url(r'^get-token/', obtain_auth_token),
}

urlpatterns = format_suffix_patterns(urlpatterns)