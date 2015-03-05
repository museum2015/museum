from django.conf.urls import patterns, include, url
from django.contrib import admin
from mainapp import views
admin.autodiscover()


urlpatterns = patterns('',
    # Examples
    # url(r'^$', 'museum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^form/add_on_ts$', views.TempSave),
    url(r'^form/ret_from_ts$', views.TempRet),
    url(r'^projects/$', views.GetProjects)
)
