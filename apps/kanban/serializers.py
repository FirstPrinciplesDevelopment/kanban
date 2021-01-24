from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        ModelSerializer, Serializer)
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from .models import (Attachment, AttachmentType, Board, Card, Container,
                     KanBanUser, Label, Member, Tag)

# constants
AUDITABLE_FIELDS = [
    'created_by', 'created_time', 'changed_by', 'changed_time',
    'archived', 'archived_by', 'archived_time'
]


# related model serializers

class RelatedContainerSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a related model to a Container."""
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

    class Meta:
        model = Container
        fields = ('url', 'id', 'name')


class RelatedBoardSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a related model to a Board."""
    parent_lookup_kwargs = {'pk': 'pk'}

    class Meta:
        model = Board
        fields = ('url', 'id')


class RelatedLabelSerialzer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a related model to a Label"""
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

    class Meta:
        model = Label
        fields = ('url', 'id', 'name')


class RelatedMemberSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a related model to a Member."""
    parent_lookup_kwargs = {
        'board_pk': 'board__pk'
    }

    class Meta:
        model = Member
        fields = ('url', 'id', 'board')


class RelatedCardSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a related model to a Card."""
    parent_lookup_kwargs = {
        'board_pk': 'container__board__pk', 'container_pk': 'container__pk'
    }

    class Meta:
        model = Card
        fields = ('url', 'id', 'name')


class RelatedTagSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a related model to a Tag"""
    parent_lookup_kwargs = {'user_pk': 'user__pk'}

    class Meta:
        model = Tag
        fields = ('url', 'id', 'name')


class RelatedAttachmentSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a related model to a Attachment"""
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

    class Meta:
        model = Attachment
        fields = ('url', 'id', 'name', 'file_path')


# model serializers

class BoardSerializer(HyperlinkedModelSerializer):
    """Serialize a Board object."""
    containers = RelatedContainerSerializer(many=True, required=False)
    labels = RelatedLabelSerialzer(many=True, required=False)
    attachments = RelatedAttachmentSerializer(many=True, required=False)
    members = RelatedMemberSerializer(many=True, required=False)

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
    cards = RelatedCardSerializer(many=True, required=False)
    labels = RelatedLabelSerialzer(many=True, required=False)
    tags = RelatedTagSerializer(many=True, required=False)
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

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
    container = NestedHyperlinkedRelatedField(
        parent_lookup_kwargs={'board_pk': 'board__pk'},
        view_name='container-detail',
        queryset=Container.objects.all()
    )
    labels = RelatedLabelSerialzer(many=True, required=False)
    tags = RelatedTagSerializer(many=True, required=False)
    attachments = RelatedAttachmentSerializer(many=True, required=False)
    parent_lookup_kwargs = {
        'board_pk': 'container__board__pk', 'container_pk': 'container__pk'
    }

    class Meta:
        model = Card
        fields = [
            'url', 'id', 'board', 'container', 'name', 'slug', 'content',
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


class AttachmentTypeSerializer(ModelSerializer):
    """Serialize an AttachmentType object."""
    class Meta:
        model = AttachmentType
        fields = ['id', 'name', 'file_extension']


class AttachmentSerializer(NestedHyperlinkedModelSerializer):
    """Serialize an Attachment object."""
    attachment_type = PrimaryKeyRelatedField(
        queryset=AttachmentType.objects.all()
    )
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

    class Meta:
        model = Attachment
        fields = [
            'url', 'id', 'board', 'name', 'file_path', 'attachment_type',
            'uploaded_by', 'uploaded_time'
        ]


class KanBanUserSerializer(HyperlinkedModelSerializer):
    """Serialize a KanBanUser object."""
    tags = RelatedTagSerializer(many=True, required=False)
    memberships = RelatedMemberSerializer(many=True, required=False)

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
    attachment_types = AttachmentTypeSerializer(many=True, read_only=True)
    members = MemberSerializer(many=True, read_only=True)
