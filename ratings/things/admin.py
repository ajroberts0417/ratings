from django.contrib import admin

from ratings.things.models import Rating, Tag, Thing
from ratings.utils.admin_util import BetterAdmin


@admin.register(Rating)
class RatingAdmin(BetterAdmin):
    """Custom definition for Rating admin form."""
    list_display = (
        'thing',
        'like',
    )
    search_fields = ('thing__name',)
    autocomplete_fields = ['thing']


@admin.register(Thing)
class ThingAdmin(BetterAdmin):
    """Custom definition for Thing admin form."""
    list_display = (
        'name',
        'likes',
        'dislikes',
    )
    search_fields = ('name',)


# Register your models here.
admin.site.register(Tag)