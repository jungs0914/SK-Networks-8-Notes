# Generated by Django 5.1.3 on 2024-12-10 03:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("game", "0001_initial"),
        ("player", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Dice",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("number", models.IntegerField()),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dice",
                        to="game.game",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dice",
                        to="player.player",
                    ),
                ),
            ],
            options={
                "db_table": "dice",
            },
        ),
    ]
