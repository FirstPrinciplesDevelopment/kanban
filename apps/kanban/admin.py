from django.contrib import admin
from .models import Board, Member, Container, Card, AttachmentType, Attachment, Tag, Label

# Register your models here.
admin.site.Register(Board)
admin.site.Register(Member)
admin.site.Register(Container)
admin.site.Register(Card)
admin.site.Register(AttachmentType)
admin.site.Register(Attachment)
admin.site.Register(Tag)
admin.site.Register(Label)
