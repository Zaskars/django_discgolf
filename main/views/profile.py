from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from main.models import PlayerProfile


class ProfileView(LoginRequiredMixin, DetailView):
    model = PlayerProfile
    template_name = "profile.html"
    context_object_name = "profile"
    login_url = "/login/"
    redirect_field_name = "redirect_to"
