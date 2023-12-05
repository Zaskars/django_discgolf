from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from main.models import Course, Basket
from main.forms.course_create import CourseForm
from django.urls import reverse_lazy


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = "course_create.html"
    success_url = reverse_lazy("course_list")

    def form_valid(self, form):
        response = super(CourseCreateView, self).form_valid(form)
        baskets_count = int(self.request.POST.get("num_basket"))

        for i in range(1, baskets_count + 1):
            basket_par = self.request.POST.get(f"basket{i}")
            if basket_par:
                # Создание или обновление объекта basket
                Basket.objects.create(
                    course=self.object, basket_number=i, par=basket_par
                )

        return response


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
