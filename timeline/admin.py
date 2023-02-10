from datetime import date

from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect
from django.db import models
from django.forms import TextInput

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
    list_display = ('title', 'topics_list', 'weight', 'date' ,'created_at', 'updated_at')
    list_filter = [DecadeFilter, 'topics']
    autocomplete_fields = ['topics']
    search_fields = ['title']

    def topics_list(self, entry):
        return ", ".join([t.slug for t in entry.topics.all()])

    topics_list.short_description = 'Topics'


class EntryInline(admin.TabularInline):
    model = Topic.entries.through
    autocomplete_fields = ['entry']
    # formfield_overrides = {
    #     models.ForeignKey: {
    #         'widget': AutocompleteSelect(
    #             Topic.entries.field,
    #             admin.site,
    #             attrs={'style': 'width: 450px'}
    #         )
    #     },
    # }


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name', 'abbr', 'category')
    list_filter = ['category']
    search_fields = ['name', 'slug']
    inlines = [EntryInline]
