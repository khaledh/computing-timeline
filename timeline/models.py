from django.db import models


class Topic(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=50, unique=True)
    abbr = models.CharField(max_length=15, null=True, blank=True)

    class Category(models.TextChoices):
        TOPIC = 'T', 'Topic'
        PERSON = 'P', 'Person'
        ORG = 'O', 'Organization'

    category = models.CharField(
        max_length=2,
        choices=Category.choices,
        default=Category.TOPIC,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['slug']


class Entry(models.Model):
    title = models.CharField(max_length=75, unique=True)
    desc = models.TextField(max_length=1000, null=True, blank=True)
    date = models.DateField()
    topics = models.ManyToManyField(Topic, related_name='entries', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "entries"
        ordering = ['date']

    def __str__(self):
        return self.title
