from django.urls import include, path
from rest_framework import routers

from .views import (
    KanBanUserViewSet, AttachmentTypeViewSet, AttachmentViewSet, BoardViewSet,
    CardViewSet, ContainerViewSet, LabelViewSet, MemberViewSet, TagViewSet
)


router = routers.DefaultRouter()
router.register(r'boards', BoardViewSet)
router.register(r'members', MemberViewSet)
router.register(r'containers', ContainerViewSet)
router.register(r'cards', CardViewSet)
router.register(r'attachments', AttachmentViewSet)
router.register(r'attachments', AttachmentTypeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'labels', LabelViewSet)
router.register(r'users', KanBanUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
