from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index, name='my_index'),
	url(r'^success$', views.success, name='my_success'),
	url(r'^process$', views.process, name='my_process'),
	url(r'^login$', views.login, name='my_login'),
	url(r'^clear$', views.clear, name='my_clear'),
]