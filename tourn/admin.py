from django.contrib import admin

from . import models


class MatchInline(admin.TabularInline):
    model = models.Match
    extra = 0


class PlayerRandomTeamEntryInline(admin.TabularInline):
    model = models.PlayerRandomTeamEntry
    extra = 0


class TeamEntryInline(admin.TabularInline):
    model = models.TeamEntry
    extra = 0


class TournamentAdmin(admin.ModelAdmin):
    inlines = (
        MatchInline,
        TeamEntryInline,
        PlayerRandomTeamEntryInline,
    )
    list_display = ('name', 'planned_start', 'planned_finish')


admin.site.register(models.Tournament, TournamentAdmin)


class TeamAdmin(admin.ModelAdmin):
    fields = ('name', 'creator')
    inlines = (TeamEntryInline,)
    list_display = ('name', 'creator')


admin.site.register(models.Team, TeamAdmin)
