from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from main.forms.tournament_create import TournamentForm
from main.models import Tournament, Round
from django.contrib.auth.mixins import LoginRequiredMixin


class TournamentListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = "index.html"
    context_object_name = "tournaments"
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get_queryset(self):
        return Tournament.objects.annotate(
            rounds_count=Count("rounds"), registered_count=Count("registrations")
        )
