# Generated by Django 5.1.4 on 2025-02-06 08:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("account_profile", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Board",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                (
                    "create_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("update_date", models.DateTimeField(auto_now=True)),
                (
                    "writer",
                    models.ForeignKey(
                        db_column="account_profile_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="boards",
                        to="account_profile.accountprofile",
                    ),
                ),
            ],
            options={
                "db_table": "board",
            },
        ),
    ]
