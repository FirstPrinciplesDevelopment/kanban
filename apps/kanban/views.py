from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from .models import (
    Attachment, AttachmentType, Board, Card, Container,
    KanBanUser, Label, Member, Tag
    )

from .serializers import (
    AttachmentSerializer, AttachmentTypeSerializer, BoardSerializer,
    CardSerializer, ContainerSerializer, KanBanUserSerializer,
    LabelSerializer, MemberSerializer, TagSerializer
    )

# from rest_framework.views import APIView
from rest_framework.response import Response
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


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    # def list(self, request):
    #     queryset = Board.objects.filter()
    #     serializer = BoardSerializer(queryset, many=True,
    #                                  context={'request': request})
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = Board.objects.filter()
    #     board = get_object_or_404(queryset, pk=pk)
    #     serializer = BoardSerializer(board, context={'request': request})
    #     return Response(serializer.data)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_queryset(self, *args, **kwargs):
        return Member.objects.filter(board=self.kwargs['board_pk'])

    # def list(self, request, board_pk=None):
    #     queryset = Member.objects.filter(board=board_pk)
    #     serializer = MemberSerializer(queryset, many=True,
    #                                   context={'request': request})
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None, board_pk=None):
    #     queryset = Member.objects.filter(pk=pk, board=board_pk)
    #     member = get_object_or_404(queryset, pk=pk)
    #     serializer = MemberSerializer(member, context={'request': request})
    #     return Response(serializer.data)


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

    def get_queryset(self, *args, **kwargs):
        return Container.objects.filter(board=self.kwargs['board_pk'])

    # def list(self, request, board_pk=None):
    #     queryset = Container.objects.filter(board=board_pk)
    #     serializer = ContainerSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None, board_pk=None):
    #     queryset = Container.objects.filter(pk=pk, board=board_pk)
    #     container = get_object_or_404(queryset, pk=pk)
    #     serializer = ContainerSerializer(container)
    #     return Response(serializer.data)


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self, *args, **kwargs):
        return Card.objects.filter(board=self.kwargs['board_pk'],
                                   container=self.kwargs['container_pk'])

    def list(self, request, board_pk=None, container_pk=None):
        queryset = Card.objects.filter(board=board_pk, container=container_pk)
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, board_pk=None, container_pk=None):
        queryset = Card.objects.filter(board=board_pk, container=container_pk)
        card = get_object_or_404(queryset, board=board_pk,
                                 container=container_pk, pk=pk)
        serializer = CardSerializer(card)
        return Response(serializer.data)


class AttachmentTypeViewSet(viewsets.ModelViewSet):
    queryset = AttachmentType.objects.all()
    serializer_class = AttachmentTypeSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class KanBanUserViewSet(viewsets.ModelViewSet):
    queryset = KanBanUser.objects.all()
    serializer_class = KanBanUserSerializer
