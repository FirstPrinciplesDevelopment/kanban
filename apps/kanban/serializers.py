from rest_framework.serializers import HyperlinkedModelSerializer, Serializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from .models import (Attachment, Board, Card, Container, KanBanUser, Label,
                     Member, Tag)

# constants
AUDITABLE_FIELDS = [
    'created_by', 'created_time', 'changed_by', 'changed_time',
    'archived', 'archived_by', 'archived_time'
]


class BoardSerializer(HyperlinkedModelSerializer):
    """Serialize a Board object."""
    containers = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        parent_lookup_kwargs={'board_pk': 'board__pk'},
        view_name='container-detail',
        queryset=Container.objects.all()
    )
    labels = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        parent_lookup_kwargs={'board_pk': 'board__pk'},
        view_name='label-detail',
        queryset=Label.objects.all()
    )
    attachments = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        parent_lookup_kwargs={'board_pk': 'board__pk'},
        view_name='attachment-detail',
        queryset=Attachment.objects.all()
    )
    members = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        parent_lookup_kwargs={'board_pk': 'board__pk'},
        view_name='member-detail',
        queryset=Member.objects.all()
    )

    class Meta:
        model = Board
        fields = [
            'url', 'id', 'name', 'slug', 'position',
            'containers', 'members', 'labels', 'attachments'
        ] + AUDITABLE_FIELDS


class MemberSerializer(NestedHyperlinkedModelSerializer):
    """Serialize a Member object."""
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

    class Meta:
        model = Member
        fields = ['url', 'id', 'board', 'user', 'starred', 'position']


class ContainerSerializer(NestedHyperlinkedModelSerializer):
    """Serialize a Container object."""
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

    cards = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        parent_lookup_kwargs={
            'board_pk': 'container__board__pk', 'container_pk': 'container__pk'
        },
        view_name='card-detail',
        queryset=Card.objects.all()
    )
    labels = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        parent_lookup_kwargs={'board_pk': 'board__pk'},
        view_name='label-detail',
        queryset=Label.objects.all()
    )
    tags = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        parent_lookup_kwargs={'user_pk': 'user__pk'},
        view_name='tag-detail',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Container
        fields = [
            'url', 'id', 'board', 'name', 'slug',
            'position', 'cards', 'labels', 'tags'
        ] + AUDITABLE_FIELDS

    def create(self, validated_data):
        container = Container.objects.create(**validated_data)
        return container


class CardSerializer(NestedHyperlinkedModelSerializer):
    """Serialize a Card object."""
    parent_lookup_kwargs = {
        'board_pk': 'container__board__pk', 'container_pk': 'container__pk'
    }

    container = NestedHyperlinkedRelatedField(
        required=True,
        parent_lookup_kwargs={'board_pk': 'board__pk'},
        view_name='container-detail',
        queryset=Container.objects.all()
    )
    labels = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        parent_lookup_kwargs={'board_pk': 'board__pk'},
        view_name='label-detail',
        queryset=Label.objects.all()
    )
    tags = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        parent_lookup_kwargs={'user_pk': 'user__pk'},
        view_name='tag-detail',
        queryset=Tag.objects.all()
    )
    attachments = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        parent_lookup_kwargs={'board_pk': 'board__pk'},
        view_name='attachment-detail',
        queryset=Attachment.objects.all()
    )
    assigned_users = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        parent_lookup_kwargs={'board_pk': 'board__pk'},
        view_name='member-detail',
        queryset=Member.objects.all()
    )

    class Meta:
        model = Card
        fields = [
            'url', 'id', 'container', 'name', 'slug', 'content',
            'start_time', 'end_time', 'complexity', 'hours', 'position',
            'assigned_users', 'labels', 'tags', 'attachments'
        ] + AUDITABLE_FIELDS

    def create(self, validated_data):
        card = Card.objects.create(**validated_data)
        return card


class TagSerializer(NestedHyperlinkedModelSerializer):
    """Serialize a Tag object."""
    parent_lookup_kwargs = {'user_pk': 'user__pk'}

    class Meta:
        model = Tag
        fields = ['url', 'id', 'user', 'name', 'color']


class LabelSerializer(NestedHyperlinkedModelSerializer):
    """Serialize a Label object."""
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

    class Meta:
        model = Label
        fields = ['url', 'id', 'board', 'name', 'color']


class AttachmentSerializer(NestedHyperlinkedModelSerializer):
    """Serialize an Attachment object."""
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

    class Meta:
        model = Attachment
        fields = [
            'url', 'id', 'board', 'name', 'file_path',
            'uploaded_by', 'uploaded_time'
        ]


class KanBanUserSerializer(HyperlinkedModelSerializer):
    """Serialize a KanBanUser object."""
    tags = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='tag-detail',
        parent_lookup_kwargs={'user_pk': 'user__pk'},
        queryset=Tag.objects.all()
    )
    memberships = NestedHyperlinkedRelatedField(
        many=True,
        required=False,
        parent_lookup_kwargs={'board_pk': 'board__pk'},
        view_name='member-detail',
        queryset=Member.objects.all()
    )

    class Meta:
        model = KanBanUser
        fields = [
            'url', 'id', 'username', 'first_name', 'last_name', 'email',
            'is_staff', 'is_active', 'tags', 'memberships'
        ]


class NormalizedSerializer(Serializer):
    """
    Serialize all the entities needed by a user.

    response is flattened (normalized) for easy consumption by a frontend.
    """
    boards = BoardSerializer(many=True, read_only=True)
    containers = ContainerSerializer(many=True, read_only=True)
    cards = CardSerializer(many=True, read_only=True)
    users = KanBanUserSerializer(many=True, read_only=True)
    labels = LabelSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    members = MemberSerializer(many=True, read_only=True)
