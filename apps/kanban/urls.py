from django.urls import include, path
from rest_framework_nested import routers

from .views import (
    KanBanUserViewSet, AttachmentTypeViewSet, AttachmentViewSet, BoardViewSet,
    CardViewSet, ContainerViewSet, LabelViewSet, MemberViewSet, TagViewSet
)


router = routers.DefaultRouter()
router.register(r'boards', BoardViewSet)
# /boards/
# /boards/{pk}/

boards_router = routers.NestedDefaultRouter(
    router, r'boards', lookup='board'
    )
boards_router.register(r'members', MemberViewSet)
# /boards/{board_pk}/members/
# /boards/{board_pk}/members/{member_pk}/
boards_router.register(r'containers', ContainerViewSet)
# /boards/{board_pk}/containers/
# /boards/{board_pk}/containers/{container_pk}/

containers_router = routers.NestedDefaultRouter(
    boards_router, r'containers', lookup='container'
    )
containers_router.register(r'cards', CardViewSet)
# /boards/{board_pk}/containers/{container_pk}/cards/
# /boards/{board_pk}/containers/{container_pk}/cards/{card_pk}/

router.register(r'labels', LabelViewSet)
router.register(r'attachments', AttachmentViewSet)
router.register(r'attachments', AttachmentTypeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'users', KanBanUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(boards_router.urls)),
    path('', include(containers_router.urls))
]
