from django.conf.urls import patterns, include, url
from django.contrib import admin
from mainapp import views
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^staff/add_on_ts/$', views.TempSave),
    url(r'^staff/add_on_ts/(?P<id_number>[0-9]+)/$', views.TempSave),
    url(r'^staff/return/$', views.TempRet),
    url(r'^staff/return/(?P<id_number>[0-9]+)/$', views.TempRet),
    url(r'^staff/return/prepare/$', views.PrepareRet),
    url(r'^activities/approve(?P<offset>[0-9]+)/$', views.ApproveProject),
    #url(r'^projects/(?P<id_number>[0-9]+)/$', views.ProjectPage),
    url(r'^staff/add_on_ps/$', views.PreparePS),
    url(r'^staff/add_on_ps/(?P<id_number>[0-9]+)/$', views.AddOnPS),
    url(r'^staff/edit/(?P<pk>[0-9]+)/$', views.ObjectUpdate.as_view()),
    url(r'^staff/create/$', views.ObjectCreate.as_view()),
    url(r'^activity/(?P<id_number>[0-9]+)/$', views.ActivityPage),
    url(r'^activities/$', views.GetProject),
    url(r'^objects/$', views.ObjectList),
    url(r'^logout/$', views.logout),
    url(r'^$', views.aut),
    url(r'^staff/inventory_save/$', views.PrepareInventory),
    url(r'^staff/inventory_save/(?P<id_number>[0-9]+)/$', views.AddOnInventorySave),
    url(r'^staff/ps_to_ts/$', views.PreparePSToTS),
    url(r'^staff/ps_to_ts/(?P<id_number>[0-9]+)/$', views.FromPSToTS),
    url(r'^staff/ts_to_ps/$', views.PrepareTSToPS),
    url(r'^staff/ts_to_ps/(?P<id_number>[0-9]+)/$', views.FromTSToPS),
    url(r'^staff/send_on_ps/$', views.PrepareSendOnPS),
    url(r'^staff/send_on_ps/(?P<id_number>[0-9]+)/$', views.SendOnPS),
    url(r'^staff/writing_off/$', views.PrepareWritingOff),
    url(r'^staff/writing_off/(?P<id_number>[0-9]+)/$', views.WritingOff),
)
