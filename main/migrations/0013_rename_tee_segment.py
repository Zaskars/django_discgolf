# Generated by Django 4.2.7 on 2023-12-06 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_tee_remove_basket_par_delete_layoutbasket_tee_basket_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Tee",
            new_name="Segment",
        ),
    ]
