from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView

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
        form.instance.director = self.request.user
        return super(TournamentCreateView, self).form_valid(form)

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
        context["rounds"] = Round.objects.filter(tournament=tournament)
        return context


class TournamentRegistrationView(View):
    def post(self, request, pk):
        tournament = get_object_or_404(Tournament, pk=pk)
        TournamentRegistration.objects.create(
            tournament=tournament, player=request.user.playerprofile
        )
        return redirect("single_tournament", pk=pk)


class TournamentUpdateView(LoginRequiredMixin, UpdateView):
    model = Tournament
    form_class = TournamentForm
    template_name = "tournament_update.html"
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get_success_url(self):
        return reverse_lazy("home")
