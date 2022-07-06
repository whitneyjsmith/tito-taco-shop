from django.contrib import admin
from .models import Team, TeamUser

# Register your models here.

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass

@admin.register(TeamUser)
class TeamUserAdmin(admin.ModelAdmin):
    pass
