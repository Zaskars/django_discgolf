from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Layout(models.Model):
    course = models.ForeignKey(Course, related_name="layouts", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} at {self.course.name}"


class Basket(models.Model):
    course = models.ForeignKey(Course, related_name="baskets", on_delete=models.CASCADE)
    basket_number = models.IntegerField()

    def __str__(self):
        return f"Basket {self.basket_number} of {self.course.name}"


class Segment(models.Model):
    layout = models.ForeignKey(Layout, related_name="tees", on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    tee_number = models.IntegerField()
    par = models.IntegerField()

    def __str__(self):
        return f"Tee {self.tee_number} for {self.basket} in {self.layout.name}"
