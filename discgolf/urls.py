"""
URL configuration for discgolf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views.auth import UserRegisterView, UserLoginView
from main.views.index import TournamentListView
from django.contrib.auth.views import LogoutView
from main.views.tournament import TournamentCreateView

urlpatterns = [
    path("", TournamentListView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path(
        "tournament_create/", TournamentCreateView.as_view(), name="tournament_create"
    ),
]
