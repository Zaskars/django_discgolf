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
