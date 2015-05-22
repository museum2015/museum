from django.conf.urls import patterns, include, url
from django.contrib import admin
from mainapp import views
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^staff/add_on_ts/$', views.TempSave),
    url(r'^staff/add_on_ts/(?P<id_number>[0-9]+)/$', views.TempSave),
    url(r'^staff/return/$', views.TempRet),
    url(r'^staff/return/(?P<id_number>[0-9]+)/$', views.TempRet),
    url(r'^activities/approve(?P<offset>[0-9]+)/$', views.ApproveProject),
    url(r'^activities/reject(?P<offset>[0-9]+)/$', views.RejectProject),
    #url(r'^projects/(?P<id_number>[0-9]+)/$', views.ProjectPage),
    url(r'^staff/add_on_ps/(?P<id_number>[0-9]+)/$', views.AddOnPS),
    url(r'^staff/delete/(?P<pk>[0-9]+)/$', views.ObjectDelete.as_view()),
    url(r'^activity/(?P<id_number>[0-9]+)/$', views.ActivityPage),
    url(r'^activities/$', views.GetProject),
    url(r'^objects/$', views.ObjectList),
    url(r'^logout/$', views.logout),
    url(r'^$', views.aut),
    url(r'^staff/inventory_save/(?P<id_number>[0-9]+)/$', views.AddOnInventorySave),
    url(r'^staff/spec_inventory_save/(?P<id_number>[0-9]+)/$', views.AddOnSpecInventorySave),
    url(r'^staff/passport/(?P<id_number>[0-9]+)/$', views.Passport),
    url(r'^staff/ps_to_ts/(?P<id_number>[0-9]+)/$', views.FromPSToTS),
    url(r'^staff/ts_to_ps/(?P<id_number>[0-9]+)/$', views.FromTSToPS),
    url(r'^staff/send_on_ps/(?P<id_number>[0-9]+)/$', views.SendOnPS),
    url(r'^staff/writing_off/(?P<id_number>[0-9]+)/$', views.WritingOff),
    url(r'^pdf/(?P<id_number>[0-9]+)/', views.MyPDFView.as_view()),
    url(r'^xml/$', views.EditXML),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
