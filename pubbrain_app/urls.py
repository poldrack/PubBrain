# urls for pubbrain_app
from django.conf.urls import patterns, include, url
from pubbrain_app import views
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls))
)
urlpatterns += staticfiles_urlpatterns()