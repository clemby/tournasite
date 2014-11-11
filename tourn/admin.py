from django.contrib import admin

from . import models


admin.site.register(models.Tournament)
admin.site.register(models.Match)


class TeamEntryInline(admin.TabularInline):
    model = models.TeamEntry
    extra = 0


class TeamAdmin(admin.ModelAdmin):
    fields = ('name', 'creator')
    inlines = [TeamEntryInline]
    list_display = ('name', 'creator')


admin.site.register(models.Team, TeamAdmin)
