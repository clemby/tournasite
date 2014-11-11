from django.contrib import admin

from . import models


class MatchInline(admin.TabularInline):
    model = models.Match
    extra = 0


class TournamentAdmin(admin.ModelAdmin):
    inlines = (MatchInline,)
    list_display = ('name', 'planned_start', 'planned_finish')


admin.site.register(models.Tournament, TournamentAdmin)


class TeamEntryInline(admin.TabularInline):
    model = models.TeamEntry
    extra = 0


class TeamAdmin(admin.ModelAdmin):
    fields = ('name', 'creator')
    inlines = (TeamEntryInline,)
    list_display = ('name', 'creator')


admin.site.register(models.Team, TeamAdmin)
