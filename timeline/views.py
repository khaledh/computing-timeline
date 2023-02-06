from django.db.models import Case, F, When, Value as V
from django.db.models.functions import Coalesce, Lower, Reverse, Right, StrIndex
from django.views import generic

from timeline.models import Entry, Topic


class Timeline(generic.ListView):
    queryset = Entry.objects.prefetch_related('topics')
    template_name = 'timeline/index.html'

    extra_context = {
        'topics': Topic.objects.annotate(
            space_pos=StrIndex(Reverse('name'), V(' '))
        ).annotate(
            name_ord=Case(
                When(category=Topic.Category.PERSON, then=Right('name', F('space_pos') - 1)),
                default=Lower(Coalesce('abbr', 'name')),
            )
        ).annotate(
            category_ord=Case(
                When(category=Topic.Category.TOPIC, then=V(1)),
                When(category=Topic.Category.ORG, then=V(2)),
                When(category=Topic.Category.PERSON, then=V(3)),
                default=V(999),
            )
        ).order_by('category_ord', 'name_ord').all(),
    }
