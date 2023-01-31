from datetime import date

from django.contrib import admin

from timeline.models import Entry, Topic


class DecadeFilter(admin.SimpleListFilter):
    title = 'decade'
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        return [
            (year, f'{year}s')
            for year in range(2020, 1800 - 1, -10)
        ]

    def queryset(self, request, queryset):
        if self.value():
            decade = int(self.value())
            return queryset.filter(
                date__gte=date(decade, 1, 1),
                date__lte=date(decade + 9, 12, 31),
            )


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'topics_list', 'date')
    list_filter = [DecadeFilter, 'topics']
    autocomplete_fields = ['topics']
    search_fields = ['title']

    def topics_list(self, entry):
        return ", ".join([t.slug for t in entry.topics.all()])

    topics_list.short_description = 'Topics'


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name', 'category')
    search_fields = ['name', 'slug']
