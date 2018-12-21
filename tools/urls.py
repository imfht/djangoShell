from django.conf.urls import url

from . import views

app_name = 'tools'

urlpatterns = [
    url(r'^test/', view=views.stream_response),
    url(r'index', view=views.index)
]
