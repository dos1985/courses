# Generated by Django 4.2.5 on 2023-09-23 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0003_product_is_deleted"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": "Продукт", "verbose_name_plural": "Продукты"},
        ),
    ]
