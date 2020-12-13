from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from .models import (Attachment, AttachmentType, Board, Card, Container,
                     KanBanUser, Label, Member, Tag)

# constants
AUDITABLE_FIELDS = [
    'created_by', 'created_time', 'changed_by', 'changed_time',
    'archived', 'archived_by', 'archived_time'
    ]


class BoardMemberSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a Board to a Member."""
    parent_lookup_kwargs = {
        'board_pk': 'board__pk'
    }

    class Meta:
        model = Member
        fields = ('url',)


class MemberBoardSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a Member to a Board."""
    parent_lookup_kwargs = {
        'pk': 'pk'
    }

    class Meta:
        model = Board
        fields = ('url', 'name')


class BoardContainerSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a Board to a Container."""
    parent_lookup_kwargs = {
        'board_pk': 'board__pk'
    }

    class Meta:
        model = Container
        fields = ('url', 'name')


class ContainerBoardSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a Container to a Board."""
    parent_lookup_kwargs = {
        'pk': 'pk'
    }

    class Meta:
        model = Board
        fields = ('url', 'name')


class ContainerCardSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a Container to a Card."""
    parent_lookup_kwargs = {
        'board_pk': 'container__board__pk', 'container_pk': 'container__pk'
    }

    class Meta:
        model = Card
        fields = ('url', 'name')


class CardContainerSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a Card to a Container."""
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

    class Meta:
        model = Container
        fields = ('url', 'name')


class CardBoardSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a Card to a Board."""
    parent_lookup_kwargs = {'pk': 'pk'}

    class Meta:
        model = Board
        fields = ('url', 'name')


class MemberKanBanUserSerializer(NestedHyperlinkedModelSerializer):
    """Serialize the relationship from a Member to a KanBanUser."""
    parent_lookup_kwargs = {'pk': 'pk'}

    class Meta:
        model = KanBanUser
        fields = ('url', 'username')


class BoardSerializer(HyperlinkedModelSerializer):
    """Serialize a Board object."""
    containers = BoardContainerSerializer(many=True, read_only=True)
    # members = BoardMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            'url', 'id', 'name', 'slug', 'position', 'containers', 'members'
            ] + AUDITABLE_FIELDS


class MemberSerializer(NestedHyperlinkedModelSerializer):
    """Serialize a Member object."""
    board = MemberBoardSerializer(read_only=True)
    user = MemberKanBanUserSerializer(read_only=True)
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

    class Meta:
        model = Member
        fields = ['url', 'id', 'board', 'user', 'starred', 'position']


class ContainerSerializer(NestedHyperlinkedModelSerializer):
    """Serialize a Container object."""
    board = ContainerBoardSerializer(many=False, read_only=True)
    cards = ContainerCardSerializer(many=True, read_only=True)
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

    class Meta:
        model = Container
        fields = [
             'url', 'id', 'board', 'name', 'slug',
             'position', 'cards', 'labels', 'tags'
            ] + AUDITABLE_FIELDS


class CardSerializer(NestedHyperlinkedModelSerializer):
    """Serialize a Card object."""
    container = CardContainerSerializer(read_only=True)
    board = CardBoardSerializer(read_only=True)
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


class AttachmentTypeSerializer(HyperlinkedModelSerializer):
    """Serialize an AttachmentType object."""
    class Meta:
        model = AttachmentType
        fields = ['url', 'id', 'name', 'file_extension']


class AttachmentSerializer(HyperlinkedModelSerializer):
    """Serialize an Attachment object."""
    class Meta:
        model = Attachment
        fields = [
             'url', 'id', 'board', 'name', 'file_path', 'attachment_type',
             'uploaded_by', 'uploaded_time'
            ]


class KanBanUserSerializer(HyperlinkedModelSerializer):
    """Serialize a KanBanUser object."""
    class Meta:
        model = KanBanUser
        fields = [
            'url', 'id', 'username', 'first_name', 'last_name', 'email',
            'is_staff', 'is_active'
            ]
