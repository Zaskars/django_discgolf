from django.db import models
from django.contrib.auth.models import User

from .user import PlayerProfile


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    baskets_count = models.IntegerField()
    date = models.DateField()
    city = models.CharField(max_length=100)
    max_players = models.IntegerField()
    park_scheme = models.ImageField(upload_to="park_schemes/", null=True, blank=True)
    director = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class TournamentRegistration(models.Model):
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="registrations"
    )
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tournament", "player")


class Round(models.Model):
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="rounds"
    )
    round_number = models.IntegerField()
    name = models.CharField(max_length=100, default=f"Раунд {round_number}")

    def get_registered_players(self):
        # Получение списка зарегистрированных игроков для этого турнира
        return [
            registration.player for registration in self.tournament.registrations.all()
        ]


class PlayerRound(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    round = models.ForeignKey(
        Round, on_delete=models.CASCADE, related_name="player_rounds"
    )
    throws = models.IntegerField(default=0)
