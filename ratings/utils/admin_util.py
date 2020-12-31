from django.contrib import admin
from django.db import models
from django.forms import TextInput

# class PrefixedHashField(models.CharField):

#     @staticmethod
#     def gen_value(prefix, hash_length):
#         hashtext = "".join(random.choices(string.ascii_letters + string.digits, k=hash_length))
#         return f"{prefix}_{hashtext}"

#     def __init__(self, *args, **kwargs):
#         prefix = kwargs.pop('prefix')
#         hash_length = kwargs.pop('hash_length')
#         kwargs["default"] = partial(self.gen_value, prefix, hash_length)
#         super(PrefixedHashField, self).__init__(*args, **kwargs)


class BetterAdmin(admin.ModelAdmin):
    """A mixin for Django Admin classes for models that renders single-line TextField inputs."""

    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "80"})},
        models.TextField: {"widget": TextInput(attrs={"size": "80"})},
    }
