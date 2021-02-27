from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
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
    path('auth/', obtain_auth_token),
    path('normalized/', NormalizedView.as_view()),
    path('', include(router.urls))
]
