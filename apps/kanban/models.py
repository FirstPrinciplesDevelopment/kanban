from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from rest_framework.authtoken.models import Token


# helpers
def max_container_position(board_id: int) -> int:
    if board_id > 0:
        # return the max container position for this board
        query_result = (
            Container
            .objects
            .filter(board__pk=board_id)
            .aggregate(Max('position'))
        )
        # query_result is a dict, return just the int value or zero if None
        if query_result['position__max'] is None:
            return 0
        else:
            return query_result['position__max']
    else:
        raise Exception('Invalid board id passed in')


def max_card_position(container_id: int) -> int:
    if container_id > 0:
        # return the max card position for this container
        query_result = (
            Card
            .objects
            .filter(container__pk=container_id)
            .aggregate(Max('position'))
        )
        # query_result is a dict, return just the int value or zero if None
        if query_result['position__max'] is None:
            return 0
        else:
            return query_result['position__max']
    else:
        raise Exception('Invalid container id passed in')


class KanBanUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Create an auth token for every user after they are created."""
    if created:
        Token.objects.create(user=instance)


# related names:
# https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ForeignKey.related_name
# abstract base classes:
# https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
class Auditable(models.Model):
    """A base class to define common auditable fields."""
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
    archived = models.BooleanField(default=False)
    archived_by = models.ForeignKey(
        KanBanUser, related_name='%(app_label)s_%(class)s_archived',
        on_delete=models.SET_NULL, blank=True, null=True
    )
    archived_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Board(Auditable):
    """A Board has many Containers with Cards in them and many members."""
    name = models.CharField(
        max_length=50, unique=True,
        blank=False, null=False
    )
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=False)

    def __str__(self):
        return self.name


class Member(models.Model):
    """A Member maps a KanBanUser to a Board and provides additional fields."""
    board = models.ForeignKey(Board, related_name='members',
                              on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(KanBanUser, related_name='memberships',
                             on_delete=models.CASCADE, null=False)
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
    """A Tag is only visible to the KanBanUser that created it."""
    user = models.ForeignKey(
        KanBanUser, related_name='tags', on_delete=models.CASCADE,
        blank=False, null=False
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
    """A Label is visible to the members of the Board that it belongs to."""
    board = models.ForeignKey(
        Board, related_name='labels', on_delete=models.CASCADE,
        blank=False, null=False
    )
    name = models.CharField(
        max_length=50, unique=True, blank=False, null=False
    )
    color = models.CharField(
        max_length=32, default="#aaaaaa", blank=True, null=False
    )

    def __str__(self):
        return self.name


class Attachment(models.Model):
    """An Attachment is a file uploaded by a Member of a Board."""
    board = models.ForeignKey(
        Board, related_name='attachments', on_delete=models.CASCADE,
        blank=False, null=False
    )
    name = models.CharField(
        max_length=50, unique=True, blank=False, null=False
    )
    file_path = models.URLField(blank=False, null=False)
    uploaded_by = models.ForeignKey(
        KanBanUser, on_delete=models.CASCADE, blank=False, null=False
    )
    uploaded_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Container(Auditable):
    """A Container contains many Cards and belongs to a single Board."""
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

    def save(self, *args, **kwargs):
        if not self.position:
            # get the max position of a containers in this container's board
            max_position = max_container_position(self.board_id)
            # increment that max position
            new_position = max_position + 1
            # set self.position
            self.position = new_position
        return super().save(*args, **kwargs)


class Card(Auditable):
    """The most fundamental KanBan unit, represents an item or task."""
    container = models.ForeignKey(
        Container, related_name='cards', on_delete=models.CASCADE,
        blank=False, null=False
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
    assigned_users = models.ManyToManyField(Member, blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)

    def reorder_cards(self):
        """Card being saved is source of truth, reorder others around it"""
        # get all the other cards in this container, ordered by position
        cards = list(
            Card.objects
            .filter(container__pk=self.container_id)
            .exclude(id=self.id)
            .order_by('position')
        )
        i = 1
        while len(cards) > 0:
            if (i != self.position):
                # pop the card with the lowest position, set position and save
                c = cards.pop(0)
                if (c.position != i):
                    c.position = i
                    # save with reorder kwarg False to prevent recursion
                    c.save(reorder=False)
            i += 1

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # important! make sure 'reordering' kwarg is removed
        # https://docs.python.org/3/library/stdtypes.html#dict.pop
        do_reorder = kwargs.pop('reorder', True)
        if not self.position:
            # get the max position of a cards in this card's containers
            max_position = max_card_position(self.container_id)
            # increment that max position
            new_position = max_position + 1
            # set self.position
            self.position = new_position
        if do_reorder:
            self.reorder_cards()
        return super().save(*args, **kwargs)
