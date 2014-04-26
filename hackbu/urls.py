from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackbu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include('schedulizer.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
