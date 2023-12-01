from django.urls import path
from .views import  getRouter , UserRegister , UserList , UserDetails , LoginAPI , UserSoftDelet , UserEdit,UserSearch,UserAdd,UserImage
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', getRouter),

    path('token/',LoginAPI.as_view() , name='user_login'),
   

    path('register',UserRegister.as_view(),name='user_register'),
    path('userlist',UserList.as_view(),name="user_list"),
    path('adduser',UserAdd.as_view(),name="user_add"),
    path('userdetails/<int:id>',UserDetails.as_view(),name="user_detailsw"),
    path('userdelete/<int:id>',UserSoftDelet.as_view(),name="user_delete"),
    path('edituser/<int:id>',UserEdit.as_view(),name="user_edit"),
    path('usersearch/<str:user>', UserSearch.as_view(),name='user_search'),
    path('imageupload', UserImage.as_view(),name='imageupload')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)