from django.db import models
from django.contrib.auth.models import User

# constants
IMAGE = 0
TEXT_FILE = 1
FILE_EXTENSION_CHOICES = (
    (IMAGE, '.jpg,.jpeg,.gif,.png,.pdf,'),
    (TEXT_FILE, '.txt,.rst,.md,.c,.cpp,.h,.cs.,.py')
)

# related names: https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ForeignKey.related_name
# abstract base classes: https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
class Auditable(models.Model):
    """A base class to define common auditable fields"""
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    changed_time = models.DateTimeField(auto_now=True)
    archived = models.BooleanField()
    archived_by = models.ForeignKey(User, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    archived_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Board(Auditable):
    """A Board has many Containers with Cards in them and many assigned users"""
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=False)
    position = models.PositiveSmallIntegerField(blank=True, null=False)
    members = models.ManyToManyField(User, through='Member')


class Member(models.Model):
    """A Member maps a User to a Board, it is the explicit through table for that many-to-many"""
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    starred = models.BooleanField(default=False, blank=True, null=False)
    position = models.PositiveSmallIntegerField(blank=True, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['board', 'user'], name='unique_board_member')
        ]


class Tag(models.Model):
    """A Tag is only visible to the User that created it"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    color = models.CharField(max_length=32, default="#aaaaaa", blank=True, null=False)


class Label(models.Model):
    """A Label is visible to the members of the Board that it belongs to"""
    board = models.ForeignKey(Board, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    color = models.CharField(max_length=32, default="#aaaaaa", blank=True, null=False)


class AttachmentType(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    file_extension = models.IntegerField(choices=FILE_EXTENSION_CHOICES, default=IMAGE)


class Attachment(models.Model):
    """An Attachment is a file uploaded by a Member of a Board"""
    board = models.ForeignKey(Board, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    url = models.URLField(blank=False, null=False)
    attachment_type = models.ForeignKey(AttachmentType, on_delete=models.CASCADE, blank=False, null=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    uploaded_time = models.DateTimeField(auto_now=True)


class Container(Auditable):
    """A Container contains many Cards and belongs to a single Board"""
    board = models.ForeignKey(Board, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=False)
    position = models.PositiveSmallIntegerField(blank=True, null=False)
    labels = models.ManyToManyField(Label)
    tags = models.ManyToManyField(Tag)


class Card(Auditable):
    """A Card is the most fundamental KanBan unit, and represents a single item or task"""
    board = models.ForeignKey(Board, on_delete=models.CASCADE, blank=False, null=False)
    container = models.ForeignKey(Container, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=False)
    content = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    complexity = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    hours = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    position = models.PositiveSmallIntegerField(blank=True, null=False)
    assigned_users = models.ManyToManyField(User)
    labels = models.ManyToManyField(Label)
    tags = models.ManyToManyField(Tag)
    attachments = models.ManyToManyField(Attachment)
