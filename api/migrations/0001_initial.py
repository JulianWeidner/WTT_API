# Generated by Django 5.0.6 on 2024-06-23 20:49

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tournament",
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
                ("name", models.CharField(max_length=300)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
            ],
            options={
                "verbose_name": "tournaments",
                "ordering": ["start_time"],
            },
        ),
    ]
