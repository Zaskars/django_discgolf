from django import forms
from django.forms import inlineformset_factory

from main.models import Tournament, Round


class TournamentForm(forms.ModelForm):
    rounds_count = forms.IntegerField(
        min_value=1, initial=1, label="Количество раундов"
    )

    class Meta:
        model = Tournament
        fields = ["name", "baskets_count", "date", "city", "max_players", "park_scheme"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "park_scheme": forms.FileInput(),
        }
