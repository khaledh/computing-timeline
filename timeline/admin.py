from django.contrib import admin

from timeline.models import Entry, Topic


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'topics_list', 'date')
    autocomplete_fields = ['topics']
    # filter_horizontal = ['topics']
    search_fields = ['title']

    def topics_list(self, entry):
        return ", ".join([t.slug for t in entry.topics.all()])

    topics_list.short_description = 'Topics'


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name', 'category')
    search_fields = ['name', 'slug']
