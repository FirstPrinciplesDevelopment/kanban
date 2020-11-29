from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import (Attachment, AttachmentType, Auditable, Board, Card,
                     Container, KanBanUser, Label, Member, Tag)

# constants
AUDITABLE_FIELDS = ['created_by', 'created_time', 'changed_by', 'changed_time',
                    'archived', 'archived_by', 'archived_time']


class KanBanUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanBanUser
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name', 'slug', 'position', 'members'] + AUDITABLE_FIELDS


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'board', 'user', 'starred', 'position']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'user', 'name', 'color']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'board', 'name', 'color']


class AttachmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachmentType
        fields = ['id', 'name', 'file_extension']


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = [
            'id', 'board', 'name', 'file_path', 'attachment_type', 'uploaded_by', 'uploaded_time'
            ]


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = [
            'id', 'board', 'name', 'slug', 'position', 'labels', 'tags'
            ] + AUDITABLE_FIELDS

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'id', 'board', 'container', 'name', 'slug', 'content', 'start_time', 'end_time',
            'complexity', 'hours', 'position', 'assigned_users', 'labels', 'tags', 'attachments'
            ] + AUDITABLE_FIELDS
