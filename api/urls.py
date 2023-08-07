from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ConnectedAccountViewSet, CategoryViewSet, DifficultyViewSet,QuestionViewSet, AnswerViewSet, SubscriptionViewSet, CouponViewSet, NoteViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'connected_accounts', ConnectedAccountViewSet)
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'difficulty', DifficultyViewSet)
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'coupons', CouponViewSet)
router.register(r'notes', NoteViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/', include(router.urls)),
]