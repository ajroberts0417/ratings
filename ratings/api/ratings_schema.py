import graphene
from django.conf import settings
from django.core.exceptions import PermissionDenied
from graphene_django import DjangoObjectType

from ratings.things.models import Rating, Tag, Thing
from ratings.users.models import DiscordUser, User
from ratings.utils.model_util import get_random

BOT_TOKEN = settings.BOT_TOKEN


class RatingType(DjangoObjectType):
    """Define the graphene type schema for a Rating."""

    class Meta:
        """The django model and fields from which we derive the Graphene Type."""

        model = Rating
        fields = "__all__"


class ThingType(DjangoObjectType):
    """Define the graphene type schema for a Thing."""

    class Meta:
        """The django model and fields from which we derive the Graphene Type."""

        model = Thing
        fields = "__all__"

    likes = graphene.Int()
    dislikes = graphene.Int()

    def resolve_likes(parent: Thing, info):
        return parent.likes

    def resolve_dislikes(parent: Thing, info):
        return parent.dislikes


class TagType(DjangoObjectType):
    """Define the graphene type schema for a Tag."""

    class Meta:
        """The django model and fields from which we derive the Graphene Type."""

        model = Tag
        fields = "__all__"


class RatingsQuery(graphene.ObjectType):
    ratings_count = graphene.Int(username=graphene.String())
    ratings = graphene.List(RatingType, username=graphene.String())
    things = graphene.List(ThingType)
    get_thing = graphene.Field(ThingType)

    def resolve_ratings_count(root: None, info, **kwargs):
        if username := kwargs.get("username"):
            return Rating.objects.filter(user__username=username).count()
        return Rating.objects.count()

    def resolve_ratings(root: None, info, **kwargs):
        if username := kwargs.get("username"):
            return Rating.objects.filter(user__username=username)
        return Rating.objects.all()

    def resolve_things(root: None, info, **kwargs):
        return Thing.objects.all()

    def resolve_get_thing(root: None, info, **kwargs):
        return get_random(Thing)


class IncrementRating(graphene.Mutation):
    """Mutation to increment the rating of a thing."""

    class Arguments:
        """Define the schema for arguments to the mutation."""

        thing_id = graphene.ID()
        discord_user_id = graphene.String(required=False)

    rating = graphene.Field(RatingType)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(parent: None, info, thing_id, discord_user_id=None, bot_token=""):
        """Perform the mutation."""
        user = info.context.user
        if user.is_authenticated:
            rating, _ = Rating.objects.update_or_create(
                thing_id=thing_id, user=user, defaults={"like": True}
            )
            return IncrementRating(ok=True)
        if discord_user_id and bot_token == BOT_TOKEN:
            try:
                discord_user = DiscordUser.objects.get(discord_id=discord_user_id)
            except DiscordUser.DoesNotExist:
                user, _ = User.objects.get_or_create(username=discord_user_id)
                discord_user = DiscordUser.objects.create(
                    user=user, discord_id=discord_user_id
                )
            rating, _ = Rating.objects.update_or_create(
                thing_id=thing_id, user=discord_user.user, defaults={"like": True}
            )
            return IncrementRating(rating=rating, ok=True)

        raise PermissionDenied("No valid user provided.")


class DecrementRating(graphene.Mutation):
    """Mutation to increment the rating of a thing."""

    class Arguments:
        """Define the schema for arguments to the mutation."""

        thing_id = graphene.ID()
        discord_user_id = graphene.String(required=False)

    rating = graphene.Field(RatingType)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(parent: None, info, thing_id, discord_user_id=None, bot_token=""):
        """Perform the mutation."""
        user = info.context.user
        if user.is_authenticated:
            rating, _ = Rating.objects.update_or_create(
                thing_id=thing_id, user=user, defaults={"like": False}
            )
            return IncrementRating(ok=True)
        if discord_user_id and bot_token == BOT_TOKEN:
            try:
                discord_user = DiscordUser.objects.get(discord_id=discord_user_id)
            except DiscordUser.DoesNotExist:
                user, _ = User.objects.get_or_create(username=discord_user_id)
                discord_user = DiscordUser.objects.create(
                    user=user, discord_id=discord_user_id
                )
            rating, _ = Rating.objects.update_or_create(
                thing_id=thing_id, user=discord_user.user, defaults={"like": False}
            )
            return IncrementRating(rating=rating, ok=True)

        raise PermissionDenied("No valid user provided.")


class RatingsMutation(graphene.ObjectType):
    increment_rating = IncrementRating.Field()
    decrement_rating = DecrementRating.Field()
