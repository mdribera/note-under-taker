from django.conf.urls import url
from . import views

app_name = 'notes'
urlpatterns = [
	# ex: /notes
  url(r'^$', views.index, name='index'),
  # ex: /notes/2
  url(r'^(?P<note_id>[0-9]+)/$', views.detail, name='detail'),
]