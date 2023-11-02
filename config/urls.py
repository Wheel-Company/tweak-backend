# Third-party imports
from baton.autodiscover import admin
from rest_framework import urls, routers, permissions
from rest_framework_jwt.views import (
    verify_jwt_token,
    refresh_jwt_token,
    ObtainJSONWebTokenView,
    BaseJSONWebTokenAPIView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Django imports
from django.urls import path, re_path, include

# Application imports
from api import views
from config.serializers import GrammarCorrectionSerializer
from config.views import *
from config.views import health_check
from django.urls import path, re_path, include
from rest_framework import urls, routers, permissions
from rest_framework_jwt.views import (
    verify_jwt_token,
    refresh_jwt_token,
    ObtainJSONWebTokenView,
    BaseJSONWebTokenAPIView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api import views
from config.views import *

# Set up schema view for API documentation
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

class ObtainAuthTokenWithLogin(BaseJSONWebTokenAPIView):
    def post(self, request):
        result = super().post(request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=request.data["username"])
            update_last_login(None, user)
            if "type" in request.data:
                refresh_token = User.objects.make_random_password(length=20)
                result.data["refresh_token"] = refresh_token
        return result

router = routers.DefaultRouter()
# router.register(r"api-user", UserViewSet)

urlpatterns = [
    path('health_check/', health_check, name='health_check'),
    path("admin/", admin.site.urls),
    path("baton/", include("baton.urls")),
    path("api-", include("api.urls")),
    path("", include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('grammar-correction/', views.grammar_correction_veiw, name='grammar-correction'),
    path('myNote/', views.my_note, name='my_note'),
    path('last_sub_category/<int:user_id>/', views.get_last_sub_category, name='get_last_sub_category'),
    path('get_answer_stats/<int:user_id>/', views.get_answer_stats, name='get_answer_stats'),
    path('get_sns_user/<str:sns_id>/', views.get_sns_user, name='get_sns_user'),
    path('create_sns_user/', views.create_sns_user, name='get_sns_user'),
]

urlpatterns += router.urls