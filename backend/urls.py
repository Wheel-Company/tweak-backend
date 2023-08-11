"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import urls, routers
from api.models import *
from api import views
from rest_framework_jwt.views import (
    verify_jwt_token,
    refresh_jwt_token,
    ObtainJSONWebTokenView,
    BaseJSONWebTokenAPIView,
)
from .views import *
import logging

logger = logging.getLogger("django")


class ObtainAuthTokenWithLogin(BaseJSONWebTokenAPIView):
    def post(self, request):
        result = super().post(request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=request.data["username"])
            update_last_login(None, user)
            # authenticate(request, username=user.username, password=user.password)
            # login(request,user=user)
            if "type" in request.data:
                refresh_token = User.objects.make_random_password(length=20)
                result.data["refresh_token"] = refresh_token
        logger.error("login_user : %s" % user.pk)
        return result


router = routers.DefaultRouter()

router.register(r"api-user", UserViewSet)
# router.register(r'api-user', UserViewSet)
# router.register(r'user', views.getViewSet(models.User))
urlpatterns = [
    path("admin/", admin.site.urls),
    path("baton/", include("baton.urls")),
    path("api-auth/", include(urls)),
    path("api-", include("api.urls")),
    path("", include(router.urls)),
    path("send_validation_mail/", send_validation_mail),
    path("send_change_mail/", send_change_mail),
    path("user-verify/", verify),
    # path('accountItem',views.getViewSet(models.AccountItems).as_view({'get': 'list'})),
    # path('accountItem/<int:pk>', views.getViewSet(models.AccountItems).as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
    # path(r'api-user/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'patch':'update' , 'delete' : 'destroy' })),
    # path(r'api-user', UserViewSet.as_view({'get': 'list' , 'post': 'create'})),
    # path(r'api-users/', UserViewSet.as_view({'get': 'list'})),
    # path(r'api-auth-user/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    # path(r'api-auth-user/<str:username>/', UserViewSet.as_view({'get': 'retrieve'})),
    path(r"api/token/", ObtainAuthTokenWithLogin.as_view()),
    path(r"api/token/verify/", verify_jwt_token),
    path(r"api/token/refresh/", refresh_jwt_token),
    path(
        "activate/<str:uid64>/<str:token>/", activate
    ),  # active user -> create 시에 발송된 email
    path("send_reset_mail", send_reset_mail),  # send reset email
    path("reset/<str:uid64>/<str:token>/", reset),  # reset password
    path("active/<int:pk>/", is_active),  # check active user
    path("edit", edit),
    path("api/bgm/popular", views.getBgmOrderByPopularity),
    path("api/curation/popular", views.getcurationOrderByPopularity),
]

urlpatterns += router.urls
