import abc

from django.db import models
from django.utils.functional import cached_property

from ratings.users.models import User


class BetterModel(models.Model):
    """A better default model with a better default primary key."""

    __metaclass__ = abc.ABCMeta

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.
class Tag(BetterModel):
    """A tag for a thing.

    A tag is primarily a descriptor, like "movie", or "celebrity", or "video game".
    Tags exist in order to classify things."""

    name = models.CharField(max_length=30, unique=True, db_index=True)


class Thing(BetterModel):
    """A generic polymorphic 'thing', representing literally anything.

    A thing is defined exclusively by its metadata.
    """

    name = models.CharField(max_length=50, unique=True, db_index=True)
    tags = models.ManyToManyField(Tag, related_name="things", db_index=True, blank=True)

    @cached_property
    def get_ratings(self):
        """Return all of the likes and dislikes for the thing.

        {'likes': 123, 'dislikes': 456}
        """
        likes = self.ratings.filter(like=True).count()
        dislikes = self.ratings.filter(like=False).count()
        return {"likes": likes, "dislikes": dislikes}

    @cached_property
    def likes(self) -> int:
        """Return the number of likes."""
        return self.ratings.filter(like=True).count()

    @cached_property
    def dislikes(self) -> int:
        """Return the number of dislikes for the thing."""
        return self.ratings.filter(like=False).count()


class Rating(BetterModel):
    """A rating for a thing. Each rating has one thing."""

    class Meta:
        constraints = [
            # throws django.db.utils.IntegrityError if a duplicate is attempted
            models.UniqueConstraint(
                fields=["thing", "user"], name="user-thing ratings are unique"
            ),
        ]

    thing = models.ForeignKey(
        Thing, related_name="ratings", db_index=True, on_delete=models.CASCADE
    )
    like = models.BooleanField()  # True = like, False = dislike
    user = models.ForeignKey(
        User, related_name="ratings", db_index=True, on_delete=models.CASCADE
    )
