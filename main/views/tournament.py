from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from main.forms.tournament_create import TournamentForm
from main.models import Tournament, Round, TournamentRegistration, Layout
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


class TournamentRegistrationView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

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

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.director != self.request.user:
            raise PermissionDenied("Вы не имеете права редактировать этот турнир")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.object
        context["rounds"] = Round.objects.filter(tournament=tournament)
        return context

    def get_success_url(self):
        return reverse_lazy("home")


class AddRoundToTournamentView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def dispatch(self, request, *args, **kwargs):
        tournament = get_object_or_404(Tournament, pk=kwargs["tournament_id"])
        if tournament.director != request.user:
            raise PermissionDenied("Вы не имеете права добавлять раунды в этот турнир")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, tournament_id, layout_id):
        tournament = get_object_or_404(Tournament, pk=tournament_id)
        layout = get_object_or_404(Layout, pk=layout_id)

        round_number = tournament.rounds.count() + 1
        Round.objects.create(
            tournament=tournament, layout=layout, round_number=round_number
        )

        return redirect("tournament_update", pk=tournament_id)


class DeleteRoundFromTournamentView(View):
    def dispatch(self, request, *args, **kwargs):
        self.round = get_object_or_404(Round, pk=kwargs["round_id"])

        if self.round.tournament.director != request.user:
            raise PermissionDenied("Вы не имеете права удалять этот раунд")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        tournament_id = self.round.tournament.id
        self.round.delete()

        return redirect(reverse_lazy("tournament_update", kwargs={"pk": tournament_id}))
