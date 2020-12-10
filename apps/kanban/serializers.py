from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
from .models import (
    Attachment, AttachmentType, Board, Card,
    Container, KanBanUser, Label, Member, Tag
    )

# app_name = 'kanban'

# constants
AUDITABLE_FIELDS = [
    'created_by', 'created_time', 'changed_by', 'changed_time',
    'archived', 'archived_by', 'archived_time'
    ]


class BoardSerializer(serializers.HyperlinkedModelSerializer):
    members = HyperlinkedIdentityField(
        view_name='board-members-list',
        lookup_url_kwarg='board_pk'
    )
    
    containers = HyperlinkedIdentityField(
        view_name='board-containers-list',
        lookup_url_kwarg='board_pk'
    )
    
    # labels = HyperlinkedIdentityField(
    #     view_name='board-labels-list',
    #     lookup_url_kwarg='board_pk'
    # )

    class Meta:
        model = Board
        fields = [
            'url', 'id', 'name', 'slug', 'position', 'containers', 'members'
            ] + AUDITABLE_FIELDS


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(view_name='board-members-detail', parent_lookup_kwargs={'board_pk': 'board__pk'})

    class Meta:
        model = Member
        fields = ['url', 'id', 'board', 'user', 'starred', 'position']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'id', 'user', 'name', 'color']


class LabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Label
        fields = ['url', 'id', 'board', 'name', 'color']


class AttachmentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AttachmentType
        fields = ['url', 'id', 'name', 'file_extension']


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attachment
        fields = [
             'url', 'id', 'board', 'name', 'file_path', 'attachment_type',
             'uploaded_by', 'uploaded_time'
            ]


class ContainerSerializer(serializers.HyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(view_name='board-containers-detail', parent_lookup_kwargs={'board_pk': 'board__pk'})

    class Meta:
        model = Container
        fields = [
             'url', 'id', 'board', 'cards', 'name', 'slug', 'position', 'labels', 'tags'
            ] + AUDITABLE_FIELDS


class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = [
             'url', 'id', 'board', 'container', 'name', 'slug', 'content',
             'start_time', 'end_time', 'complexity', 'hours', 'position',
             'assigned_users', 'labels', 'tags', 'attachments'
            ] + AUDITABLE_FIELDS


class KanBanUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KanBanUser
        fields = [
            'url', 'id', 'username', 'first_name', 'last_name', 'email',
            'is_staff', 'is_active', 'boards_created', 'containers_created',
            'cards_created'
            ]
