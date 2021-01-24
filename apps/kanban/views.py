from rest_framework import viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.response import Response

from .models import (Attachment, AttachmentType, Board, Card, Container,
                     KanBanUser, Label, Member, Tag)
from .serializers import (AttachmentSerializer, AttachmentTypeSerializer,
                          BoardSerializer, CardSerializer, ContainerSerializer,
                          KanBanUserSerializer, LabelSerializer,
                          MemberSerializer, NormalizedSerializer,
                          TagSerializer)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
# from django.contrib.auth.models import User


# class UserViewSet(viewsets.ViewSet):
#     """
#     Example empty viewset demonstrating the standard
#     actions that will be handled by a router class.

#     If you're using format suffixes, make sure to also include
#     the `format=None` keyword argument for each action.
#     """

#     def list(self, request):
#         pass

#     def create(self, request):
#         pass

#     def retrieve(self, request, pk=None):
#         pass

#     def update(self, request, pk=None):
#         pass

#     def partial_update(self, request, pk=None):
#         pass

#     def destroy(self, request, pk=None):
#         pass


class NormalizedViewSet(viewsets.ViewSet):
    # TODO: make pk into user identifier (auth token)
    def list(self, request, pk=None):
        entities = {
            "boards": Board.objects.all(),
            "containers": Container.objects.all(),
            "cards": Card.objects.all(),
            "members": Member.objects.all(),
            "tags": Tag.objects.all(),
            "labels": Label.objects.all(),
            "attachments": Attachment.objects.all(),
            "attachment_types": AttachmentType.objects.all(),
            "users": KanBanUser.objects.all()
        }
        serializer = NormalizedSerializer(
            entities, context={'request': request}
            )
        return Response(serializer.data)


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self, *args, **kwargs):
        return Member.objects.filter(board=self.kwargs['board_pk'])


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self, *args, **kwargs):
        return Container.objects.filter(board=self.kwargs['board_pk'])


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self, *args, **kwargs):
        return Card.objects.filter(container__board=self.kwargs['board_pk'],
                                   container=self.kwargs['container_pk'])


class AttachmentTypeViewSet(viewsets.ModelViewSet):
    queryset = AttachmentType.objects.all()
    serializer_class = AttachmentTypeSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self, *args, **kwargs):
        return Tag.objects.filter(user=self.kwargs['user_pk'])


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self, *args, **kwargs):
        return Label.objects.filter(board=self.kwargs['board_pk'])


class KanBanUserViewSet(viewsets.ModelViewSet):
    queryset = KanBanUser.objects.all()
    serializer_class = KanBanUserSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
