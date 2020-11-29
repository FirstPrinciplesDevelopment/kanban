from django.urls import include, path
from rest_framework import routers

from .views import (AttachmentTypeViewSet, AttachmentViewSet, BoardViewSet,
                    CardViewSet, ContainerViewSet, LabelViewSet, TagViewSet)

app_name = 'kanban'

router = routers.DefaultRouter()
router.register(r'boards', BoardViewSet)
router.register(r'containers', ContainerViewSet)
router.register(r'cards', CardViewSet)
router.register(r'attachments', AttachmentViewSet)
router.register(r'attachments', AttachmentTypeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'labels', LabelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
