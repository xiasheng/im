from django.conf.urls import patterns, include, url

from django.contrib import admin
from view_account import RegisterVerify, RegisterConfirm
from view_auth import Login, Logout, ExternalAuth
from view_status import PublishStatus, GetStatus

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'im.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^account/register/verify/$', RegisterVerify),
    url(r'^account/register/confirm/$', RegisterConfirm),
    url(r'^auth/login/$', Login),
    url(r'^auth/logout/$', Logout),
    url(r'^auth/external/$', ExternalAuth),
    url(r'^status/publish_text/$', PublishStatus),
    url(r'^status/show/id/$', GetStatus),
    #url(r'^admin/', include(admin.site.urls)),
)
