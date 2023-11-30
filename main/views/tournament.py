from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView

from main.forms.tournament_create import TournamentForm
from main.models import Tournament, Round, TournamentRegistration
from django.contrib.auth.mixins import LoginRequiredMixin


class TournamentCreateView(LoginRequiredMixin, CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = "tournament_create.html"
    login_url = "/login/"
    redirect_field_name = "redirect_to"

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
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.object
        context["already_registered"] = TournamentRegistration.objects.filter(
            tournament=tournament, player=self.request.user.playerprofile
        ).exists()
        context["registered_players"] = TournamentRegistration.objects.filter(
            tournament=tournament
        ).select_related("player")
        return context


class TournamentRegistrationView(View):
    def post(self, request, pk):
        tournament = get_object_or_404(Tournament, pk=pk)
        TournamentRegistration.objects.create(
            tournament=tournament, player=request.user.playerprofile
        )
        return redirect("single_tournament", pk=pk)
