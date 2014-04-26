from django.conf.urls import url
from schedulizer import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'addclasses', views.addClasses, name='addClasses'),
    url(r'finalschedule', views.finalSchedule, name='finalSchedule'),
    url(r'inputdars', views.inputDars, name='inputDars'),

]
