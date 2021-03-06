from news.models import Newspost
from django.contrib import admin


class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['title']}),
        ('Date information',    {'fields': ['pub_date']}),
        ('Content',             {'fields': ['content']}),
    ]
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']

admin.site.register(Newspost, NewsAdmin)
