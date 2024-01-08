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
from api.views import cancel_saved_questions, user_completion_status,bookmark_all
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
    
# class CustomRouter(routers.DefaultRouter):
#     def get_default_basename(self, viewset):
#         if viewset == WritingContentViewSet:
#             return None
#         return super().get_default_basename(viewset)

# router = CustomRouter()
# router.register(r'writing-content', WritingContentViewSet, basename='writingcontent')
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
    path('grammar-correction/', views.grammar_correction_view, name='grammar-correction'),
    path('recent_learning/<int:user_id>/', views.get_recent_learning, name='recent_learning'),
    path('answer_stats/<int:user_id>/', views.get_answer_stats, name='answer_stats'),
    path('sns_user/<str:sns_id>/', views.get_sns_user, name='sns_user'),
    path('sns_user/', views.create_sns_user, name='sns_user'),
    # path('api-writing/content/', views.api_writing_content, name='api-writing-content'),
    # path('api-user-note/<int:user_id>/', views.get_note_list, name='api-user-note'),
     # Include your new views
    path('cancel_saved_questions/', cancel_saved_questions, name='cancel_saved_questions'),
    path('user_completion_status/', user_completion_status, name='user_completion_status'),
    path('bookmark_all/', bookmark_all, name='bookmark_all'),
    
    
]

urlpatterns += router.urls