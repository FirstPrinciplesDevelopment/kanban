from django.contrib import admin
from .models import Board, Member, Container, Card, AttachmentType, Attachment, Tag, Label

# register your models here.
admin.site.register(Board)
admin.site.register(Member)
admin.site.register(Container)
admin.site.register(Card)
admin.site.register(AttachmentType)
admin.site.register(Attachment)
admin.site.register(Tag)
admin.site.register(Label)
