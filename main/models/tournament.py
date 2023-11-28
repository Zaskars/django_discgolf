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


class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round_number = models.IntegerField()


class PlayerRound(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    throws = models.IntegerField(default=0)
