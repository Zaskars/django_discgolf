from django import forms
from django.forms import inlineformset_factory

from main.models import Tournament, Round


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ["name", "date", "city", "max_players", "park_scheme"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "park_scheme": forms.FileInput(),
        }
