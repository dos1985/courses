# Generated by Django 4.2.5 on 2023-09-23 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_remove_lessonview_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]