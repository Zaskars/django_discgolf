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
from main.views.course import CourseCreateView, CourseListView
from main.views.index import TournamentListView
from django.contrib.auth.views import LogoutView

from main.views.layout import LayoutSelectionView
from main.views.profile import ProfileView, MyProfileView
from main.views.round import RoundDetailView
from main.views.tournament import (
    TournamentCreateView,
    TournamentDetailView,
    TournamentRegistrationView,
    TournamentUpdateView,
    AddRoundToTournamentView,
    DeleteRoundFromTournamentView,
)

urlpatterns = [
    path("", TournamentListView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path(
        "tournament_create/", TournamentCreateView.as_view(), name="tournament_create"
    ),
    path(
        "tournament/<int:pk>",
        TournamentDetailView.as_view(),
        name="single_tournament",
    ),
    path(
        "tournament/register/<int:pk>/",
        TournamentRegistrationView.as_view(),
        name="tournament_register",
    ),
    path(
        "tournament/update/<int:pk>/",
        TournamentUpdateView.as_view(),
        name="tournament_update",
    ),
    path(
        "tournament/update/<int:tournament_id>/round/layout_selection",
        LayoutSelectionView.as_view(),
        name="layout_selection",
    ),
    path(
        "tournament/<int:tournament_id>/round/<int:round_number>",
        RoundDetailView.as_view(),
        name="single_round",
    ),
    path(
        "tournament/<int:tournament_id>/add_round/<int:layout_id>/",
        AddRoundToTournamentView.as_view(),
        name="add_round_to_tournament",
    ),
    path(
        "tournament/<int:tournament_id>/delete_round/<int:round_id>/",
        DeleteRoundFromTournamentView.as_view(),
        name="delete_round_from_tournament",
    ),
    path(
        "profile/<int:pk>",
        ProfileView.as_view(),
        name="profile",
    ),
    path("my-profile/", MyProfileView.as_view(), name="my_profile"),
    path("course/create/", CourseCreateView.as_view(), name="course_create"),
    path("course/list/", CourseListView.as_view(), name="course_list"),
]
