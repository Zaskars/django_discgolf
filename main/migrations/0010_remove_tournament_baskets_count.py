# Generated by Django 4.2.7 on 2023-12-05 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_alter_round_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tournament",
            name="baskets_count",
        ),
    ]
