# Generated by Django 4.2.7 on 2023-12-05 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_remove_basket_course_layout_basket_layout"),
    ]

    operations = [
        migrations.AlterField(
            model_name="round",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
