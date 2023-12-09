from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from main.models import Layout, Tournament


class LayoutSelectionView(ListView):
    model = Layout
    template_name = "layout_selection.html"

    def dispatch(self, request, *args, **kwargs):
        self.tournament = get_object_or_404(Tournament, pk=kwargs["tournament_id"])
        if self.tournament.director != self.request.user:
            raise PermissionDenied("Вы не имеете права редактировать этот турнир")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tournament_id"] = self.kwargs.get("tournament_id")
        return context
