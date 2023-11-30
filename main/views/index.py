from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from main.forms.tournament_create import TournamentForm
from main.models import Tournament
from django.contrib.auth.mixins import LoginRequiredMixin


class TournamentListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = "index.html"
    context_object_name = "tournaments"
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class TournamentCreateView(LoginRequiredMixin, CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = "tournament_create.html"
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        form.instance.director = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("home")
