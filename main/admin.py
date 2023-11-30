from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from main.models import PlayerProfile, Tournament, Round


class ProfileInline(admin.StackedInline):
    model = PlayerProfile
    can_delete = False
    verbose_name_plural = "profile"


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


class RoundInline(admin.TabularInline):
    model = Round
    extra = 1


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "city", "max_players", "rounds_count")
    inlines = [RoundInline]

    def rounds_count(self, obj):
        return obj.rounds.count()

    rounds_count.short_description = "Количество раундов"


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ("tournament", "round_number")
    list_filter = ("tournament",)
    search_fields = ("tournament__name",)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
