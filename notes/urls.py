from django.conf.urls import url
from . import views

app_name = 'notes'
urlpatterns = [
    # ex: /notes or /notes?label=journal
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /notes/2
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]
