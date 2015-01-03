from django.conf.urls import patterns, url

from egebraServer import views

urlpatterns = patterns('',
	url(r'^login$', views.login_page, name='login'),
	url(r'^notebook_viewer$', views.notebook_viewer_page, name='notebook_viewer'),
	url(r'^logout$', views.logout_page, name='logout'),

	url(r'cas_request/listen', views.listen_request, name='listen_request'),
	url(r'cas_request/createSymbolicObject', views.createSymbolicObject_request, name='createSymbolicObject_request'),
	url(r'cas_request/requestComputation', views.requestComputation_request, name='requestComputation_request'),
	#url(r'cas_request/requestListOfPossibleComputations', views.list_of_possible_computations_request, name="list_of_possible_computations"),
) 