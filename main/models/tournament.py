from django.db import models
from django.contrib.auth.models import User

from .course import Segment, Layout
from .user import PlayerProfile


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    city = models.CharField(max_length=100)
    max_players = models.IntegerField()
    park_scheme = models.ImageField(upload_to="park_schemes/", null=True, blank=True)
    director = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super(Tournament, self).save(*args, **kwargs)

        if is_new:
            group, _ = Group.objects.get_or_create(name='Tournament Directors')
            self.director.groups.add(group)


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
    name = models.CharField(max_length=100, blank=True)
    # course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    layout = models.ForeignKey(
        Layout, on_delete=models.SET_NULL, null=True, related_name="rounds"
    )

    def get_registered_players(self):
        return [
            registration.player for registration in self.tournament.registrations.all()
        ]

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"Раунд {self.round_number}"
        super().save(*args, **kwargs)


class PlayerScore(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    throws = models.IntegerField()

    def __str__(self):
        return f"{self.player.user.username} - Round {self.round.round_number}, {self.segment}"
