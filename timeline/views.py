from django.db.models.functions import Coalesce
from django.views import generic

from timeline.models import Entry, Topic


class Timeline(generic.ListView):
    queryset = Entry.objects.prefetch_related('topics')
    template_name = 'timeline/index.html'

    extra_context = {
        'topics': Topic.objects.annotate(
            name_ord=Coalesce('abbr', 'name')
        ).order_by('name_ord').all(),
    }
