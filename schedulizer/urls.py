from django.conf.urls import url
from schedulizer import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
