from django import forms

from main.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "country", "city"]
