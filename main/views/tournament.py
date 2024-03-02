from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from main.forms.tournament_create import TournamentForm
from main.models import Tournament, Round, TournamentRegistration, Layout, PlayerProfile
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
        return reverse_lazy("tournament_update", kwargs={"pk": self.object.pk})


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
        context["is_full"] = (
            TournamentRegistration.objects.filter(tournament=tournament).count()
            >= tournament.max_players
        )
        context["rounds"] = Round.objects.filter(tournament=tournament)
        return context


class TournamentRegistrationView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def post(self, request, pk):
        tournament = get_object_or_404(Tournament, pk=pk)
        already_registered = TournamentRegistration.objects.filter(
            tournament=tournament, player=request.user.playerprofile
        ).exists()

        if already_registered:
            return HttpResponseForbidden("Вы уже зарегистрированы на этот турнир.")

        already_registered_count = TournamentRegistration.objects.filter(
            tournament=tournament
        ).count()

        if tournament.max_players > already_registered_count:
            TournamentRegistration.objects.create(
                tournament=tournament, player=request.user.playerprofile
            )
            return redirect("single_tournament", pk=pk)
        else:
            raise PermissionDenied("Все места на турнир заняты.")

    def get(self, request, *args, **kwargs):
        return redirect("home")


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
        context["registered_players"] = TournamentRegistration.objects.filter(
            tournament=tournament
        ).select_related("player")
        return context

    def form_valid(self, form):
        registered_players_count = TournamentRegistration.objects.filter(
            tournament=self.object
        ).count()

        if form.cleaned_data["max_players"] < registered_players_count:
            form.add_error(
                "max_players",
                "Нельзя установить количество мест меньше, чем уже зарегистрированных игроков.",
            )
            return self.form_invalid(form)

        return super().form_valid(form)

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


class DeletePlayerFromTournamentView(View):
    def dispatch(self, request, *args, **kwargs):
        self.player = get_object_or_404(PlayerProfile, pk=kwargs["player_id"])
        self.tournament = get_object_or_404(Tournament, pk=kwargs["tournament_id"])
        if self.tournament.director != request.user:
            raise PermissionDenied("Вы не имеете права удалять игрока")
        if not TournamentRegistration.objects.filter(
            tournament=self.tournament, player=self.player
        ).exists():
            raise Http404("Этот игрок не зарегистрирован на этом раунде")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        tournament_id = self.tournament.id
        registration = TournamentRegistration.objects.get(
            tournament=self.tournament, player=self.player
        )
        registration.delete()

        return redirect(reverse_lazy("tournament_update", kwargs={"pk": tournament_id}))
