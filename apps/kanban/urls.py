from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    # TokenVerifyView
)
from rest_framework.routers import DefaultRouter

from .views import (AttachmentViewSet, BoardViewSet, CardViewSet,
                    ContainerViewSet, KanBanUserViewSet, LabelViewSet,
                    MemberViewSet, NormalizedView, TagViewSet)

router = DefaultRouter()

router.register(r'boards', BoardViewSet)
router.register(r'containers', ContainerViewSet)
router.register(r'cards', CardViewSet)
router.register(r'labels', LabelViewSet)
router.register(r'attachments', AttachmentViewSet)
router.register(r'members', MemberViewSet)
router.register(r'users', KanBanUserViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('normalized/', NormalizedView.as_view()),
    path('', include(router.urls))
]
