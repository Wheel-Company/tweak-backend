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
# from django.contrib import admin
from baton.autodiscover import admin
from django.urls import path, re_path, include
from rest_framework import urls, routers, permissions
from api.models import *
from api import views
from rest_framework_jwt.views import (
    verify_jwt_token,
    refresh_jwt_token,
    ObtainJSONWebTokenView,
    BaseJSONWebTokenAPIView,
)
from .views import *
# import logging
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import GrammarCorrectionView

schema_view = get_schema_view(
    openapi.Info(
        title="Tweak API",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.tweak-english.com/terms/",
        contact=openapi.Contact(email="contact@tweak-english.com"),
        license=openapi.License(name="tweak-english License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# logger = logging.getLogger("django")


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
    path("api/", include("api.urls")),
    path("api-", include("api.urls")),
    path("", include(router.urls)),
    path("user-verify/", verify),
    path(r"api/token/", ObtainAuthTokenWithLogin.as_view()),
    path(r"api/token/verify/", verify_jwt_token),
    path(r"api/token/refresh/", refresh_jwt_token),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('grammar-correction/', GrammarCorrectionView.as_view(), name='grammar-correction'),
    path('myNote/', views.my_note, name='my_note'),
    path('last_sub_category/', views.get_last_sub_category, name='get_last_sub_category'),
    path('get_answer_stats/', views.get_answer_stats, name='get_answer_stats'),
    # path('api/', include('api.urls')),  # Replace with your app's URL patterns
]

urlpatterns += router.urls
