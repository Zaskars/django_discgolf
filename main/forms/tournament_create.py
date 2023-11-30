from django import forms
from main.models import Tournament


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ["name", "baskets_count", "date", "city", "max_players", "park_scheme"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "park_scheme": forms.FileInput(),
        }
