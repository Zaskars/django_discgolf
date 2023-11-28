from django.db import models
from django.contrib.auth.models import User


class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    subscription_status = models.BooleanField(
        default=False
    )  # True если пользователь с подпиской
    city = models.CharField(max_length=100)
    birth_year = models.IntegerField()

    def update_rating(self, new_rating):
        self.rating = new_rating
        self.save()
