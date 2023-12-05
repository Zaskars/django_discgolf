from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from main.models.course import Course, Layout
from main.forms.course_create import CourseForm
from django.urls import reverse_lazy


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = "course_create.html"
    success_url = reverse_lazy("course_list")

    def form_valid(self, form):
        response = super(CourseCreateView, self).form_valid(form)
        layouts_count = int(self.request.POST.get("num_layout"))

        for i in range(1, layouts_count + 1):
            layout_name = self.request.POST.get(f"layout{i}")
            if layout_name:
                # Создание или обновление объекта layout
                Layout.objects.create(course=self.object, name=layout_name)

        return response


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "course_list.html"
    context_object_name = "courses"
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get_queryset(self):
        queryset = Course.objects.annotate(layouts_count=Count("layouts"))
        return queryset
