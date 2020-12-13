from rest_framework import serializers
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
    parent_lookup_kwargs = {
        'board_pk': 'board__pk'
    }

    class Meta:
        model = Member
        fields = ('url',)


class MemberBoardSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'pk': 'pk'
    }

    class Meta:
        model = Board
        fields = ('url', 'name')


class BoardContainerSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'board_pk': 'board__pk'
    }

    class Meta:
        model = Container
        fields = ('url', 'name')


class ContainerBoardSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'pk': 'pk'
    }

    class Meta:
        model = Board
        fields = ('url', 'name')


class ContainerCardSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'board_pk': 'container__board__pk', 'container_pk': 'container__pk'
    }

    class Meta:
        model = Card
        fields = ('url', 'name')


class CardContainerSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'board_pk': 'board__pk'
    }

    class Meta:
        model = Container
        fields = ('url', 'name')


class CardBoardSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
                'pk': 'pk'
    }

    class Meta:
        model = Board
        fields = ('url', 'name')


class BoardSerializer(HyperlinkedModelSerializer):
    containers = BoardContainerSerializer(many=True, read_only=True)
    members = BoardMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            'url', 'id', 'name', 'slug', 'position', 'containers', 'members'
            ] + AUDITABLE_FIELDS


class MemberSerializer(NestedHyperlinkedModelSerializer):
    board = MemberBoardSerializer(read_only=True)
    parent_lookup_kwargs = {'board_pk': 'board__pk'}

    class Meta:
        model = Member
        fields = ['url', 'id', 'board', 'user', 'starred', 'position']


class KanBanUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KanBanUser
        fields = [
            'url', 'id', 'username', 'first_name', 'last_name', 'email',
            'is_staff', 'is_active', 'boards_created', 'containers_created',
            'cards_created'
            ]


class ContainerSerializer(NestedHyperlinkedModelSerializer):
    # url = NestedHyperlinkedIdentityField(
    #     view_name='containers-detail',
    #     parent_lookup_kwargs={'board_pk': 'board__pk'}
    #     )
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
    # url = NestedHyperlinkedIdentityField(
    #     view_name='cards-detail',
    #     parent_lookup_kwargs={'board_pk': 'board__pk',
    #                           'container_pk': 'container__pk'}
    #     )
    # parent_lookup_kwargs = {'board_pk': 'board__pk',
    #                         'container_pk': 'container__pk'}
    container = CardContainerSerializer(read_only=True)
    board = CardBoardSerializer(read_only=True)

    class Meta:
        model = Card
        fields = [
             'url', 'id', 'board', 'container', 'name', 'slug', 'content',
             'start_time', 'end_time', 'complexity', 'hours', 'position',
             'assigned_users', 'labels', 'tags', 'attachments'
            ] + AUDITABLE_FIELDS


class TagSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'id', 'user', 'name', 'color']


class LabelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Label
        fields = ['url', 'id', 'board', 'name', 'color']


class AttachmentTypeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = AttachmentType
        fields = ['url', 'id', 'name', 'file_extension']


class AttachmentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Attachment
        fields = [
             'url', 'id', 'board', 'name', 'file_path', 'attachment_type',
             'uploaded_by', 'uploaded_time'
            ]
