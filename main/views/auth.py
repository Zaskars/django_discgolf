from django.urls import reverse_lazy
from django.views import generic
from main.forms.registration import UserRegisterForm
from main.models import PlayerProfile
from main.forms.login import UserLoginForm
from django.contrib.auth.views import LoginView


class UserRegisterView(generic.CreateView):
    form_class = UserRegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        PlayerProfile.objects.create(
            user=self.object,
            city=form.cleaned_data["city"],
            birth_year=form.cleaned_data["birth_year"],
            subscription_status=form.cleaned_data["subscription_status"],
            rating=0,  # начальный рейтинг
        )
        return response


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")
