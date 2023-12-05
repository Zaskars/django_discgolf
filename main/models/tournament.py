from django.db import models
from django.contrib.auth.models import User

from .course import Basket, Course
from .user import PlayerProfile


class Tournament(models.Model):
    name = models.CharField(max_length=100)
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
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    def get_registered_players(self):
        return [
            registration.player for registration in self.tournament.registrations.all()
        ]


class PlayerScore(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    throws = models.IntegerField()

    def __str__(self):
        return f"{self.player.user.username} - Round {self.round.round_number}, {self.basket}"
