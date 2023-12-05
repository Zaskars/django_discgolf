from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.views.generic import ListView

from main.models import Course


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "course_list.html"
    context_object_name = "courses"
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get_queryset(self):
        queryset = Course.objects.annotate(
            total_par=Sum("baskets__par"), baskets_count=Count("baskets")
        )
        return queryset
