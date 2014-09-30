from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns("",
                       url(r'pubbrain_app/',include('pubbrain_app.urls')),
                       url(r'^admin/', include(admin.site.urls))
                       )
