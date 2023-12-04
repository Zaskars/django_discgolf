from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView

from main.models import PlayerProfile


class ProfileView(LoginRequiredMixin, DetailView):
    model = PlayerProfile
    template_name = "profile.html"
    context_object_name = "profile"
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class MyProfileView(LoginRequiredMixin, TemplateView):
    template_name = "my_profile.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
