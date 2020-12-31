import random

from django.db.models import Max, Model


def get_random(model: Model):
    """Efficiently get a random object -- this only works for models with auto-incrementing ids."""
    max_id = model.objects.all().aggregate(max_id=Max("id"))["max_id"]
    # loop in case of deletions
    while True:
        pk = random.randint(1, max_id)
        obj = model.objects.filter(pk=pk).first()
        if obj:
            return obj
