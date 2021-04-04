from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

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
    authentication_classes = [JWTAuthentication, SessionAuthentication]
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
            "users": KanBanUser.objects.filter(pk=request.user.pk)
        }
        serializer = NormalizedSerializer(
            entities, context={'request': request}
        )
        return Response(serializer.data)


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(created_by=self.request.user)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class KanBanUserViewSet(viewsets.ModelViewSet):
    queryset = KanBanUser.objects.all()
    serializer_class = KanBanUserSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    # the following code is left only as a helpful reminder, it CAN be removed
    # permission_classes_by_action = {'create': [AllowAny]}
    #
    # def get_permissions(self):
    #     # return permission_classes depending on action
    #     action_permissions = self.permission_classes_by_action.get(
    #         self.action, None)
    #     if action_permissions is not None:
    #         return [permission() for permission in action_permissions]
    #     else:
    #         # action is not set, return default permission_classes
    #         return [permission() for permission in self.permission_classes]


class Register(APIView):
    """View for new user registration"""
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """Create a new user with the specified username and password"""
        try:
            user = KanBanUser()
            if len(request.data['username']) == 0:
                return Response(
                    {"error": "username cannot be empty"},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            elif len(request.data['password']) == 0:
                return Response(
                    {"error": "password cannot be empty"},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            else:
                user.username = request.data['username']
                user.password = make_password(request.data['password'])
                user.save()
        except KeyError:
            # username or password weren't in the POST body
            return Response(
                {"error": "invalid register attempt"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except IntegrityError:
            # username was not valid
            return Response(
                {"error": "a user with this username already exists"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        return Response(
            {"username": user.username, "success": True},
            status=status.HTTP_201_CREATED
        )
