from django.conf.urls import patterns, include, url
from django.contrib import admin
from mainapp import views
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'museum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^form/addts/$', views.TempSave),
    url(r'^form/retts/$', views.TempRet),

)
