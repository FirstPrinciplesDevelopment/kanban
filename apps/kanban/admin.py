from django.contrib import admin

from .models import (
    Attachment, Board, Card, Container,
    KanBanUser, Label, Member, Tag
)

# register your models here.
admin.site.register(Board)
admin.site.register(Member)
admin.site.register(Container)
admin.site.register(Card)
admin.site.register(Attachment)
admin.site.register(Tag)
admin.site.register(Label)
admin.site.register(KanBanUser)
