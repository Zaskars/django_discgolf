from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView

from main.models import Round, Tournament


class RoundDetailView(LoginRequiredMixin, DetailView):
    model = Round
    template_name = "single_round.html"
    context_object_name = "round"
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get_object(self):
        tournament_id = self.kwargs.get("tournament_id")
        tournament = get_object_or_404(Tournament, pk=tournament_id)
        round_number = self.kwargs.get("round_number")
        return get_object_or_404(
            Round, tournament=tournament, round_number=round_number
        )
