from django.views.generic import ListView
from main.models import Layout


class LayoutSelectionView(ListView):
    model = Layout
    template_name = "layout_selection.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tournament_id"] = self.kwargs.get("tournament_id")
        return context
