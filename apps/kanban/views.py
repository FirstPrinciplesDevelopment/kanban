from rest_framework import viewsets

from .models import (
    Attachment, AttachmentType, Board, Card, Container,
    KanBanUser, Label, Member, Tag
    )

from .serializers import (
    AttachmentSerializer, AttachmentTypeSerializer, BoardSerializer,
    CardSerializer, ContainerSerializer, KanBanUserSerializer,
    LabelSerializer, MemberSerializer, TagSerializer
    )


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


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
