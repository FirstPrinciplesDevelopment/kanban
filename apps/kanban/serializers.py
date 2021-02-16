from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        HyperlinkedRelatedField, Serializer)

from .models import (Attachment, Board, Card, Container, KanBanUser, Label,
                     Member, Tag)

# constants
AUDITABLE_FIELDS = [
    'created_by', 'created_time', 'changed_by', 'changed_time',
    'archived', 'archived_by', 'archived_time'
]


class BoardSerializer(HyperlinkedModelSerializer):
    """Serialize a Board object."""
    containers = HyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='container-detail',
        queryset=Container.objects.all()
    )
    labels = HyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='label-detail',
        queryset=Label.objects.all()
    )
    attachments = HyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='attachment-detail',
        queryset=Attachment.objects.all()
    )
    members = HyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='member-detail',
        queryset=Member.objects.all()
    )

    class Meta:
        model = Board
        fields = [
            'url', 'id', 'name', 'slug', 'containers',
            'members', 'labels', 'attachments'
        ] + AUDITABLE_FIELDS


class MemberSerializer(HyperlinkedModelSerializer):
    """Serialize a Member object."""

    class Meta:
        model = Member
        fields = ['url', 'id', 'board', 'user', 'starred', 'position']


class ContainerSerializer(HyperlinkedModelSerializer):
    """Serialize a Container object."""

    cards = HyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='card-detail',
        queryset=Card.objects.all()
    )
    labels = HyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='label-detail',
        queryset=Label.objects.all()
    )
    tags = HyperlinkedRelatedField(
        many=True,
        required=False,
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


class CardSerializer(HyperlinkedModelSerializer):
    """Serialize a Card object."""

    container = HyperlinkedRelatedField(
        required=True,
        view_name='container-detail',
        queryset=Container.objects.all()
    )
    labels = HyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='label-detail',
        queryset=Label.objects.all()
    )
    tags = HyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='tag-detail',
        queryset=Tag.objects.all()
    )
    attachments = HyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='attachment-detail',
        queryset=Attachment.objects.all()
    )
    assigned_users = HyperlinkedRelatedField(
        many=True,
        required=False,
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


class TagSerializer(HyperlinkedModelSerializer):
    """Serialize a Tag object."""

    class Meta:
        model = Tag
        fields = ['url', 'id', 'user', 'name', 'color']


class LabelSerializer(HyperlinkedModelSerializer):
    """Serialize a Label object."""

    class Meta:
        model = Label
        fields = ['url', 'id', 'board', 'name', 'color']


class AttachmentSerializer(HyperlinkedModelSerializer):
    """Serialize an Attachment object."""

    class Meta:
        model = Attachment
        fields = [
            'url', 'id', 'board', 'name', 'file_path',
            'uploaded_by', 'uploaded_time'
        ]


class KanBanUserSerializer(HyperlinkedModelSerializer):
    """Serialize a KanBanUser object."""
    tags = HyperlinkedRelatedField(
        many=True,
        required=False,
        view_name='tag-detail',
        queryset=Tag.objects.all()
    )
    memberships = HyperlinkedRelatedField(
        many=True,
        required=False,
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
