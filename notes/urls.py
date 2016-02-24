from django.conf.urls import url
from . import views

app_name = 'notes'
urlpatterns = [
	# ex: /notes
  url(r'^$', views.IndexView.as_view(), name='index'),
	# ex: /notes/label/journal
  url(r'^label/([\w-]+)/$', views.LabelView.as_view(), name='label'),
  # ex: /notes/2
  url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]
