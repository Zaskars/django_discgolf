from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from main.forms.tournament_create import TournamentForm
from main.models import Tournament, Round
from django.contrib.auth.mixins import LoginRequiredMixin


class TournamentCreateView(LoginRequiredMixin, CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = "tournament_create.html"

    def form_valid(self, form):
        response = super(TournamentCreateView, self).form_valid(form)
        rounds_count = int(self.request.POST.get("num_round"))

        for i in range(1, rounds_count + 1):
            round_name = self.request.POST.get(f"round{i}")
            if round_name:
                # Создание или обновление объекта Round
                Round.objects.create(
                    tournament=self.object, round_number=i, name=round_name
                )

        return response

    def get_success_url(self):
        return reverse_lazy("home")


class TournamentDetailView(LoginRequiredMixin, DetailView):
    model = Tournament
    template_name = "single_tournament.html"
    context_object_name = "tournament"
