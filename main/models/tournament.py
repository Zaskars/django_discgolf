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


class Course(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Layout(models.Model):
    course = models.ForeignKey(Course, related_name="layouts", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} at {self.course.name}"


class Basket(models.Model):
    layout = models.ForeignKey(Layout, related_name="baskets", on_delete=models.CASCADE)
    basket_number = models.IntegerField()
    par = models.IntegerField()

    def __str__(self):
        return f"Basket {self.basket_number} of {self.layout.name}"


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
