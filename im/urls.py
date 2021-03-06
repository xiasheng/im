from django.conf.urls import patterns, include, url

from django.contrib import admin
from view_account import RegisterVerify, RegisterConfirm, GetThirdPartyAccount, AddThirdPartyAccount, DelThirdPartyAccount, UpdateThirdPartyAccount, ResetPassword
from view_auth import Login, Logout, ExternalAuth
from view_status import PublishStatus, PublishStatusWithFile, GetStatus, BatchGetStatus, GetUserStatusList, GetUserStatusDetail
from view_file import UploadFile, DownloadFile
from view_comment import AddComment, DelCommentById, GetCommentById, BatchGetCommentByIds, GetCommentDetailByStatusId
from view_place import GetNearByUserList, GetNearByStatusList, GetNearByPhotoList, GetNearByStatusDetail
from view_profile import AddProfile, DelProfile, UpdateProfile, ShowProfile, UploadProfileImage, AddProfilePhoto, DelProfilePhoto, ShowProfilePhoto
from view_friendship import AddFriend, DelFriend, ShowFriends, ShowFans, SearchFriends

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'im.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^account/register/verify/$', RegisterVerify),
    url(r'^account/register/confirm/$', RegisterConfirm),
    url(r'^account/resetpassword/$', ResetPassword),
    url(r'^account/thirdparty/show/$', GetThirdPartyAccount),
    url(r'^account/thirdparty/add/$', AddThirdPartyAccount),
    url(r'^account/thirdparty/del/$', DelThirdPartyAccount),
    url(r'^account/thirdparty/update/$', UpdateThirdPartyAccount),
    
    url(r'^auth/login/$', Login),
    url(r'^auth/logout/$', Logout),
    url(r'^auth/external/$', ExternalAuth),
    
    url(r'^profile/add/$', AddProfile),
    url(r'^profile/del/$', DelProfile),
    url(r'^profile/update/$', UpdateProfile),
    url(r'^profile/show/$', ShowProfile),
    url(r'^profile/image/upload/$', UploadProfileImage),
    url(r'^profile/photo/add/$', AddProfilePhoto),
    url(r'^profile/photo/del/$', DelProfilePhoto),
    url(r'^profile/photo/show/$', ShowProfilePhoto),

    url(r'^status/publish/text/$', PublishStatus),
    url(r'^status/publish/withfile/$', PublishStatusWithFile),
    url(r'^status/show/id/$', GetStatus),
    url(r'^status/show/ids/$', BatchGetStatus),
    url(r'^status/show/user_timeline/list/$', GetUserStatusList),
    url(r'^status/show/user_timeline/detail/$', GetUserStatusDetail),

    url(r'^comment/add/$', AddComment),
    url(r'^comment/del/$', DelCommentById),
    url(r'^comment/show/$', GetCommentDetailByStatusId),
    #url(r'^comment/show/cid/$', GetCommentById),
    #url(r'^comment/show/sid/$', GetCommentListByStatusId),
    #url(r'^comment/show_batch/$', BatchGetCommentByIds),

    url(r'^place/nearby/user/list/$', GetNearByUserList),
    url(r'^place/nearby/status/list/$', GetNearByStatusList),
    url(r'^place/nearby/status/detail/$', GetNearByStatusDetail),
    url(r'^place/nearby/photo/list/$', GetNearByPhotoList),

    url(r'^file/upload/$', UploadFile),
    url(r'^file/download/$', DownloadFile),

    url(r'^friends/add/$', AddFriend),
    url(r'^friends/del/$', DelFriend),
    url(r'^friends/show/$', ShowFriends),
    url(r'^fans/show/$', ShowFans),
    url(r'^friends/search/$', SearchFriends),

    #url(r'^admin/', include(admin.site.urls)),
)
