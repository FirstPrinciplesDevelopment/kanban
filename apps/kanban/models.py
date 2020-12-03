from django.contrib.auth.models import AbstractUser
from django.db import models

# constants
IMAGE = 0
TEXT_FILE = 1
FILE_EXTENSION_CHOICES = (
    (IMAGE, '.jpg,.jpeg,.gif,.png,.pdf,'),
    (TEXT_FILE, '.txt,.rst,.md,.c,.cpp,.h,.cs.,.py')
)


class KanBanUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.username


# related names:
# https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ForeignKey.related_name
# abstract base classes:
# https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
class Auditable(models.Model):
    """A base class to define common auditable fields"""
    created_by = models.ForeignKey(
        KanBanUser, related_name='%(class)ss_created',
        on_delete=models.SET_NULL, blank=True, null=True
        )
    created_time = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(
        KanBanUser, related_name='%(app_label)s_%(class)s_changed',
        on_delete=models.SET_NULL, blank=True, null=True
        )
    changed_time = models.DateTimeField(auto_now=True)
    archived = models.BooleanField()
    archived_by = models.ForeignKey(
        KanBanUser, related_name='%(app_label)s_%(class)s_archived',
        on_delete=models.SET_NULL, blank=True, null=True
        )
    archived_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Board(Auditable):
    """A Board has many Containers with Cards in them and many members"""
    name = models.CharField(
        max_length=50, unique=True,
        blank=False, null=False
        )
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=False)
    position = models.PositiveSmallIntegerField(blank=True, null=False)
    members = models.ManyToManyField(KanBanUser, through='Member')

    def __str__(self):
        return self.name


class Member(models.Model):
    """
    A Member maps a KanBanUser to a Board,
    it is the explicit through table for that many-to-many
    """
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(KanBanUser, on_delete=models.CASCADE, null=False)
    starred = models.BooleanField(default=False, blank=True, null=False)
    position = models.PositiveSmallIntegerField(blank=True, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['board', 'user'],
                name='unique_board_member'
                )
        ]


class Tag(models.Model):
    """A Tag is only visible to the KanBanUser that created it"""
    user = models.ForeignKey(
        KanBanUser, on_delete=models.CASCADE, blank=False, null=False
        )
    name = models.CharField(
        max_length=50, unique=True, blank=False, null=False
        )
    color = models.CharField(
        max_length=32, default="#aaaaaa", blank=True, null=False
        )

    def __str__(self):
        return self.name


class Label(models.Model):
    """A Label is visible to the members of the Board that it belongs to"""
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, blank=False, null=False
        )
    name = models.CharField(
        max_length=50, unique=True, blank=False, null=False
    )
    color = models.CharField(
        max_length=32, default="#aaaaaa", blank=True, null=False
    )

    def __str__(self):
        return self.name


class AttachmentType(models.Model):
    name = models.CharField(
        max_length=50, unique=True, blank=False, null=False
    )
    file_extension = models.IntegerField(
        choices=FILE_EXTENSION_CHOICES, default=IMAGE
    )

    def __str__(self):
        return self.name


class Attachment(models.Model):
    """An Attachment is a file uploaded by a Member of a Board"""
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, blank=False, null=False
        )
    name = models.CharField(
        max_length=50, unique=True, blank=False, null=False
        )
    file_path = models.URLField(blank=False, null=False)
    attachment_type = models.ForeignKey(
        AttachmentType, on_delete=models.CASCADE, blank=False, null=False
        )
    uploaded_by = models.ForeignKey(
        KanBanUser, on_delete=models.CASCADE, blank=False, null=False
        )
    uploaded_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Container(Auditable):
    """A Container contains many Cards and belongs to a single Board"""
    board = models.ForeignKey(
        Board, related_name="containers", on_delete=models.CASCADE,
        blank=False, null=False
        )
    name = models.CharField(
        max_length=50, unique=True, blank=False, null=False
        )
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=False)
    position = models.PositiveSmallIntegerField(blank=True, null=False)
    labels = models.ManyToManyField(Label, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name


class Card(Auditable):
    """
    A Card is the most fundamental KanBan unit,
    and represents an item, task
    """
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, blank=False, null=False
        )
    container = models.ForeignKey(
        Container, related_name='cards', on_delete=models.CASCADE, blank=False, null=False
        )
    name = models.CharField(
        max_length=100, unique=True, blank=False, null=False
        )
    slug = models.SlugField(
        max_length=100, unique=True, blank=True, null=False
        )
    content = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    complexity = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True
        )
    hours = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True
        )
    position = models.PositiveSmallIntegerField(blank=True, null=False)
    assigned_users = models.ManyToManyField(KanBanUser, blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)

    def __str__(self):
        return self.name
