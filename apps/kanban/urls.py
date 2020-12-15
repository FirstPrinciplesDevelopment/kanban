from django.urls import include, path
from rest_framework_nested import routers

from .views import (
    KanBanUserViewSet, AttachmentTypeViewSet, AttachmentViewSet, BoardViewSet,
    CardViewSet, ContainerViewSet, LabelViewSet, MemberViewSet, TagViewSet
)


router = routers.DefaultRouter()
router.register(r'boards', BoardViewSet)
# /boards/
# /boards/{user_pk}/

boards_router = routers.NestedDefaultRouter(
    router, r'boards', lookup='board'
    )
boards_router.register(r'members', MemberViewSet)
# /boards/{board_pk}/members/
# /boards/{board_pk}/members/{member_pk}/
boards_router.register(r'containers', ContainerViewSet)
# /boards/{board_pk}/containers/
# /boards/{board_pk}/containers/{container_pk}/
boards_router.register(r'labels', LabelViewSet)
# /boards/{board_pk}/labels/
# /boards/{board_pk}/labels/{label_pk}/
boards_router.register(r'attachments', AttachmentViewSet)
# /boards/{board_pk}/attachments/
# /boards/{board_pk}/attachments/{attachment_pk}/

containers_router = routers.NestedDefaultRouter(
    boards_router, r'containers', lookup='container'
    )
containers_router.register(r'cards', CardViewSet)
# /boards/{board_pk}/containers/{container_pk}/cards/
# /boards/{board_pk}/containers/{container_pk}/cards/{card_pk}/

router.register(r'users', KanBanUserViewSet)
# /users/
# /users/{user_pk}/

user_router = routers.NestedDefaultRouter(
    router, 'users', lookup='user'
)
user_router.register(r'tags', TagViewSet)
# /users/{user_pk}/tags/
# /users/{user_pk}/tags/{tag_pk}


urlpatterns = [
    path('', include(router.urls)),
    path('', include(boards_router.urls)),
    path('', include(containers_router.urls)),
    path('', include(user_router.urls))
]
