from django.db.models import Case, When, Value
from django.db.models.functions import Coalesce, Lower
from django.views import generic

from timeline.models import Entry, Topic


class Timeline(generic.ListView):
    queryset = Entry.objects.prefetch_related('topics')
    template_name = 'timeline/index.html'

    extra_context = {
        'topics': Topic.objects.annotate(
            name_ord=Lower(Coalesce('abbr', 'name'))
        ).annotate(
            category_ord=Case(
                When(category=Topic.Category.TOPIC, then=Value(1)),
                When(category=Topic.Category.ORG, then=Value(2)),
                When(category=Topic.Category.PERSON, then=Value(3)),
                default=Value(999),
            )
        ).order_by('category_ord', 'name_ord').all(),
    }
