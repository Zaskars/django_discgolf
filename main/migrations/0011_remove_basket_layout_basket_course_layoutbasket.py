# Generated by Django 4.2.7 on 2023-12-06 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0010_remove_tournament_baskets_count"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="basket",
            name="layout",
        ),
        migrations.AddField(
            model_name="basket",
            name="course",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="baskets",
                to="main.course",
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="LayoutBasket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "basket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.basket"
                    ),
                ),
                (
                    "layout",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="layout_baskets",
                        to="main.layout",
                    ),
                ),
            ],
            options={
                "unique_together": {("layout", "basket")},
            },
        ),
    ]
