from django.conf.urls import patterns, include, url

from django.contrib import admin
from view_account import RegisterVerify, RegisterConfirm, GetThirdPartyAccount, AddThirdPartyAccount, DelThirdPartyAccount, UpdateThirdPartyAccount
from view_auth import Login, Logout, ExternalAuth
from view_status import PublishStatus, PublishStatusWithFile, GetStatus, BatchGetStatus, GetUserStatusList, GetUserStatusDetail
from view_file import UploadFile, DownloadFile

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'im.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^account/register/verify/$', RegisterVerify),
    url(r'^account/register/confirm/$', RegisterConfirm),
    url(r'^account/thirdparty/show/$', GetThirdPartyAccount),
    url(r'^account/thirdparty/add/$', AddThirdPartyAccount),
    url(r'^account/thirdparty/del/$', DelThirdPartyAccount),
    url(r'^account/thirdparty/update/$', UpdateThirdPartyAccount),
    url(r'^auth/login/$', Login),
    url(r'^auth/logout/$', Logout),
    url(r'^auth/external/$', ExternalAuth),
    url(r'^status/publish/text/$', PublishStatus),
    url(r'^status/publish/withfile/$', PublishStatusWithFile),
    url(r'^status/show/id/$', GetStatus),
    url(r'^status/show/ids/$', BatchGetStatus),
    url(r'^status/show/user_timeline/list/$', GetUserStatusList),
    url(r'^status/show/user_timeline/detail/$', GetUserStatusDetail),
    url(r'^file/upload/$', UploadFile),
    url(r'^file/download/$', DownloadFile),

    #url(r'^admin/', include(admin.site.urls)),
)
