from rest_framework import viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Attachment, Board, Card, Container, KanBanUser, Label,
                     Member, Tag)
from .serializers import (AttachmentSerializer, BoardSerializer,
                          CardSerializer, ContainerSerializer,
                          KanBanUserSerializer, LabelSerializer,
                          MemberSerializer, NormalizedSerializer,
                          TagSerializer)


# TODO: be more granular with user level permissions here
# TODO: implement user level permissions across all views/models
class NormalizedView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entities = {
            "boards": Board.objects.filter(created_by=request.user),
            "containers": Container.objects.filter(created_by=request.user),
            "cards": Card.objects.filter(created_by=request.user),
            "members": Member.objects.filter(user=request.user),
            "tags": Tag.objects.filter(user=request.user),
            "labels": Label.objects.all(),
            "attachments": Attachment.objects.filter(uploaded_by=request.user),
            "users": KanBanUser.objects.get(pk=request.user.pk)
        }
        serializer = NormalizedSerializer(
            entities, context={'request': request}
        )
        return Response(serializer.data)


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class KanBanUserViewSet(viewsets.ModelViewSet):
    queryset = KanBanUser.objects.all()
    serializer_class = KanBanUserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
